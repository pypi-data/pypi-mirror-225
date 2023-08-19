"""
The Repo module contains the Arraylake classes for interacting with repositories, #AsyncRepo and #Repo.

The #Repo class provides a Zarr-compatible store interface for use with Zarr, Xarray, and other libraries
that support the Zarr protocol.

Repos should not be instantiated directly--instead, use the #Client and #AsyncClient, i.e.

```python
from arraylake_client import Client
client = Client()
repo = client.get_repo("my-org/my-repo")
```
"""

from __future__ import annotations

import asyncio
import datetime
import functools
import json
import random
import uuid
import warnings
from dataclasses import dataclass
from html import escape
from typing import (
    AsyncGenerator,
    Awaitable,
    Callable,
    Generator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

import zarr
from zarr._storage.store import StoreV3
from zarr.util import normalize_storage_path

from arraylake_client import config as config_obj
from arraylake_client.async_utils import (
    BlockingPortal,
    BlockingPortalGenerator,
    cached_portal,
)
from arraylake_client.chunkstore import Chunkstore
from arraylake_client.commits import CommitData, CommitLog
from arraylake_client.exceptions import (
    CommitFailedError,
    DocumentNotFoundError,
    InvalidPrefixError,
)
from arraylake_client.log_util import get_logger
from arraylake_client.metastore import MetastoreDatabase
from arraylake_client.types import (
    Author,
    BranchName,
    CollectionName,
    CommitID,
    NewCommit,
    Path,
    ReferenceData,
    SessionID,
    SessionInfo,
    SessionPathsResponse,
    Tree,
)
from arraylake_client.virtual import reformat_kerchunk_refs, scan_netcdf, scan_zarr_v2
from arraylake_client.zarr_util import (
    ENTRY_POINT_METADATA,
    data_root,
    is_chunk_key,
    is_meta_key,
    meta_root,
)

logger = get_logger(__name__)

metadata_collection = CollectionName("metadata")
chunks_collection = CollectionName("chunks")


def _write_op(func):
    """
    Decorator for write operations. Ensures that the repo is in a writable state.
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._writable:
            raise IOError("Repo is not writable")
        return func(self, *args, **kwargs)

    return wrapper


AsyncFunctionOrGenerator = TypeVar("AsyncFunctionOrGenerator", AsyncGenerator, Awaitable)


def _dispatch_over_collections(func: Callable[..., AsyncFunctionOrGenerator], prefix: str, **kwargs) -> List[AsyncFunctionOrGenerator]:
    """A utility function for calling async functions against multiple collections.

    Args:
        func: The function to call. It should accept `prefix` as the first argument and `collection` as a keyword argument.
        prefix: The prefix to use for the function call. If the prefix starts with `meta`.
            The function will be called against the metadata_collection. If the prefix starts with `data`,
            the function will be called against the chunks_collection. If the prefix is empty, the function
            will be called against both collections.
        kwargs: Keyword arguments to pass to the function

    Returns:
        A list of results from the function calls (length 0, 1, or 2). These can be awaited or async iterated over,
        depending on the input function return type.
    """

    collections = {"data": chunks_collection, "meta": metadata_collection}

    if prefix == "":
        return [func(prefix, collection=c, **kwargs) for c in collections.values()]

    key = prefix[:4]
    collection = collections.get(key)
    if collection:
        return [func(prefix, collection=collection, **kwargs)]
    else:
        raise InvalidPrefixError(f"Invalid prefix: {0}. Prefix should start with 'meta', 'data' or be the empty string.".format(prefix))


class AsyncRepo:
    """Asynchronous interface to Arraylake repo.

    :::note
    Because Zarr does not support asynchronous I/O, the async client cannot be used to read or write Zarr data directly.
    :::

    The async repo should be used as a context manager
    ```python

    async with async_repo:
        async_repo.checkout("main")
    ```
    """

    db: MetastoreDatabase
    chunkstore: Chunkstore
    repo_name: str
    author: Author

    _db: Optional[MetastoreDatabase]  # set in __aenter__
    _commit_data: Optional[CommitData]  # set in _refresh_commit_data
    _session: Optional[SessionInfo]  # set in checkout
    _writable: bool

    def __init__(self, metastore_db: MetastoreDatabase, chunkstore: Chunkstore, name: str, author: Author):
        """
        Args:
            metastore_db: A metastore database for storing metadata
            chunkstore: A chunkstore for storing chunks
            name: The name of the repo. Purely for display purposes.
            author: The author name and email for commits
        """
        self.db = metastore_db
        self.chunkstore = chunkstore
        self.repo_name = name
        self.author = author

        # The following can't be initialized until we're in the async context because we need to query the metastore
        self._commit_data = None
        self._session = None
        self._OPEN = False
        self._writable = False

    async def __aenter__(self):
        await self.db.__aenter__()
        await self.chunkstore.__aenter__()
        self._OPEN = True
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.db.__aexit__(*args, **kwargs)
        await self.chunkstore.__aexit__(*args, **kwargs)
        self._OPEN = False

    def __getstate__(self):
        return self.db, self.chunkstore, self.repo_name, self.author, self._session, self._OPEN, self._writable

    def __setstate__(self, state):
        self.db, self.chunkstore, self.repo_name, self.author, self._session, self._OPEN, self._writable = state
        # commit_data can be large and is not needed for most operations, therefore we omit it during serialization.
        self._commit_data = None

    def __repr__(self):
        repo_name = self.repo_name
        status = "OPEN" if self._OPEN else "CLOSED"
        return f"<arraylake_client.repo.AsyncRepo name='{repo_name}' status={status}>"

    @property
    def session(self) -> SessionInfo:
        # accessing the session via this property makes mypy happy
        if self._session is None:
            raise ValueError("There is no session active. You have to call checkout first.")
        return self._session

    async def commit_data(self) -> CommitData:
        """Returns the #CommitData for the current session."""
        if self._commit_data is None:
            if not self._OPEN:
                raise ValueError("must be in async context to fetch commit_data")
            # lazily refresh commit data
            await self._refresh_commit_data()
        return self._commit_data

    async def commit_log(self) -> CommitLog:
        """Returns the #CommitLog for the current session."""

        return CommitLog(self.repo_name, self.session["base_commit"], await self.commit_data())

    async def status(self, limit: int = 1000) -> SessionStatus:
        """Returns the #SessionStatus for the current session.

        Args:
            limit (int): [Optional] The number of modified paths to return. Defaults to 1000, passing 0
            is equivalent to setting no limit.
        """
        modified_paths = [(spr.path, spr.deleted) async for spr in self._modified(limit=limit)]
        if len(modified_paths) >= limit:
            warnings.warn(
                f".status results were limited to the first {limit} records. If more records are required, use .status(limit={limit})"
            )
        return SessionStatus(repo_name=self.repo_name, session=self.session, modified_paths=modified_paths)

    async def _refresh_commit_data(self) -> None:
        commit_list = await self.db.get_commits()
        tags, branches = await self.db.get_refs()
        self._commit_data = CommitData(commit_list, tags, branches)

    async def ping(self) -> None:
        """Ping the metastore to confirm connection"""

        await self.db.ping()
        await self.chunkstore.ping()

    async def checkout(self, ref: str = "main") -> CommitID:
        """Checkout a ref (branch, tag, or commit ID) and initialize a new session.

        Args:
            ref: Commit, branch, or tag name

        Returns:
            commit: #CommitID
        """

        await self._refresh_commit_data()
        commit, branch = (await self.commit_data()).get_ref(ref)

        session_start_time = datetime.datetime.utcnow()
        # TODO: replace this with a pydantic model
        self._session = {"id": SessionID(uuid.uuid4().hex), "start_time": session_start_time, "base_commit": commit, "branch": branch}

        if branch is None:
            warnings.warn("You are not on a branch tip, so you can't commit changes.")
            self._writable = False
        else:
            self._writable = True

        return commit

    async def commit(self, message: str, auto_ff=True) -> CommitID:
        """Commit this session's changes and start a new session.

        Args:
            message: Commit message
            auto_ff: Whether to automatically fast-forward the repo and retry if the commit fails

        Returns:
            new_commit: ID of new commit
        """
        return await self._single_commit(message)

    async def _single_commit(self, message: str, attempt=0) -> CommitID:
        """Create a new commit based on current state and attempt to write to branch."""
        max_attempts = int(config_obj.config.get("max_commit_attempts", 50))
        max_jitter = 5  # seconds
        if self.session["branch"] is None:
            raise RuntimeError("You are not on a branch tip, so you can't commit changes.")

        commit_metadata = NewCommit(
            session_id=self.session["id"],
            session_start_time=self.session["start_time"],
            parent_commit=self.session.get("base_commit", None),
            commit_time=datetime.datetime.utcnow(),
            author_name=self.author.name,
            author_email=self.author.email,
            message=message,
        )

        # the server will validate if the commit can happen
        # and return an error if not
        try:
            new_commit = await self.db.new_commit(commit_metadata)
        except ValueError as err:
            if str(err).startswith("No changes to commit"):
                warnings.warn(str(err))
                return self.session.get("base_commit", None)
            else:
                raise err

        new_branch = (self.session["branch"] not in (await self.commit_data()).branches) or (self.session["base_commit"] is None)
        try:
            await self.db.update_branch(
                self.session["branch"], base_commit=self.session["base_commit"], new_commit=new_commit, new_branch=new_branch
            )
        # TODO: fix metastore impl. inconsistency around error classes here
        except (ValueError, RuntimeError) as err:
            if not (str(err).startswith("Failed to update branch") or str(err).startswith("Cannot create branch")):
                raise
            else:
                if attempt < max_attempts:
                    await logger.ainfo(f"Encountered commit conflict {attempt}, retrying")
                    # add a small amount of jitter to avoid dos
                    delay = random.uniform(0, max_jitter)
                    await asyncio.sleep(delay)
                    await self._rebase(new_commit)
                    return await self._single_commit(message, attempt=attempt + 1)
                else:
                    raise CommitFailedError(f"Failed to update branch {self.session['branch']} to point to commit {new_commit}")

        # reset session parameters
        checked_out_commit = await self.checkout(self.session["branch"])
        assert checked_out_commit == new_commit, "These should always match"
        return new_commit

    async def _rebase(self, commit_id: CommitID):
        """Update the session base commit to branch HEAD, if possible."""
        branch = self.session["branch"]
        try:
            latest_branch_commit_id = await self.db.rebase(commit_id, branch)
            self._session["base_commit"] = latest_branch_commit_id
            await self._refresh_commit_data()
        except ValueError as err:
            if not str(err).startswith("Branch does not exist"):
                raise

    async def fast_forward(self):
        """Fast-forward the session.
        Attempts to update the session base commit to the latest branch tip.
        Will fail if the same paths have been modified in the current session and on the branch.
        """
        try:
            latest_commit = await self._try_fast_forward()
            # it succeeded; we can move the branch tip
            self._session["base_commit"] = latest_commit
        except Exception:
            raise

    async def _try_fast_forward(self) -> CommitID:
        # returns the ID to ff to

        if self.session["branch"] is None:
            raise RuntimeError("Fast-forward unavailable: You are not on a branch tip")

        await self._refresh_commit_data()
        branch = self.session["branch"]
        branch_latest_commit = (await self.commit_data()).branches.get(branch, None)
        session_base_commit = self._session["base_commit"]

        if branch_latest_commit is None:
            # that branch has seen no commits yet
            return branch_latest_commit

        if branch_latest_commit == session_base_commit:
            # no new commits have come in on this branch, nothing to ff
            return branch_latest_commit

        # our _modified check is unlimited
        # this is to ensure that any overlaps are accounted for when comparing to the modified
        # paths of other sessions later in the logic of fast forwarding
        modified_paths = set([spr.path async for spr in self._modified(limit=0)])
        if len(modified_paths) == 0:
            # nothing changed; nothing to do
            return branch_latest_commit

        # this is different from self.commit_log because it starts from branch_latest_commit
        commit_log = CommitLog(self.repo_name, branch_latest_commit, await self.commit_data())
        upstream_modifications = set()
        for commit in commit_log:
            if commit.id == session_base_commit:
                # we can stop iterating
                break
            for collection in (metadata_collection, chunks_collection):
                upstream_modifications.update(
                    {response.path async for response in self.db.get_all_paths_for_session(commit.session_id, collection=collection)}
                )
        conflicting_paths = upstream_modifications & modified_paths
        if conflicting_paths:
            raise RuntimeError(f"Can't fast-forward due to conflicting paths {conflicting_paths}.")
        return branch_latest_commit

    async def new_branch(self, branch_name: str) -> None:
        """Create a new branch based on the current session reference

        Args:
            branch_name: New branch name
        """

        branch = BranchName(branch_name)
        if self._session is None:
            # this was added to make mypy happy but is not covered by tests
            raise ValueError("There is no session active. You have to call checkout first.")
        if branch in (await self.commit_data()).branches or branch == self.session["branch"]:
            raise ValueError(f"Branch {branch} already exists.")
        self._session["branch"] = branch

    @_write_op
    async def _set_doc(self, path: Path, *, content: dict) -> None:
        """Write a single document to the metastore

        Parameters
        ----------
        path : str
            Path to document in the metastore
        content : dict
            Document contents
        """
        await self._set_docs({path: content})

    @_write_op
    async def _set_docs(self, items: Mapping[Path, dict]) -> None:
        """Write multiple documents to the metastore

        Parameters
        ----------
        items : dict
            Mapping where the keys are document paths and values are documents in the form of dictionaries.
        """
        await self.db.add_docs(items, collection=metadata_collection, session_id=self.session["id"])

    async def _get_doc(self, path: Path) -> Mapping[Path, dict]:
        """Get a single document from the metastore

        Parameters
        ----------
        path : str
            Path to document in the metastore

        Returns
        -------
        content : dict
            Document contents
        """
        result = await self._get_docs([path])
        try:
            return result[path]
        except KeyError:
            raise DocumentNotFoundError

    async def _doc_exists(self, path: Path) -> bool:
        """Check if a doc exists in the metastore

        Parameters
        ----------
        path : str
            Document path
        """
        try:
            # Here we are trading a small amount of extra data transfer
            # (just getting the whole doc) in order to simplify our code.
            # Since individual docs are all tiny, in practice, this should not have
            # any performance consequence, as other sources of latency are much, much higher.
            await self._get_doc(path)
            return True
        except DocumentNotFoundError:
            return False

    async def _get_docs(self, paths: Sequence[str]) -> Mapping[Path, dict]:
        """Get multiple documents from the metastore

        Parameters
        ----------
        paths : sequence of str
            Sequence of document paths

        Returns
        -------
        docs : dict
            Mapping where keys are document paths and values are documents in the form of dictionaries.
        """
        # Here we do what fsspec does and just OMIT the missing paths from the dictionary
        db_results = {
            doc.path: doc.content
            async for doc in self.db.get_docs(
                paths, collection=metadata_collection, session_id=self.session["id"], commit_id=self.session["base_commit"]
            )
        }
        return db_results

    @_write_op
    async def _del_docs(self, paths: Sequence[str]) -> None:
        """Delete multiple documents from the metastore

        Parameters
        ----------
        paths : sequence of str
            Sequence of document paths
        """
        await self.db.del_docs(paths, collection=metadata_collection, session_id=self.session["id"])

    @_write_op
    async def _del_doc(self, path: Path) -> None:
        """Delete a single documents from the metastore

        Parameters
        ----------
        path : str
            Document path
        """
        # make sure there is actually a doc there first
        # TODO: make this as inexpensive as possible
        _ = await self._get_doc(path)
        await self.db.del_docs([path], collection=metadata_collection, session_id=self.session["id"])

    @_write_op
    async def _del_prefix(self, prefix: Path) -> None:
        """Delete all documents with a given prefix from the metastore

        Parameters
        ----------
        prefix : str
            Document path prefix
        """
        try:
            delete_functions = _dispatch_over_collections(
                self.db.del_prefix, prefix, commit_id=self.session["base_commit"], session_id=self.session["id"]
            )
        except InvalidPrefixError:
            return
        await asyncio.gather(*delete_functions)

    @_write_op
    async def _set_chunk(self, path: Path, *, data: bytes) -> None:
        """Write a single chunk to the chunkstore and record it in the metastore's chunk manifest

        Parameters
        ----------
        path : str
            Document path
        data : bytes
            Chunk data
        """
        await self._set_chunks({path: data})

    @_write_op
    async def _set_chunks(self, items: Mapping[Path, bytes]) -> None:
        """Write a single chunk to the chunkstore and record it in the metastore's chunk manifest

        Parameters
        ----------
        path : str
            Document path
        data : bytes
            Chunk data
        """
        chunk_refs = await asyncio.gather(*(self.chunkstore.add_chunk(data) for data in items.values()))
        chunk_ref_dicts = [ref.dict() for ref in chunk_refs]  # convert from pydantic model
        await self.db.add_docs(dict(zip(items, chunk_ref_dicts)), collection=chunks_collection, session_id=self.session["id"])

    async def _set_chunk_ref(self, path: Path, *, reference_data: ReferenceData) -> None:
        """Set a chunk reference in the metastore

        Parameters
        ----------
        path : str
            Document path
        reference_data : ReferenceData
            Chunk reference document
        """
        await self.db.add_docs({path: reference_data.dict()}, collection=chunks_collection, session_id=self.session["id"])

    async def _set_chunk_refs(self, items: Mapping[Path, ReferenceData]) -> None:
        """Set multiple chunk reference documents in the metastore

        Parameters
        ----------
        items : dict
            Mapping where keys are paths and values are chunk reference documents in the form of dictionaries
        """
        chunk_refs = {k: ref.dict() for k, ref in items.items()}  # convert from pydantic model
        await self.db.add_docs(chunk_refs, collection=chunks_collection, session_id=self.session["id"])

    async def _get_chunk_ref(self, path: Path) -> ReferenceData:
        """Get a single chunk reference from the metastore

        Parameters
        ----------
        path : str
            Document path

        Returns
        -------
        refdata : ReferenceData
            Chunk reference document
        """
        results = await self._get_chunk_refs([path])
        try:
            return results[path]
        except KeyError:
            raise DocumentNotFoundError

    async def _get_chunk_refs(self, paths: Sequence[str]) -> Mapping[Path, ReferenceData]:
        """Get multiple chunk references from the metastore

        Parameters
        ----------
        paths : sequence of str
            Sequence of document paths

        Returns
        -------
        docs : dict
            Mapping where keys are paths and values are chunk ``ReferenceData`` objects.
        """
        # Here we do what fsspec does and just OMIT the missing paths from the dictionary
        db_results = {
            doc.path: ReferenceData(**doc.content)
            async for doc in self.db.get_docs(
                paths, collection=chunks_collection, session_id=self.session["id"], commit_id=self.session["base_commit"]
            )
        }
        return db_results

    async def _get_chunk(self, path: Path, *, validate: bool = False) -> bytes:
        """Get a chunk from the chunkstore

        Parameters
        ----------
        path : str
            Chunk path
        validate : bool, default=False
            If True, validate the chunk hash after retrieving it from the chunkstore
        """
        chunk_ref = await self._get_chunk_ref(path)
        chunk = await self.chunkstore.get_chunk(chunk_ref, validate=validate)
        return chunk

    async def _get_chunks(self, paths: Sequence[Path]) -> Mapping[Path, bytes]:
        """Get multiple chunks from the chunkstore

        Parameters
        ----------
        paths : sequence of str
            Sequence of chunk paths

        Returns
        -------
        chunks : dict
            Mapping where keys are paths and values are chunk objects in the form of bytes.
        """
        chunk_refs = await self._get_chunk_refs(paths)
        chunks = await asyncio.gather(*(self.chunkstore.get_chunk(ref) for ref in chunk_refs.values()))
        return dict(zip(chunk_refs, chunks))

    async def _chunk_exists(self, path: Path) -> bool:
        """Check if a chunk exists in the metastore

        Parameters
        ----------
        path : str
            Chunk path

        Returns
        -------
        bool

        .. note:: The presence of the chunk is only checked in the metastore's chunk manifest, not the chunkstore.
        """
        try:
            await self._get_chunk_ref(path)
            return True
        except DocumentNotFoundError:
            return False

    @_write_op
    async def _del_chunk(self, path: Path) -> None:
        """Delete a single chunk from the metastore

        Parameters
        ----------
        path : str
            Document path

        .. note:: This method does not remove the chunk from the chunkstore, only the metastore's chunk manifest

        """
        _ = await self._get_chunk_ref(path)
        await self.db.del_docs([path], collection=chunks_collection, session_id=self.session["id"])

    @_write_op
    async def _del_chunks(self, paths: Sequence[str]) -> None:
        """Delete multiple chunks from the metastore

        Parameters
        ----------
        paths : sequence of str
            Sequence of chunk paths

        .. note:: This method does not remove chunks from the chunkstore, only the metastore's chunk manifest
        """
        await self.db.del_docs(paths, collection=chunks_collection, session_id=self.session["id"])

    # Note: this implementation does not support implicit groups!
    # The zarr V3 abstract store interface (https://zarr-specs.readthedocs.io/en/latest/core/v3.0.html#abstract-store-interface) says
    # > For example, if a store contains the keys “a/b”, “a/c”, “a/d/e”, “a/f/g”
    # > then _list_dir("a/") would return keys “a/b” and “a/c” and prefixes “a/d/” and “a/f/”.
    # > _list_dir("b/") would return the empty set.
    # This is problematic for us for because, even if we could discover the prefixes "a/d/" and "a/f/", we couldn't
    # assign a unique session_id to them.
    # To resolve this, I propose we DISALLOW IMPLICIT GROUPS. This will help a lot, because every "directory"
    # corresponds to a .group.json document.

    async def _list(self, prefix: str, *, all_subdirs: bool = False, _jmespath_filter_expression: str = None) -> AsyncGenerator[Path, None]:
        """Convenience function to dispatch queries to the right collection"""
        kwargs = dict(
            session_id=self.session["id"],
            commit_id=self.session["base_commit"],
            all_subdirs=all_subdirs,
            _jmespath_filter_expression=_jmespath_filter_expression,
        )
        try:
            async_generators = _dispatch_over_collections(self.db.list, prefix, **kwargs)
        except InvalidPrefixError:
            return
        for agen in async_generators:
            async for path in agen:
                yield path

    async def _list_dir(self, prefix: str) -> AsyncGenerator[Path, None]:
        """List a directory in the metastore

        Parameters
        ----------
        prefix : str

        Yields
        ------
        path : str
            Document path
        """
        path_query = normalize_storage_path(prefix)

        # TODO: refactor all of this once Zarr python reverts to not having a top-level entry point
        # we don't need a query for these; they are guaranteed to exist
        if path_query == "":
            for prefix in ["data", "meta", "zarr.json"]:
                yield prefix
            return
        elif path_query == "data":
            yield "root"
            return

        start = len(path_query) + 1
        groups_seen = set()
        async for path in self._list(path_query, all_subdirs=False):
            # a group may end with .group.json (explicit) or have no
            # suffix (implicit). in the group
            # (in progress) should this logic be tweaked to find items without a suffix too (i.e a dir?)
            if path.endswith(".group.json"):
                p = path[start:-11]
                if p not in groups_seen:
                    yield path[start:]
                    groups_seen.add(p)
            else:
                # trim the start of the path off, we only want what's in the dir
                # e.g. meta/root/baz.array.json -> baz.array.json
                yield path[start:]

    async def _list_prefix(self, prefix: str) -> AsyncGenerator[str, None]:
        """List a prefix in the metastore

        Parameters
        ----------
        prefix : str

        Yields
        ------
        path : str
            Document path
        """

        # starting with a prefix is invalid
        if prefix.startswith("/"):
            raise ValueError("prefix must not begin with /")
        path_query = normalize_storage_path(prefix)

        # The function normalize_storage_path is responsible for cleaning paths,
        # which includes removing leading and trailing slashes ("/"). However,
        # if the provided prefix already has a trailing slash, it should be retained.
        # This is important because store.list_dir uses store.list_prefix,
        # but list_dir only supports directory listing and not general
        # key prefix matching. To ensure proper functionality, we need to make
        # sure that the prefix we use includes a trailing slash in this case.
        if prefix.endswith("/"):
            path_query += "/"

        async for path in self._list(path_query, all_subdirs=True):
            yield path
        if path_query == "":
            yield "zarr.json"

    async def _modified(self, limit=1000) -> AsyncGenerator[SessionPathsResponse, None]:
        """Get modified paths for session, across both chunks and metadata.

        We query multiple collections to determine modified paths. To enforce a limit, we manually
        manage the number of docs that we yield with this call.
        """
        c = 0
        while (limit == 0) or c < limit:
            async for item in self.db.get_all_paths_for_session(self.session["id"], collection=metadata_collection, limit=limit):
                yield item
                c += 1
            async for item in self.db.get_all_paths_for_session(self.session["id"], collection=chunks_collection, limit=limit):
                yield item
                c += 1
            break

    async def _getsize(self, prefix: str) -> int:
        """Get the size of a prefix in the metastore

        Parameters
        ----------
        prefix : str

        Returns
        -------
        size : int
            Size of all documents in the prefix (only includes chunks, not metadata)
        """
        path_query = normalize_storage_path(prefix)
        response = await self.db.getsize(
            path_query,
            session_id=self.session["id"],
            commit_id=self.session["base_commit"],
        )
        return response.total_chunk_bytes

    async def tree(self, prefix: str = "", depth: int = 10) -> Tree:
        """Display this repo's hierarchy as a Rich Tree

        Args:
            prefix: Path prefix
            depth: Maximum depth to descend into the hierarchy
        """

        # this is a bit fragile but will go away soon
        if not prefix.startswith("meta/"):
            prefix = "meta/" + prefix

        tree_obj = await self.db.tree(prefix=prefix, depth=depth, session_id=self.session["id"], commit_id=self.session["base_commit"])
        return tree_obj

    @_write_op
    async def add_virtual_netcdf(self, path: Path, netcdf_uri: str, **kwargs) -> None:
        """Add a virtual Netcdf dataset to the repo.

        Args:
            path: The path within the repo where the virtual dataset should be created.
            netcdf_uri: The path to the netCDF file. Only `s3://` URIs are supported at the moment.
              Both netCDF4 and netCDF3 files are supported.
            kwargs: Additional arguments to pass to the kerchunk
              [file format backend](https://fsspec.github.io/kerchunk/reference.html#file-format-backends).
              Do not pass `storage_options` or `inline_threshold`.
        """
        kerchunk_refs = scan_netcdf(netcdf_uri, **kwargs)
        meta_docs, chunk_refs = reformat_kerchunk_refs(kerchunk_refs, path)
        asyncio.gather(self._set_docs(meta_docs), self._set_chunk_refs(chunk_refs))

    @_write_op
    async def add_virtual_zarr(self, path: Path, zarr_uri: str) -> None:
        """Add a virtual Zarr dataset to the repo.

        Args:
            path: The path within the repo where the virtual dataset should be created.
            zarr_uri: The path to the Zarr store. Only Zarr V2 stores and `s3://` URIs are supported at the moment.
        """
        kerchunk_refs = scan_zarr_v2(zarr_uri)
        meta_docs, chunk_refs = reformat_kerchunk_refs(kerchunk_refs, path)
        asyncio.gather(self._set_docs(meta_docs), self._set_chunk_refs(chunk_refs))


def _sort_keys(keys: Sequence[str]) -> tuple[list[str], list[str]]:
    """Convenience function to sort keys into meta_keys and chunk_keys"""
    chunk_keys = []
    meta_keys = []
    bad_keys = []
    for key in keys:
        if is_chunk_key(key):
            chunk_keys.append(key)
        elif is_meta_key(key):
            meta_keys.append(key)
        else:  # pragma: no cover
            bad_keys.append(key)
    if bad_keys:  # pragma: no cover
        # don't expect to get here because we have already called self._validate_key
        raise ValueError(f"unexpected keys: {key}")
    return meta_keys, chunk_keys


class Repo:
    """Synchronous interface to Arraylake repo."""

    _arepo: AsyncRepo
    _OPEN: bool
    _cached_portal_context: Optional[BlockingPortalGenerator]
    _portal: Optional[BlockingPortal]
    _arepo_context: Optional[Generator]

    def __init__(self, arepo: AsyncRepo):
        """
        Initialize a Repo from an initialized AsyncRepo

        Args:
            arepo: An existing AsyncRepo
        """
        self._arepo = arepo

        # default / unset attributes used to wrap AsyncRepo
        self._OPEN = False
        self._cached_portal_context = None
        self._portal = None
        self._arepo_context = None

    @classmethod
    def from_metastore_and_chunkstore(cls, metastore_db: MetastoreDatabase, chunkstore: Chunkstore, name: str, author: Author) -> Repo:
        """
        Initialize a Repo from an initialized metastore database and chunkstore

        Args:
            metastore_db: A metastore database for storing metadata
            chunkstore: A chunkstore for storing chunks
            name: The name of the repo. Purely for display purposes.
            author: The author name and email for commits
        """
        arepo = AsyncRepo(metastore_db, chunkstore, name, author)
        return cls(arepo)

    @property
    def repo_name(self) -> str:
        return self._arepo.repo_name

    def _open(self):
        """using a AnyIO blocking portal, enter the AsyncRepo's async context"""

        # Acquire the blocking portal .acquire() returns a context manager that when entered, provisions a BlockingPortal.
        # and when exited, deprovisions the BlockingPortal (provided there are no other active references, e.g. from
        # other repo objects).
        self._cached_portal_context = cached_portal.acquire()
        self._portal = self._cached_portal_context.__enter__()
        # wrap_async_context_manager wraps the AsyncRepo object and .__enter__() enters the async context (synchronously)
        self._arepo_context = self._portal.wrap_async_context_manager(self._arepo)
        self._arepo_context.__enter__()

        # _OPEN signals that the portal and async context are ready for use
        self._OPEN = True

    def _synchronize(self, method, *args, **kwargs):
        if not self._OPEN:
            self._open()

        # we have to wrap the method because portal.call doesn't support kwargs
        def wrapped_method():
            return method(*args, **kwargs)

        @functools.wraps(method)
        def wrap(*args, **kwargs):
            return self._portal.call(wrapped_method)

        return wrap(*args, **kwargs)

    def _wrap_async_iter(self, func, *args, **kwargs):
        async def iter_to_list():
            # TODO: replace with generators so we don't load massive lists into memory
            # (e.g. list_prefix(""))
            return [item async for item in func(*args, **kwargs)]

        return self._synchronize(iter_to_list)

    def __getstate__(self):
        return self._arepo

    def __setstate__(self, state):
        self._arepo = state
        self._open()

    def close(self):
        if self._OPEN:
            try:
                self._arepo_context.__exit__(None, None, None)
            except RuntimeError:
                pass
            self._arepo_context = None
            self._portal = None
            self._cached_portal_context.__exit__(None, None, None)
            self._cached_portal_context = None
            self._OPEN = False

    def __del__(self):
        self.close()

    def __repr__(self):
        repo_name = self._arepo.repo_name
        return f"<arraylake_client.repo.Repo '{repo_name}'>"

    def initialize_v3_store(self):
        """Initialize a Zarr V3 store on this Repo."""
        self._synchronize(self._arepo.initialize_v3_store)

    def ping(self):
        """Ping the metastore to confirm connection"""

        return self._synchronize(self._arepo.ping)

    def checkout(self, ref="main") -> CommitID:
        """Checkout a ref (branch, tag, or commit ID) and initialize a new session.

        Args:
            ref: Commit, branch, or tag name

        Returns:
            commit: #CommitID
        """

        return self._synchronize(self._arepo.checkout, ref)

    def commit(self, message: str, auto_ff=True) -> str:
        """Commit this session's changes and start a new session.

        Args:
            message: Commit message
            auto_ff: Whether to automatically fast-forward the repo and retry if the commit fails

        Returns:
            new_commit: ID of new commit
        """

        return self._synchronize(self._arepo.commit, message, auto_ff=auto_ff)

    def fast_forward(self):
        """Fast-forward the session.
        Attempts to update the session base commit to the latest branch tip.
        Will fail if the same paths have been modified in the current session and on the branch.
        """

        return self._synchronize(self._arepo.fast_forward)

    def new_branch(self, branch: str) -> None:
        """Create a new branch based on the current session reference

        Args:
            branch_name: New branch name
        """

        return self._synchronize(self._arepo.new_branch, branch)

    # TODO: figure out some clever metaclass way of wrapping all of these methods
    # For now it's faster to just plug and chug
    def _set_doc(self, path: Path, *, content: dict) -> None:
        return self._synchronize(self._arepo._set_doc, path, content=content)

    def _set_docs(self, items: Mapping[str, dict]) -> None:
        return self._synchronize(self._arepo._set_docs, items)

    def _get_doc(self, path: Path) -> dict:
        return self._synchronize(self._arepo._get_doc, path)

    def _doc_exists(self, path: Path) -> bool:
        return self._synchronize(self._arepo._doc_exists, path)

    def _get_docs(self, paths: Sequence[str]) -> Mapping[str, dict]:
        return self._synchronize(self._arepo._get_docs, paths)

    def _del_doc(self, path: Path) -> None:
        return self._synchronize(self._arepo._del_doc, path)

    def _del_docs(self, paths: Sequence[str]) -> None:
        return self._synchronize(self._arepo._del_docs, paths)

    def _set_chunk(self, path: Path, *, data: bytes) -> None:
        return self._synchronize(self._arepo._set_chunk, path, data=data)

    def _set_chunks(self, items: Mapping[str, bytes]) -> None:
        return self._synchronize(self._arepo._set_chunks, items)

    def _get_chunk(self, path: Path) -> bytes:
        return self._synchronize(self._arepo._get_chunk, path)

    def _chunk_exists(self, path: Path) -> bool:
        return self._synchronize(self._arepo._chunk_exists, path)

    def _get_chunks(self, paths: Sequence[str]) -> Mapping[str, bytes]:
        return self._synchronize(self._arepo._get_chunks, paths)

    def _del_chunk(self, path: Path) -> None:
        return self._synchronize(self._arepo._del_chunk, path)

    def _del_chunks(self, paths: Sequence[str]) -> None:
        return self._synchronize(self._arepo._del_chunks, paths)

    def _set_chunk_ref(self, path: Path, *, reference_data: ReferenceData) -> None:
        return self._synchronize(self._arepo._set_chunk_ref, path, reference_data=reference_data)

    def _set_chunk_refs(self, items: Mapping[Path, ReferenceData]) -> None:
        return self._synchronize(self._arepo._set_chunk_refs, items)

    @property
    def store(self) -> ArraylakeStore:
        """Access a Zarr-compatible #ArraylakeStore store object for this repo.

        Example:

        ```python
        repo = Repo("my_org/my_repo")
        group = zarr.open_group(store=repo.store)
        ```
        """
        return ArraylakeStore(self)

    @property
    def root_group(self) -> zarr.Group:
        """Open the Zarr root group of this repo.

        Example:

        ```python
        repo = Repo("my_org/my_repo")
        group = repo.root_group
        group.tree()  # visualize group hierarchy
        ```
        """
        return zarr.open_group(store=self.store, zarr_version=3)

    def status(self, limit: int = 1000):
        """Returns the #SessionStatus for the current session.

        Args:
           limit (int): [Optional] The number of modified paths to return. Defaults to 1000, passing 0
           is equivalent to setting no limit."""
        return self._synchronize(self._arepo.status, limit=limit)

    @property
    def commit_log(self):
        return self._synchronize(self._arepo.commit_log)

    def add_virtual_hdf(self, path: Path, hdf_uri: str) -> None:
        """Add a virtual HDF5 dataset to the arraylake.

        Args:
            path: The path with the repo where the virtual HDF5 dataset should be created.
            hdf_uri: The path to the HDF5 file. Only `s3://` URIs are supported at the moment.
        """
        warnings.warn("Use add_virtual_netcdf instead", DeprecationWarning)
        self._synchronize(self._arepo.add_virtual_netcdf, path, hdf_uri)

    def add_virtual_netcdf(self, path: Path, netcdf_uri: str, **kwargs) -> None:
        """Add a virtual Netcdf dataset to the repo.

        Args:
            path: The path within the repo where the virtual dataset should be created.
            netcdf_uri: The path to the netCDF file. Only `s3://` URIs are supported at the moment.
              Both netCDF4 and netCDF3 files are supported.
            kwargs: Additional arguments to pass to the kerchunk
              [file format backend](https://fsspec.github.io/kerchunk/reference.html#file-format-backends).
              Do not pass `storage_options` or `inline_threshold`.
        """
        self._synchronize(self._arepo.add_virtual_netcdf, path, netcdf_uri, **kwargs)

    def add_virtual_zarr(self, path: Path, zarr_uri: str) -> None:
        """Add a virtual Zarr dataset to the repo.

        Args:
            path: The path within the repo where the virtual dataset should be created.
            zarr_uri: The path to the Zarr store. Only Zarr V2 stores and `s3://` URIs are supported at the moment.
        """
        self._synchronize(self._arepo.add_virtual_zarr, path, zarr_uri)

    def tree(self, prefix: str = "", depth: int = 10) -> Tree:
        """Display this repo's hierarchy as a Rich Tree

        Args:
            prefix: Path prefix
            depth: Maximum depth to descend into the hierarchy
        """
        return self._synchronize(self._arepo.tree, prefix=prefix, depth=depth)


class ArraylakeStore(StoreV3):
    """ArrayLake's Zarr Store interface

    This is an implementation of a [Zarr V3 Store](https://zarr-specs.readthedocs.io/en/latest/core/v3.0.html#id14).

    :::note
    This class is not intended to be constructed directly by users. Instead, use the `store` property on the `Repo` class.
    :::

    """

    def __init__(self, repo: Repo):
        self._repo = repo

    def list_prefix(self, prefix: str) -> list[str]:
        """List a prefix in the store

        Args:
            prefix : the path to list

        Returns:
            A list of document paths
        """
        return self._repo._wrap_async_iter(self._repo._arepo._list_prefix, prefix)

    def listdir(self, prefix: str) -> list[str]:
        """List a directory in the store

        Args:
            prefix: the path to list

        Returns:
            A list of document paths
        """
        return self._repo._wrap_async_iter(self._repo._arepo._list_dir, prefix)

    def getsize(self, prefix: str) -> int:
        data_prefix = data_root + prefix
        return self._repo._synchronize(self._repo._arepo._getsize, data_prefix)

    def rmdir(self, dir: str) -> None:
        dir = normalize_storage_path(dir)
        meta_dir = (meta_root + dir).rstrip("")
        self._repo._synchronize(self._repo._arepo._del_prefix, meta_dir)
        data_dir = (data_root + dir).rstrip("")
        self._repo._synchronize(self._repo._arepo._del_prefix, data_dir)

    def __getitem__(self, key) -> bytes:
        """Get a value

        Args:
            key: the path to get

        Returns:
            bytes (metadata or chunk)
        """
        self._validate_key(key)
        if is_chunk_key(key):
            return self._repo._get_chunk(key)
        elif is_meta_key(key):
            if key == "zarr.json":
                return ENTRY_POINT_METADATA
            doc = self._repo._get_doc(key)
            return json.dumps(doc).encode()
        else:  # pragma: no cover
            # don't expect to ever reach this
            raise KeyError(f"unexpected key: {key}")

    def getitems(self, keys, on_error="omit") -> Mapping[str, bytes]:
        """Get multiple items

        Args:
            keys: list of paths to get

        Returns:
            Mapping where keys are paths and values are bytes (metadata or chunks)
        """

        if on_error != "omit":  # pragma: no cover
            raise ValueError("Only support on_error='omit' for now")
        for key in keys:
            self._validate_key(key)
        meta_keys, chunk_keys = _sort_keys(keys)
        # TODO: can we have all of the needed queries in flight at the same time?
        # This two-step process is potentially inefficient
        chunk_docs = self._repo._get_chunks(chunk_keys) if chunk_keys else {}
        if "zarr.json" in meta_keys:
            meta_docs = {"zarr.json": ENTRY_POINT_METADATA}
            meta_keys.remove("zarr.json")
        else:
            meta_docs = {}
        if meta_keys:
            meta_docs.update({key: json.dumps(doc).encode() for key, doc in self._repo._get_docs(meta_keys).items()})

        # TODO: use this much better syntax once we drop Python 3.9
        # return meta_docs | chunk_docs
        return {**meta_docs, **chunk_docs}

    def __setitem__(self, key, value: bytes) -> None:
        """Set a value

        Args:
            key: the path to set

        Returns:
            bytes (metadata or chunk)
        """

        self._validate_key(key)
        if is_chunk_key(key):
            return self._repo._set_chunk(key, data=value)
        elif is_meta_key(key):
            if key == "zarr.json":
                raise KeyError("Cannot set zarr.json")
            doc = json.loads(value)
            return self._repo._set_doc(key, content=doc)
        else:
            raise KeyError(f"unexpected key: {key}")

    def setitems(self, items: Mapping[str, bytes]) -> None:
        """Get multiple items

        Args:
            keys : list of paths

        Returns:
            Mapping where keys are paths and values are bytes (metadata or chunks)
        """

        for key in items:
            self._validate_key(key)
        meta_keys, chunk_keys = _sort_keys(list(items))
        meta_docs = {key: json.loads(items[key]) for key in meta_keys}
        chunk_docs = {key: items[key] for key in chunk_keys}
        # TODO: can we have all of the needed queries in flight at the same time?
        if chunk_docs:
            self._repo._set_chunks(chunk_docs)
        if meta_docs:
            self._repo._set_docs(meta_docs)

    def __delitem__(self, key):
        """Delete a key.

        Args:
            key: path to delete
        """
        self._validate_key(key)
        if is_chunk_key(key):
            return self._repo._del_chunk(key)
        elif is_meta_key(key):
            return self._repo._del_doc(key)
        else:  # pragma: no cover
            raise KeyError(f"unexpected key: {key}")

    def delitems(self, keys) -> None:
        """Delete multiple keys

        Args:
            keys: list of paths to delete
        """

        for key in keys:
            self._validate_key(key)
        meta_keys, chunk_keys = _sort_keys(keys)
        # TODO: can we have all of the needed queries in flight at the same time?
        # This two-step process is potentially inefficient
        if chunk_keys:
            self._repo._del_chunks(chunk_keys)
        if meta_keys:
            self._repo._del_docs(meta_keys)

    def __contains__(self, key: str) -> bool:
        """check if key exists in store.

        Args:
            key: path to check
        """

        # fast path for a query that Zarr does over and over again
        if key == "zarr.json":
            return True
        try:
            self._validate_key(key)
        except ValueError:
            return False
        if is_chunk_key(key):
            return self._repo._chunk_exists(key)
        elif is_meta_key(key):
            return self._repo._doc_exists(key)
        else:  # pragma: no cover
            # this should never actually happen because a valid key will always resolve
            # to either a meta key or a chunk key
            return False

    def keys(self) -> List[str]:
        """Return a list of this store's keys"""

        return self.list_prefix("")

    def __iter__(self):
        """Iterate over this store's keys"""

        yield from self.keys()

    def erase_prefix(self, prefix):
        """Erase all keys with the given prefix."""
        self._repo._synchronize(self._repo._arepo._del_prefix, prefix)

    def __len__(self) -> int:
        """number of keys in this store"""
        # TODO: this is a very inefficient way to do this
        # we should consider more efficient implementations
        return len(self.keys())


@dataclass
class SessionStatus:
    """Holds the status of a session."""

    repo_name: str
    """Name of the repo"""
    session: SessionInfo
    """#SessionInfo object."""
    modified_paths: List[Tuple[Path, bool]]
    """List of modified paths and whether they were deleted."""

    def rich_output(self, console=None):
        from rich.console import Console
        from rich.panel import Panel

        if console is None:
            console = Console()

        console.print(f":ice: Using repo [bold]{self.repo_name}[/bold]")
        console.print(f":pager: Session [bold]{self.session['id']}[/bold] started at {self.session['start_time']}")
        if self.session["branch"]:
            console.print(f":herb: On branch [bold]{self.session['branch']}[/bold]")
        else:
            console.print(":shrug: Not on a branch")

        changes = []
        for path, deleted in self.modified_paths:
            if deleted:
                changes.append(f":cross_mark: [red]{path}[/red]")
            else:
                changes.append(f":pencil: [green]{path}[/green]")

        if changes:
            console.print(Panel("\n".join(changes), title="paths modified in session", title_align="left", expand=False, padding=(1, 2)))
        else:
            console.print("No changes in current session.")

    def _repr_html_(self):
        html = "<p>\n"
        html += f"🧊 Using repo <b>{escape(self.repo_name)}</b><br />\n"
        html += f"📟 Session <b>{escape(self.session['id'])}</b> started at <i>{escape(self.session['start_time'].isoformat())}</i><br />\n"
        if self.session["branch"]:
            html += f"🌿 On branch <b>{escape(self.session['branch'])}</b><br />\n"
        else:
            html += "🤷 Not on a branch<br />\n"
        html += "</p>\n"

        changes = []
        for path, deleted in self.modified_paths:
            if deleted:
                changes.append(f"""  <li style="color: red; list-style: none;">❌ {escape(path)}</li>\n""")
            else:
                changes.append(f"""  <li style="color: green; list-style: none;">📝 {escape(path)}</li>\n""")

        if changes:
            html += """<div style="border: 1px dashed gray; border-radius: 5px; padding: 1em;">\n"""
            html += """ <h3>paths modified in session</h3>\n <ul>\n"""
            html += "".join(changes)
            html += """ </ul>\n</div>"""
        else:
            html += "<p>No changes in current session</p>\n"
        return html

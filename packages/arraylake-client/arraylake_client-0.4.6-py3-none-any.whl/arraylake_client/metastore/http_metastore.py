from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass, field
from typing import (
    Any,
    AsyncGenerator,
    Generator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
)

from cachetools import LRUCache

from arraylake_client.api_utils import (
    ArraylakeHttpClient,
    gather_and_check_for_exceptions,
    handle_response,
)
from arraylake_client.metastore.abc import Metastore, MetastoreDatabase
from arraylake_client.types import (
    Branch,
    BranchName,
    BulkCreateDocBody,
    CollectionName,
    Commit,
    CommitID,
    DocResponse,
    DocSessionsResponse,
    NewCommit,
    Path,
    PathSizeResponse,
    PyObjectId,
    RepoCreateBody,
    SessionID,
    SessionPathsResponse,
    T,
    Tag,
    Tree,
    UpdateBranchBody,
)

BATCH_SIZE = int(os.environ.get("ARRAYLAKE_CLIENT_BATCH_SIZE", 20))


def chunks(seq: Sequence[T], size: int) -> Generator[Sequence[T], None, None]:
    return (seq[pos : (pos + size)] for pos in range(0, len(seq), size))  # noqa: E203


@dataclass
class HttpMetastoreConfig:
    """Encapsulates the configuration for the HttpMetastore"""

    api_service_url: str
    org: str
    token: str = field(default=None, repr=False)  # machine token. id/access/refresh tokens are managed by CustomOauth
    auth_org: str = None


class HttpMetastore(ArraylakeHttpClient, Metastore):
    """ArrayLake's HTTP Metastore

    This metastore connects to ArrayLake over HTTP

    args:
        config: config for the metastore

    :::note
    Authenticated calls require an Authorization header. Run ``arraylake auth login`` to login before using this metastore.
    :::
    """

    _config: HttpMetastoreConfig

    def __init__(self, config: HttpMetastoreConfig):
        super().__init__(config.api_service_url, token=config.token, hint=config.auth_org)

        self._config = config
        self.api_url = config.api_service_url

    async def ping(self) -> dict:
        async with self:
            response = await self._request("GET", "user")
        handle_response(response)

        return dict(**response.json())

    async def list_databases(self) -> Sequence[dict]:
        async with self:
            response = await self._request("GET", f"/orgs/{self._config.org}/repos")
        handle_response(response)
        # TODO: use a response model for stricter typing here
        return [repo for repo in response.json()]

    async def create_database(self, name: str):
        body = RepoCreateBody(name=name)
        async with self:
            response = await self._request("POST", f"/orgs/{self._config.org}/repos", json=body.dict())
            handle_response(response)
        # TODO: we shouldn't need to make another request to get the repo (in open_database), the response body has everything we need
        # either stop shipping the repo body back in the POST request or bypass the GET request in open_database
        return await self.open_database(name)

    async def open_database(self, name: str) -> HttpMetastoreDatabase:
        # verify repo actually exists
        async with self:
            response = await self._request("GET", f"/repos/{self._config.org}/{name}")
            handle_response(response)  # raise error on 404
        db_config = HttpMetastoreDatabaseConfig(
            http_metastore_config=self._config,
            repo=name,
        )
        return HttpMetastoreDatabase(db_config)

    async def delete_database(self, name: str, *, imsure: bool = False, imreallysure: bool = False) -> None:
        if not (imsure and imreallysure):
            raise ValueError("Don't do this unless you're really sure. Once the database has been deleted, it's gone forever.")

        async with self:
            response = await self._request("DELETE", f"/orgs/{self._config.org}/{name}")
        handle_response(response)


@dataclass
class HttpMetastoreDatabaseConfig:
    """Encapsulates the configuration for an HttpMetastoreDatabase"""

    http_metastore_config: HttpMetastoreConfig
    repo: str


class HttpMetastoreDatabase(ArraylakeHttpClient, MetastoreDatabase):
    _config: HttpMetastoreDatabaseConfig
    _doc_cache: LRUCache[Tuple[CollectionName, PyObjectId], DocResponse]

    def __init__(self, config: HttpMetastoreDatabaseConfig):
        """ArrayLake's HTTP Metastore Database

        This metastore database connects to ArrayLake over HTTP

        args:
            config: config for the metastore database

        :::note
        Authenticated calls require an Authorization header. Run ``arraylake auth login`` to login before using this metastore.
        :::
        """
        super().__init__(
            config.http_metastore_config.api_service_url,
            token=config.http_metastore_config.token,
            hint=config.http_metastore_config.auth_org,
        )

        self._config = config
        self._setup()

    def _setup(self):
        self._repo_path = f"/repos/{self._config.http_metastore_config.org}/{self._config.repo}"
        self._doc_cache = LRUCache(maxsize=10000)

    def __getstate__(self):
        return self._config

    def __setstate__(self, state):
        super().__init__(
            state.http_metastore_config.api_service_url, token=state.http_metastore_config.token, hint=state.http_metastore_config.auth_org
        )
        self._config = state
        self._setup()

    def __repr__(self):
        status = "OPEN" if self._OPEN else "CLOSED"
        full_name = f"{self._config.http_metastore_config.org}/{self._config.repo}"
        return f"<arraylake_client.http_metastore.HttpMetastoreDatabase repo_name='{full_name}' status={status}>"

    async def get_commits(self) -> tuple[Commit, ...]:
        response = await self._request("GET", f"{self._repo_path}/commits")
        handle_response(response)

        return tuple(Commit(**doc) for doc in response.json())

    async def get_tags(self):
        response = await self._request("GET", f"{self._repo_path}/tags")
        handle_response(response)

        return tuple(Tag(**doc) for doc in response.json())

    async def get_branches(self):
        response = await self._request("GET", f"{self._repo_path}/branches")
        handle_response(response)

        return tuple(Branch(**doc) for doc in response.json())

    async def get_refs(self) -> tuple[tuple[Tag, ...], tuple[Branch, ...]]:
        return await gather_and_check_for_exceptions(self.get_tags(), self.get_branches())

    async def new_commit(self, commit_info: NewCommit) -> CommitID:
        response = await self._request("PUT", f"{self._repo_path}/commits", content=commit_info.json())
        handle_response(response)

        return PyObjectId(response.json()["_id"])

    async def rebase(self, commit_id: CommitID, upstream_branch: BranchName) -> CommitID:
        body = {"commit_id": str(commit_id) if commit_id else None, "branch_name": upstream_branch}
        response = await self._request("POST", f"{self._repo_path}/rebase", params=body)
        handle_response(response)
        return CommitID(response.json()["commit_id"])

    async def update_branch(
        self, branch: BranchName, *, base_commit: Optional[CommitID], new_commit: CommitID, new_branch: bool = False
    ) -> None:
        body = UpdateBranchBody(branch=branch, new_commit=new_commit, base_commit=base_commit, new_branch=new_branch)
        response = await self._request("PUT", f"{self._repo_path}/branches", content=body.json())
        handle_response(response)

    async def get_all_sessions_for_path(self, path: Path, *, collection: CollectionName) -> AsyncGenerator[DocSessionsResponse, None]:
        # keys are sids, values are deleted or not
        response = await self._request("GET", f"{self._repo_path}/sessions/{collection}/{path}")
        handle_response(response)

        for doc in response.json():  # TODO: stream/paginate here
            yield DocSessionsResponse(**doc)

    async def get_all_paths_for_session(
        self, session_id: SessionID, *, collection: CollectionName, limit: int = 0
    ) -> AsyncGenerator[SessionPathsResponse, None]:
        """Get all paths that have been modified in the current session."""

        # /repos/{org}/{repo}/sessions/{collection}/{session_id}
        response = await self._request("GET", f"{self._repo_path}/modified_paths/{collection}/{session_id}", params={"limit": limit})
        handle_response(response)

        for doc in response.json():  # TODO: stream/paginate here
            yield SessionPathsResponse(**doc)

    async def _add_docs(self, docs: Sequence[BulkCreateDocBody], collection: CollectionName, session_id: SessionID) -> None:
        """Submits a list of docs to the server to be added in bulk."""
        params = {"session_id": session_id}
        response = await self._request(
            "PUT", f"{self._repo_path}/contents/{collection}/_bulk_set", json=[d.dict() for d in docs], params=params
        )
        handle_response(response)

    async def add_docs(self, items: Mapping[Path, Mapping[str, Any]], *, collection: CollectionName, session_id: SessionID) -> None:
        docs = [BulkCreateDocBody(session_id=session_id, content=content, path=path) for path, content in items.items()]
        await gather_and_check_for_exceptions(*[self._add_docs(batch, collection, session_id) for batch in chunks(docs, BATCH_SIZE)])

    async def del_docs(self, paths: Sequence[Path], *, collection: CollectionName, session_id: SessionID) -> None:
        params = {"session_id": session_id}
        response = await self._request("PUT", f"{self._repo_path}/contents/{collection}/_bulk_delete", json=paths, params=params)
        handle_response(response)

    async def _get_docs(
        self, paths: Sequence[Path], collection: CollectionName, session_id: SessionID, commit_id: Optional[CommitID]
    ) -> List[DocResponse]:
        """Submits a list of paths to the server to be retrieved in bulk."""
        params = {"session_id": session_id, "commit_id": commit_id}
        response = await self._request("POST", f"{self._repo_path}/contents/{collection}/_bulk_get", json=paths, params=params)
        handle_response(response)
        return [DocResponse(**item) for item in response.json()]

    async def get_docs(
        self, paths: Sequence[Path], *, collection: CollectionName, session_id: SessionID, commit_id: Optional[CommitID] = None
    ) -> AsyncGenerator[DocResponse, None]:
        # remove dupes from request; is there a cheaper way of doing this? seems like a lot of overhead for every call
        paths = list(set(paths))

        results = await asyncio.gather(
            *(
                self._get_docs(paths_batch, collection, session_id=session_id, commit_id=commit_id)
                for paths_batch in chunks(paths, BATCH_SIZE)
            )
        )

        for result in results:
            for doc in result:
                yield doc

    # TODO: could make list cacheable if we can bound it on a specific commit
    async def list(
        self,
        prefix: str,
        *,
        collection: CollectionName,
        session_id: SessionID,
        commit_id: Optional[CommitID] = None,
        all_subdirs: bool = False,
        # This feature has experimental support, denoted by the leading underscore
        _jmespath_filter_expression: Optional[str] = None,
    ) -> AsyncGenerator[Path, None]:
        # TODO: implement pagination for this API call
        response = await self._request(
            "GET",
            f"{self._repo_path}/contents/{collection}/",
            params={
                "prefix": prefix,
                "session_id": session_id,
                "commit_id": commit_id,
                "all_subdirs": all_subdirs,
                "_jmespath_filter_expression": _jmespath_filter_expression,
            },
        )
        handle_response(response)

        for path in response.json():
            yield Path(path)

    async def getsize(
        self,
        prefix: str,
        *,
        session_id: SessionID,
        commit_id: Optional[CommitID] = None,
    ) -> PathSizeResponse:
        response = await self._request(
            "GET",
            f"{self._repo_path}/size/",
            params={"prefix": prefix, "session_id": session_id, "commit_id": commit_id},
        )
        handle_response(response)
        return PathSizeResponse(**response.json())

    async def del_prefix(
        self,
        prefix: str,
        *,
        collection: CollectionName,
        session_id: SessionID,
        commit_id: Optional[CommitID] = None,
    ) -> None:
        response = await self._request(
            "DELETE",
            f"{self._repo_path}/contents/{collection}/{prefix}",
            params={"session_id": session_id, "commit_id": commit_id},
        )
        handle_response(response)

    async def tree(
        self,
        prefix: str,
        *,
        session_id: SessionID,
        commit_id: Optional[CommitID] = None,
        depth: int = 10,
    ) -> Tree:
        response = await self._request(
            "GET",
            f"{self._repo_path}/tree",
            params={"prefix": prefix, "session_id": session_id, "commit_id": commit_id, "depth": depth},
        )
        handle_response(response)
        return Tree(**response.json())

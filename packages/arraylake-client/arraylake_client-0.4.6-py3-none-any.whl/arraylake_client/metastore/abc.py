from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Mapping, Optional, Sequence

from ..types import (
    Branch,
    BranchName,
    CollectionName,
    Commit,
    CommitID,
    DocResponse,
    NewCommit,
    Path,
    PathSizeResponse,
    SessionID,
    SessionPathsResponse,
    Tag,
    Tree,
)


class Metastore(ABC):  # pragma: no cover
    @abstractmethod
    async def ping(self) -> dict:
        """Verify that the metastore is accessible and responsive to the client."""
        ...

    @abstractmethod
    async def list_databases(self) -> Sequence[dict]:
        ...

    @abstractmethod
    async def create_database(self, name: str) -> MetastoreDatabase:
        """Create a new metastore database.

        Parameters
        ----------
        name : str
            Name of repo

        Returns
        -------
        MetastoreDatabase
        """
        ...

    @abstractmethod
    async def open_database(self, name: str) -> MetastoreDatabase:
        """Open an existing metastore database.

        Parameters
        ----------
        name : str
            Name of repo

        Returns
        -------
        MetastoreDatabase
        """
        ...

    @abstractmethod
    async def delete_database(self, name: str, *, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete an existing metastore database.

        Parameters
        ----------
        name : str
            Name of repo
        imsure, imreallsure : bool
            Confirm permanent deletion.
        """
        ...


class MetastoreDatabase(ABC):  # pragma: no cover
    @abstractmethod
    async def __aenter__(self):
        """Enter async context"""
        ...

    @abstractmethod
    async def __aexit__(self, *args, **kwargs):
        """Exit async context"""
        ...

    async def ping(self):
        """Ping the MetastoreDatabase to check connectivity"""
        ...

    @abstractmethod
    async def get_commits(self) -> tuple[Commit, ...]:
        """Get the complete commit history for the repo.

        Returns
        -------
        tuple
            Tuple of Commit objects
        """
        ...

    @abstractmethod
    async def get_tags(self) -> tuple[Tag, ...]:
        """Get all the tags for the repo.

        Returns
        -------
        tuple
         Tuple of Tag objects
        """
        ...

    @abstractmethod
    async def get_branches(self) -> tuple[Branch, ...]:
        """Get all the branches for the repo.

        Returns
        -------
        tuple
            Tuple of Branch objects
        """
        ...

    @abstractmethod
    async def get_refs(self) -> tuple[tuple[Tag, ...], tuple[Branch, ...]]:
        """Get all tags and branches and their corresponding commits.

        Returns
        -------
        tuple
            Tags and Branches
        """
        ...

    @abstractmethod
    async def new_commit(self, commit_info: NewCommit) -> CommitID:
        """Create and return a new commit for a session.

        Returns
        -------
        CommitID
        """
        ...

    @abstractmethod
    async def rebase(self, commit_id: CommitID, upstream_branch: BranchName) -> CommitID:
        """Determine if a commit_id can cleanly be updated to a target branch HEAD.

        Clean update means that there are no conflicting path updates in intermediate commits between
        commit_id and the HEAD commit of the upstream_branch. If the update can be performed cleanly,
        return the target branch commit_id to the caller, else raise an exception.

        Note: This is a read-only operations, it should not create or modify commits or branch states.

        Returns
        -------
        CommitID

        Raises
        ------
        ValueError
            if clean update is not possible
        """
        ...

    @abstractmethod
    async def update_branch(
        self, branch: BranchName, *, base_commit: Optional[CommitID], new_commit: CommitID, new_branch: bool = False
    ) -> None:
        """Update a branch reference in an atomic transaction.

        Parameters
        ----------
        branch : str
            Name of branch to update
        base_commit : CommitID, optional
            Parent commit ID, None signals no parent
        new_commit : CommitID
            New commit ID
        new_branch : bool, default=False
            If True, create a new branch
        """
        ...

    # Confusingly, these generator methods cannot be declared async for typing to work properly
    # https://stackoverflow.com/a/56947440
    # https://github.com/python/mypy/issues/5385#issuecomment-407281656

    @abstractmethod
    def get_all_paths_for_session(
        self, session_id: SessionID, *, collection: CollectionName, limit: int = 0
    ) -> AsyncGenerator[SessionPathsResponse, None]:
        """Get all paths that have been modified in the current session."""
        ...

    @abstractmethod
    async def add_docs(self, items: Mapping[Path, Mapping[str, Any]], *, collection: CollectionName, session_id: SessionID) -> None:
        """Add documents to the specified collection.

        Parameters
        ----------
        items : dict
            Mapping where keys are paths and values are documents in the form of dictionaries.
        collection : str
        """
        ...

    @abstractmethod
    async def del_docs(self, paths: Sequence[Path], *, collection: CollectionName, session_id: SessionID) -> None:
        """Remove documents from the specified collection.

        Parameters
        ----------
        paths : sequence
            Sequence of paths to delete
        collection : str
        """
        ...

    @abstractmethod
    async def del_prefix(self, prefix: Path, *, collection: CollectionName, session_id: SessionID) -> None:
        """Remove documents matching a prefix from the specified collection.

        Parameters
        ----------
        prefix : sequence
            Prefix to delete
        collection : str
        """
        ...

    @abstractmethod
    def get_docs(
        self, paths: Sequence[Path], *, collection: CollectionName, session_id: SessionID, commit_id: Optional[CommitID] = None
    ) -> AsyncGenerator[DocResponse, None]:
        """Fetch documents from the specified collection.

        Parameters
        ----------
        paths : sequence
            Sequence of paths to fetch
        collection : str
            Which collection to search
        session_id: SessionID
            The the active session ID
        commit_id: CommitID, optional
            The base commit for the session

        Yields
        ------
        DocResponse
        """
        ...

    @abstractmethod
    def list(
        self,
        prefix: str,
        *,
        collection: CollectionName,
        session_id: SessionID,
        commit_id: Optional[CommitID] = None,
        all_subdirs: bool = False,
    ) -> AsyncGenerator[Path, None]:
        """List documents from the specified collection matching a prefix.

        Parameters
        ----------
        prefix : str
            Path prefix to match
        collection : str
            Which collection to search
        session_id: SessionID
            The the active session ID
        commit_id: CommitID, optional
            The base commit for the session
        all_subdirs : bool, default=False
            If True, recursively include all sub directories

        Yields
        ------
        ListResponse
        """
        ...

    async def getsize(
        self,
        prefix: str,
        *,
        session_id: SessionID,
        commit_id: Optional[CommitID] = None,
    ) -> PathSizeResponse:
        """Get the total size of documents in a collection matching a prefix.

        Parameters
        ----------
        prefix : str
            The prefix to list documents for
        session_id: SessionID
            The the active session ID
        commit_id: CommitID, optional
            The base commit for the session
        all_subdirs : bool, default=False
            If True, recursively include all sub directories

        Yields
        ------
        response
            Number and size of documents (only includes chunks, not metadata)
        """
        ...

    @abstractmethod
    async def tree(
        self,
        prefix: str,
        *,
        session_id: SessionID,
        commit_id: Optional[CommitID] = None,
        depth: int = 10,
    ) -> Tree:
        """Create a nested dictionary representing this metastore's hierarchy.

        Parameters
        ----------
        prefix : str
            Path prefix to match
        session_id: SessionID
            The the active session ID
        commit_id: CommitID, optional
            The base commit for the session

        Returns
        -------
        Tree
        """
        ...

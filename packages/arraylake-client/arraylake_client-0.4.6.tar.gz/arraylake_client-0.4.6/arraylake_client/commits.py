from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Mapping, Optional, Sequence, Tuple, TypeVar

from bson.errors import InvalidId

from arraylake_client.exceptions import CommitNotFoundException, DocumentNotFoundError
from arraylake_client.types import (
    Branch,
    BranchName,
    Commit,
    CommitHistory,
    CommitID,
    DocResponse,
    DocSessionsResponse,
    SessionID,
    Tag,
    TagName,
)

T = TypeVar("T", DocResponse, DocSessionsResponse)


# this function is important: it contains the logic to determine which document to return for an active session
def find_doc(
    session_map: Mapping[SessionID, T],
    current_session_id: SessionID,
    commit_tree: Optional[CommitTree],
) -> T:
    """Convenience function to find the latest version of a document given an active session"""
    if current_session_id in session_map:
        session_id = current_session_id
    else:
        if commit_tree is None:
            raise DocumentNotFoundError("Session has no base commit.")
        for commit, session_id in commit_tree.walk():
            if session_id in session_map:
                break
        else:
            # iteration of the commit tree ended without finding a matching session
            raise DocumentNotFoundError("Document has never been written.")
    if session_map[session_id].deleted:
        raise DocumentNotFoundError("Document was deleted")
    return session_map[session_id]


@dataclass()
class CommitTree:
    """Lightweight structure to retrieve history for a given commit.

    Note: this structure is a little unnecessary and isn't a tree as the name would suggest.
    It is simply a holder for a a collection of commits and presents a single sequential history
    for the provided commit_id via `walk()`. It could be simplified to a utility function, but is maintained
    due to it's pervasive usage throughout the codebase.
    """

    commit_id: CommitID
    all_commits: Mapping[CommitID, Commit]

    def walk(self) -> CommitHistory:
        "Construct the lineage for the provided commit_id over provided commits"
        try:
            commit = self.all_commits[self.commit_id]
        except KeyError:
            raise CommitNotFoundException(f"Error retrieving commit id {self.commit_id}, root does not exist in provided commits")
        while commit:
            yield (commit.id, commit.session_id)
            if commit.parent_commit:
                try:
                    commit = self.all_commits[commit.parent_commit]
                except KeyError:
                    raise CommitNotFoundException(
                        f"Error retrieving commit id {commit.parent_commit}, parent does not exist in provided commits"
                    )
            else:
                commit = None


class CommitData:
    """Data structure containing all the commit information for a session."""

    commits: Mapping[CommitID, Commit]
    """Mapping of commit ID to full Commit object"""
    tags: Mapping[TagName, CommitID]
    """Mapping of tag name to Commit ID"""
    branches: Mapping[BranchName, CommitID]
    """Mapping of branch name to Commit ID"""

    def __init__(self, commit_list: Sequence[Commit], tag_list: Sequence[Tag], branch_list=Sequence[Branch]):
        self.commits = {commit.id: commit for commit in commit_list}
        self.tags = {tag.id: tag.commit_id for tag in tag_list}
        self.branches = {branch.id: branch.commit_id for branch in branch_list}

    def get_commit_tree(self, commit_id: CommitID) -> CommitTree:
        """Get the commit tree for a given commit ID.

        Args:
            commit_id: the commit ID to start from

        Returns:
            CommitTree
        """
        return CommitTree(commit_id, self.commits)

    def get_ref(self, ref: str) -> Tuple[CommitID, BranchName]:
        """Get the commit ID for a given commit, tag or branch name.

        Args:
            ref: commit_id, tag or branch name

        Returns:
            CommitID, BranchName
        """

        # the goal of the function is to assign these
        commit = None  # type: Optional[CommitID]
        branch = None  # type: Optional[BranchName]

        if ref in self.branches:
            branch = BranchName(ref)
            commit = self.branches[branch]
        elif ref in self.tags:
            tag = TagName(ref)
            commit = self.tags[tag]
        else:
            try:
                commit = CommitID(ref)
            except InvalidId:
                # commit won't be found and will eventually raise an error
                pass

            if commit in self.commits:
                pass
            else:
                if len(self.commits) == 0:
                    # special case, no commits to the repo yet
                    commit = None
                    branch = BranchName("main")
                else:
                    raise ValueError(f"Ref `{ref}` was not found in branches, tags, or commits")
        return commit, branch


@dataclass(frozen=True)
class CommitLog:
    """Used to display commit history to the user."""

    repo_name: str
    """Name of the repo"""
    commit_id: CommitID
    """Current commit ID"""
    commit_data: CommitData
    """Repo commit data"""

    def __iter__(self):
        """Iterate through commit history, newest to oldest.

        Yields:
            Commit
        """
        if self.commit_id is None:
            return
        tree = CommitTree(self.commit_id, self.commit_data.commits)
        for commit_id, _ in tree.walk():
            yield self.commit_data.commits[commit_id]

    def __len__(self):
        """Number of commits in the log."""
        return len([c for c in self])

    def rich_output(self, console=None):
        from rich.console import Console
        from rich.padding import Padding

        if console is None:
            console = Console()

        for commit in self:
            console.print(f"[yellow]commit [bold]{commit.id}[/bold] [/yellow]")
            console.print(f"Author: {commit.author_entry()}")
            console.print(f"Date:   {commit.commit_time}")
            console.print(Padding(commit.message, (1, 4)))

    def _repr_html_(self):
        html = """<ul style="list-style-type: none; margin: 0; padding: 0;">\n"""

        for commit in self:
            html += """ <li>\n  <table style="border: 1px dashed grey">\n"""
            html += f"""   <tr><td style="text-align:right">Commit ID</td><td style="text-align:left"><b>{escape(str(commit.id))}</b></td></tr>\n"""  # noqa: E501
            html += f"""   <tr><td style="text-align:right">Author</td><td style="text-align:left">{escape(commit.author_entry())}</td></tr>\n"""  # noqa: E501
            html += f"""   <tr><td style="text-align:right">Date</td><td style="text-align:left">{escape(commit.commit_time.isoformat())}</td></tr>\n"""  # noqa: E501
            html += "  </table>\n"
            message = escape(commit.message).replace("\n", "<br />")
            html += f"""  <p style="padding: 1em 3em;">{message}</p>\n"""
            html += " </li>\n"
        html += "</ul>\n"

        return html

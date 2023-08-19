"""
The Client module contains the main classes used to interact with the Arraylake service.
For asyncio interaction, use the #AsyncClient. For regular, non-async interaction, use the #Client.

**Example usage:**

```python
from arraylake_client import Client
client = Client()
repo = client.get_repo("my-org/my-repo")
```
"""

import re
from dataclasses import dataclass, field
from typing import Optional, Sequence, Tuple

from arraylake_client.async_utils import cached_portal
from arraylake_client.chunkstore import chunkstore
from arraylake_client.config import config
from arraylake_client.log_util import get_logger
from arraylake_client.metastore import HttpMetastore, HttpMetastoreConfig
from arraylake_client.repo import AsyncRepo, Repo
from arraylake_client.types import Author

logger = get_logger(__name__)

_VALID_NAME = r"(\w[\w\.\-_]+)"


def _parse_org_and_repo(org_and_repo: str) -> Tuple[str, str]:
    expr = f"{_VALID_NAME}/{_VALID_NAME}"
    res = re.fullmatch(expr, org_and_repo)
    if not res:
        raise ValueError(f"Not a valid repo identifier: `{org_and_repo}`. " "Should have the form `{ORG}/{REPO}`.")
    org, repo_name = res.groups()
    return org, repo_name


def _validate_org(org_name: str):
    if not re.fullmatch(_VALID_NAME, org_name):
        raise ValueError(f"Invalid org name: `{org_name}`.")


@dataclass
class AsyncClient:
    """Asyncio Client for interacting with ArrayLake

    Args:
        service_uri (str): [Optional] The service URI to target.
        token (str): [Optional] API token for service account authentication.
    """

    service_uri: Optional[str] = None
    token: Optional[str] = field(default=None, repr=False)
    auth_org: Optional[str] = None

    def __post_init__(self):
        if self.token is not None and not self.token.startswith("ema_"):
            raise ValueError("Invalid token provided. Tokens must start with ema_")
        if self.service_uri is None:
            self.service_uri = config.get("service.uri")
        self.auth_org = self.auth_org or config.get("user.org", None)

    # TODO: replace the return type with a stricted type around repo listing object
    async def list_repos(self, org: str) -> Sequence[dict]:
        """List all repositories for the specified org

        Args:
            org: Name of the org
        """

        _validate_org(org)
        mstore = HttpMetastore(HttpMetastoreConfig(self.service_uri, org, self.token, self.auth_org))
        repo_names = await mstore.list_databases()
        return repo_names

    async def get_repo(self, name: str) -> AsyncRepo:
        """Get a repo by name

        Args:
            name: Full name of the repo (of the form {ORG}/{REPO})
        """

        org, repo_name = _parse_org_and_repo(name)
        mstore = HttpMetastore(HttpMetastoreConfig(self.service_uri, org, self.token, self.auth_org))
        db = await mstore.open_database(repo_name)

        s3_uri = config.get("chunkstore.uri")
        client_kws = config.get("s3", {})
        cstore = chunkstore(s3_uri, **client_kws)

        async with mstore:
            user = await mstore.get_user()

        author: Author = user.as_author()
        return AsyncRepo(db, cstore, name, author)

    async def get_or_create_repo(self, name: str) -> AsyncRepo:
        """Get a repo by name. Create the repo if it doesn't already exist.

        Args:
            name: Full name of the repo (of the form {ORG}/{REPO})
        """
        org, repo_name = _parse_org_and_repo(name)
        all_repos = [result["name"] for result in await self.list_repos(org)]
        if repo_name in all_repos:
            return await self.get_repo(name)
        else:
            return await self.create_repo(name)

    async def create_repo(self, name: str) -> AsyncRepo:
        """Create a new repo

        Args:
            name: Full name of the repo to create (of the form {ORG}/{REPO})
        """

        org, repo_name = _parse_org_and_repo(name)
        mstore = HttpMetastore(HttpMetastoreConfig(self.service_uri, org, self.token, self.auth_org))

        s3_uri = config.get("chunkstore.uri")
        client_kws = config.get("s3", {})
        cstore = chunkstore(s3_uri, **client_kws)

        async with mstore:
            user = await mstore.get_user()
        author: Author = user.as_author()

        # important: call create_database after setting up the metastore and chunkstore objects
        db = await mstore.create_database(repo_name)
        arepo = AsyncRepo(db, cstore, name, author)
        return arepo

    async def delete_repo(self, name: str, *, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete a repo

        Args:
            name: Full name of the repo to delete (of the form {ORG}/{REPO})
        """

        org, repo_name = _parse_org_and_repo(name)
        mstore = HttpMetastore(HttpMetastoreConfig(self.service_uri, org, self.token, self.auth_org))
        await mstore.delete_database(repo_name, imsure=imsure, imreallysure=imreallysure)


# This version of synchronize is different from the one in repo.py.
# That version stores the global portal on the Repo object itself.
# This version also uses the global portal but enters and exits the context for each call.
# This is undoubtedly slower (a new thread is started and stopped on each call.)
# But it is also simpler, with no need to explicitly .close() the client.
def _synchronize(func, *args, **kwargs):
    # we have to wrap the method because portal.call doesn't support kwargs
    def wrapped():
        return func(*args, **kwargs)

    with cached_portal.acquire() as portal:
        result = portal.call(wrapped)
    return result


@dataclass
class Client:
    """Client for interacting with ArrayLake.

    Args:
        service_uri (str): [Optional] The service URI to target.
        token (str): [Optional] API token for service account authentication.
    """

    service_uri: Optional[str] = None
    token: Optional[str] = field(default=None, repr=False)
    auth_org: Optional[str] = None

    def __post_init__(self):
        if self.service_uri is None:
            self.service_uri = config.get("service.uri")
        self.auth_org = self.auth_org or config.get("user.org", None)

        self.aclient = AsyncClient(self.service_uri, token=self.token, auth_org=self.auth_org)

    def list_repos(self, org: str) -> Sequence[str]:
        """List all repositories for the specified org

        Args:
            org: Name of the org
        """

        repo_list = _synchronize(self.aclient.list_repos, org)
        return repo_list

    def get_repo(self, name: str) -> Repo:
        """Get a repo by name

        Args:
            name: Full name of the repo (of the form {ORG}/{REPO})
        """

        arepo = _synchronize(self.aclient.get_repo, name)
        return Repo(arepo)

    def get_or_create_repo(self, name: str) -> Repo:
        """Get a repo by name. Create the repo if it doesn't already exist.

        Args:
            name: Full name of the repo (of the form {ORG}/{REPO})
        """
        arepo = _synchronize(self.aclient.get_or_create_repo, name)
        return Repo(arepo)

    def create_repo(self, name: str) -> Repo:
        """Create a new repo

        Args:
            name: Full name of the repo to create (of the form {ORG}/{REPO})
        """

        arepo = _synchronize(self.aclient.create_repo, name)
        return Repo(arepo)

    def delete_repo(self, name: str, *, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete a repo

        Args:
            name: Full name of the repo to delete (of the form {ORG}/{REPO})
        """

        return _synchronize(self.aclient.delete_repo, name, imsure=imsure, imreallysure=imreallysure)

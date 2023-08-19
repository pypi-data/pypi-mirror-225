import pathlib
from json import JSONDecodeError
from typing import List, Optional, Union

import httpx
from pydantic import ValidationError

from arraylake_client.config import config
from arraylake_client.types import OauthTokens, OauthTokensResponse


class AuthException(ValueError):
    pass


class TokenHandler:
    """
    Class used to handle OAuth2
    """

    token_path: pathlib.Path
    tokens: Optional[OauthTokens]

    def __init__(
        self,
        api_endpoint: str = "https://api.earthmover.io",
        hint: str = None,
        scopes: List[str] = ["email", "openid", "profile"],
        raise_if_not_logged_in: bool = False,
    ):
        self.api_endpoint = api_endpoint
        self.scopes = scopes
        self.hint = hint

        self.token_path = pathlib.Path(config.get("service.token_path", None) or "~/.arraylake/token.json").expanduser()
        self.default_headers = {"accept": "application/vnd.earthmover+json"}

        # get cached tokens
        self.tokens = None
        try:
            self.tokens = OauthTokens.parse_file(self.token_path)
        except (ValidationError, JSONDecodeError):
            if raise_if_not_logged_in:
                raise AuthException("Found malformed auth tokens, logout and log back in")
        except FileNotFoundError:
            if raise_if_not_logged_in:
                raise AuthException("Not logged in, please log in with `arraylake auth login`")

    async def get_authorize_url(self) -> str:
        body = {"scopes": self.scopes}
        async with httpx.AsyncClient() as client:
            params = {"hint": self.hint} if self.hint else {}
            response = await client.post(f"{self.api_endpoint}/login", json=body, headers=self.default_headers, params=params)
        if response.status_code != httpx.codes.OK:
            raise AuthException("failed to get authorization url")

        return response.json()["url"]

    async def get_token(self, code: str):
        params = {"code": code}
        if self.hint:
            params["hint"] = self.hint
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_endpoint}/token", params=params, headers=self.default_headers)
        if response.status_code != httpx.codes.OK:
            raise AuthException("unable to get token")
        new_token_data = OauthTokens.parse_obj(response.json())
        self.update(new_token_data)

    async def refresh_token(self):
        params = {"token": self.tokens.refresh_token.get_secret_value()}
        if self.hint:
            params["hint"] = self.hint
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_endpoint}/refresh_token", params=params, headers=self.default_headers)
        if response.status_code == httpx.codes.OK:
            # a refresh token is persisted over time
            # performing a fresh yields a new id + access token
            # perform an update with the new values, but maintain
            # the refresh token
            new_token_data = OauthTokensResponse.parse_obj(response.json())
            self.update(new_token_data)
        else:
            raise AuthException("unable to refresh token")

    def update(self, new_token_data: Union[OauthTokens, dict]):
        if self.tokens is None:
            self.tokens = OauthTokens.parse_obj(new_token_data)
        else:
            if isinstance(new_token_data, OauthTokens):
                # converting to a dict allows us to update only non-default fields
                new_token_data = new_token_data.dict()

            # a little work to make sure we write back
            # an OauthTokens object with the correct value types
            staged_token_data = self.tokens.dict()
            staged_token_data.update(new_token_data)
            self.tokens = OauthTokens.parse_obj(staged_token_data)
        self.cache()

    def cache(self):
        if not self.tokens:
            raise ValueError("Error saving tokens, no tokens to cache")
        self.token_path.parent.mkdir(exist_ok=True)
        with self.token_path.open(mode="w") as fp:
            fp.write(self.tokens.json(exclude_unset=True))
        self.token_path.chmod(0o100600)  # -rw-------

    def get_logout_url(self) -> str:
        endpoint = f"{self.api_endpoint}/logout"
        if self.hint:
            return f"{self.api_endpoint}/logout?hint={self.hint}"
        else:
            return endpoint

    def purge_cache(self):
        self.token_path.unlink()
        self.tokens = None

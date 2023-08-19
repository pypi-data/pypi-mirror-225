import asyncio
import os
import random
from dataclasses import dataclass, field
from datetime import datetime
from functools import partial, wraps
from http import HTTPStatus
from typing import (
    Any,
    Callable,
    ClassVar,
    Coroutine,
    Iterable,
    Mapping,
    Optional,
    Union,
)

import httpx
from dateutil.parser import isoparse

import arraylake_client
from arraylake_client.log_util import get_logger
from arraylake_client.token import TokenHandler
from arraylake_client.types import ApiTokenInfo, OauthTokensResponse, UserInfo

HTTP_TIMEOUT = int(os.environ.get("ARRAYLAKE_CLIENT_HTTP_TIMEOUT", 90))

logger = get_logger(__name__)


def retry_on_exception(exception, n):
    """Retry a function when a specific exception is raised

    Intended to be used as a decorator. For example:

    @retry_on_exception(ValueError, n=3)
    async def raise_value_error():
        raise ValueError

    If the exception is re-raised `n` times, the final exception is returned.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for i in range(n):
                try:
                    return await func(*args, **kwargs)
                except exception:
                    if i == n - 1:
                        raise
                    logger.debug(f"{exception} encountered, retrying time #{i}")
                    await asyncio.sleep(0.5)  # try again after a pause

        return wrapper

    return decorator


async def gather_and_check_for_exceptions(*aws):
    """helper function to call asyncio.gather on a list of awaitables and check if any returned an exception"""
    results = await asyncio.gather(*aws, return_exceptions=True)
    for r in results:
        if isinstance(r, Exception):
            raise r  # is only raising on the first error ok?
    return results


class ArraylakeHttpClient:
    """Base class to centralize interacting with Arraylake REST API"""

    api_url: str
    hint: str = None
    token: str = field(default=None, repr=False)  # machine token. id/access/refresh tokens are managed by CustomOauth
    timeout: int = HTTP_TIMEOUT

    _client: Optional[httpx.AsyncClient]  # set in __aenter__
    _OPEN: bool

    def __init__(self, api_url: str, hint: str = None, token: str = None):
        self.api_url = api_url
        self.hint = hint
        self.token = token

        self._default_headers = {
            "accept": "application/vnd.earthmover+json",
            # technically we don't enforce this, for now it's for debugging purposes
            "client-name": "arraylake-python-client",
            "client-version": arraylake_client.__version__,
        }

        self._client = None
        self._OPEN = False

    @retry_on_exception(httpx.RemoteProtocolError, 3)
    async def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """Convenience method to make a standard request with retry on RemoteProtocolError"""
        if not self._OPEN:
            raise ValueError("must be in async context to make requests")
        return await self._client.request(method, path, **kwargs)

    async def __aenter__(self):
        transport = AsyncRetryTransport()

        if self.token:
            # if a token is presented, just use that token for all all Authentication headers
            auth = TokenAuth(self.token)
        else:
            # otherwise, assume we are using OAuth tokens stored on disk
            auth = UserAuth(self.api_url, self.hint)

        self._client = await httpx.AsyncClient(
            base_url=self.api_url, transport=transport, headers=self._default_headers, auth=auth, timeout=self.timeout
        ).__aenter__()
        self._OPEN = True
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._client.__aexit__(*args, **kwargs)
        self._client = None
        self._OPEN = False

    async def get_user(self) -> Union[ApiTokenInfo, UserInfo]:
        """Make an API request to the /user route to get the current authenticated user

        This is used in various places through the Arraylake client. For example, we use this method to:
        - determine the committer/author when creating a repo instance
        - check if a user is logged in with valid credentials

        TODO: consider moving this to the Client API.
        """
        response = await self._request("GET", "user")
        handle_response(response)
        data = response.json()
        # TODO: It would be preferable to have a firmer way to evaluate this
        # perhaps via an explicit type property included with the response
        # object.
        if data.get("first_name"):
            return UserInfo(**data)
        else:
            return ApiTokenInfo(**data)


def _exception_log_debug(request: httpx.Request, response: httpx.Response):
    """Utility function to log data pertaining to a failed req/response"""
    secret_headers = {"authorization"}
    clean_request_headers = {n: ("[omitted]" if n.lower() in secret_headers else v) for n, v in request.headers.items()}
    clean_response_headers = {n: ("[omitted]" if n.lower() in secret_headers else v) for n, v in response.headers.items()}
    logger.debug(
        "HTTP request failure debug information",
        url=str(request.url),
        request_content=request.content,
        request_headers=clean_request_headers,
        response_headers=clean_response_headers,
        response_status_code=response.status_code,
    )


def handle_response(response: httpx.Response):
    """Convenience function to handle response status codes"""
    try:
        response.raise_for_status()
    except httpx.RequestError as exc:
        _exception_log_debug(exc.request, response)
        raise RuntimeError(f"An error occurred while requesting {exc.request.url!r}. {response}: {response.read()}")
    except httpx.HTTPStatusError as exc:
        _exception_log_debug(exc.request, response)
        # we can consider a 422 an explicit message from the serves that something was invalid but handled about
        # the user input, and surface this directly to the caller. for other, less clear cases,
        # return a more complete message including the API url.
        if exc.response.status_code == 422:
            raise ValueError(response.json()["detail"])
        else:
            raise ValueError(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}. {response}: {response.read()}"
            )


@dataclass(frozen=True)
class TokenAuth(httpx.Auth):
    """
    Simple token-based Auth

    This auth flow will insert a Bearer token into the Authorization header of each request.

    Parameters
    ----------
    token : str
        Token to be inserted into request headers.
    """

    token: str

    def auth_flow(self, request: httpx.Request) -> httpx.Request:
        # Send the request, with a bearer token header
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


class UserAuth(httpx.Auth):
    """
    User / Oauth token-based Auth

    Parameters
    ----------
    api_endpoint : str
    """

    requires_response_body = True

    def __init__(self, api_endpoint: str, hint: str = None):
        self.api_endpoint = api_endpoint
        self.hint = hint
        self._refresh_url = f"{api_endpoint}/refresh_token"

        # self._sync_lock = threading.RLock()  # uncomment when we need sync_auth_flow
        self._async_lock = asyncio.Lock()

        self._token_handler = TokenHandler(api_endpoint=api_endpoint, hint=self.hint, raise_if_not_logged_in=True)

    @property
    def _bearer_token(self):
        token = self._token_handler.tokens.id_token.get_secret_value()
        return f"Bearer {token}"

    def build_refresh_request(self) -> httpx.Request:
        # Return an `httpx.Request` for refreshing tokens.
        params = {"token": self._token_handler.tokens.refresh_token.get_secret_value()}
        if self.hint:
            params["hint"] = self.hint
        request = httpx.Request("GET", self._refresh_url, params=params)
        return request

    async def async_auth_flow(self, request: httpx.Request) -> httpx.Request:
        request.headers["Authorization"] = self._bearer_token
        response = yield request
        if response.status_code == httpx.codes.UNAUTHORIZED:
            # If the server issues a 401 response, then issue a request to
            # refresh tokens, and resend the request.
            async with self._async_lock:
                refresh_response = yield self.build_refresh_request()
                await refresh_response.aread()
                handle_response(refresh_response)
                new_tokens = OauthTokensResponse.parse_obj(refresh_response.json())
                self._token_handler.update(new_tokens)

            request.headers["Authorization"] = self._bearer_token
            yield request

    def sync_auth_flow(self, request: httpx.Request) -> httpx.Request:
        # we can implement this method if we end up needing the sync httpx.Client
        raise RuntimeError("Sync auth flow not implemented yet")


# Copied and modified from https://github.com/encode/httpx/issues/108#issuecomment-1434439481
@dataclass
class AsyncRetryTransport(httpx.AsyncBaseTransport):
    max_attempts: int = 5
    max_backoff_wait: float = 10
    backoff_factor: float = 0.1  # seconds, doubled every retry
    jitter_ratio: float = 0.1
    respect_retry_after_header: bool = True
    retryable_methods: Optional[Iterable[str]] = None
    retry_status_codes: Optional[Iterable[int]] = None

    RETRYABLE_METHOD: ClassVar = frozenset(["HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "TRACE"])
    RETRYABLE_STATUS_CODES: ClassVar = frozenset(
        [
            HTTPStatus.TOO_MANY_REQUESTS,
            HTTPStatus.BAD_GATEWAY,
            HTTPStatus.SERVICE_UNAVAILABLE,
            HTTPStatus.GATEWAY_TIMEOUT,
        ]
    )

    """
    A custom HTTP transport that automatically retries requests using an exponential backoff strategy
    for specific HTTP status codes and request methods.

    Args:
        wrapped_transport (Union[httpx.BaseTransport, httpx.AsyncBaseTransport]): The underlying HTTP transport
            to wrap and use for making requests.
        max_attempts (int, optional): The maximum number of times to retry a request before giving up. Defaults to 10.
        initial_backoff_wait (float, optional): The initial backoff time in seconds. Defaults to 0.1.
        max_backoff_wait (float, optional): The maximum time to wait between retries in seconds. Defaults to 60.
        backoff_factor (float, optional): The factor by which the wait time increases with each retry attempt.
            Defaults to 0.1.
        jitter_ratio (float, optional): The amount of jitter to add to the backoff time. Jitter is a random
            value added to the backoff time to avoid a "thundering herd" effect. The value should be between 0 and 0.5.
            Defaults to 0.1.
        respect_retry_after_header (bool, optional): Whether to respect the Retry-After header in HTTP responses
            when deciding how long to wait before retrying. Defaults to True.
        retryable_methods (Iterable[str], optional): The HTTP methods that can be retried. Defaults to
            ["HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "TRACE"].
        retry_status_codes (Iterable[int], optional): The HTTP status codes that can be retried. Defaults to
            [429, 502, 503, 504].
    """

    def __post_init__(self) -> None:
        if self.retryable_methods is None:
            self.retryable_methods = self.RETRYABLE_METHOD
        if self.retry_status_codes is None:
            self.retry_status_codes = self.RETRYABLE_STATUS_CODES
        if self.jitter_ratio < 0 or self.jitter_ratio > 0.5:
            raise ValueError(f"Jitter ratio should be between 0 and 0.5, actual {self.jitter_ratio}")
        self.wrapped_transport = httpx.AsyncHTTPTransport()

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        """Sends an HTTP request, possibly with retries.

        Args:
            request: The request to perform.

        Returns:
            The response.

        """
        transport: httpx.AsyncBaseTransport = self.wrapped_transport
        if request.method in self.retryable_methods:
            send_method = partial(transport.handle_async_request)
            response = await self._retry_operation_async(request, send_method)
        else:
            response = await transport.handle_async_request(request)
        return response

    async def aclose(self) -> None:
        """
        Closes the underlying HTTP transport, terminating all outstanding connections and rejecting any further
        requests.

        This should be called before the object is dereferenced, to ensure that connections are properly cleaned up.
        """
        transport: httpx.AsyncBaseTransport = self.wrapped_transport
        await transport.aclose()

    def _calculate_sleep(self, attempts_made: int, headers: Union[httpx.Headers, Mapping[str, str]]) -> float:
        # Retry-After
        # The Retry-After response HTTP header indicates how long the user agent should wait before
        # making a follow-up request. There are three main cases this header is used:
        # - When sent with a 503 (Service Unavailable) response, this indicates how long the service
        #   is expected to be unavailable.
        # - When sent with a 429 (Too Many Requests) response, this indicates how long to wait before
        #   making a new request.
        # - When sent with a redirect response, such as 301 (Moved Permanently), this indicates the
        #   minimum time that the user agent is asked to wait before issuing the redirected request.
        retry_after_header = (headers.get("Retry-After") or "").strip()
        if self.respect_retry_after_header and retry_after_header:
            if retry_after_header.isdigit():
                return float(retry_after_header)

            try:
                parsed_date = isoparse(retry_after_header).astimezone()  # converts to local time
                diff = (parsed_date - datetime.now().astimezone()).total_seconds()
                if diff > 0:
                    return min(diff, self.max_backoff_wait)
            except ValueError:
                pass

        # note, this is never called for attempts_made == 0
        backoff = self.backoff_factor * (2 ** (attempts_made - 1))
        jitter = (backoff * self.jitter_ratio) * random.choice([1, -1])
        total_backoff = backoff + jitter
        return min(total_backoff, self.max_backoff_wait)

    async def _retry_operation_async(
        self,
        request: httpx.Request,
        send_method: Callable[..., Coroutine[Any, Any, httpx.Response]],
    ) -> httpx.Response:
        remaining_attempts = self.max_attempts
        attempts_made = 0
        headers = {}  # type: Union[httpx.Headers, Mapping[str, str]]
        while True:
            if attempts_made > 0:
                await asyncio.sleep(self._calculate_sleep(attempts_made, headers))
            response = await send_method(request)
            headers = response.headers
            if remaining_attempts < 1 or response.status_code not in self.retry_status_codes:
                return response
            await response.aclose()
            attempts_made += 1
            remaining_attempts -= 1

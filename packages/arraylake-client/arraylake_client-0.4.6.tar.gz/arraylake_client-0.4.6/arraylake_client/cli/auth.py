from typing import Union
from webbrowser import open_new

import typer
from rich.prompt import Prompt

from arraylake_client import config
from arraylake_client.api_utils import ArraylakeHttpClient
from arraylake_client.cli.utils import coro, error_console, print_logo, rich_console
from arraylake_client.token import AuthException, TokenHandler
from arraylake_client.types import ApiTokenInfo, UserInfo

auth = typer.Typer(help="Manage Arraylake authentication")


def _get_auth_handler(org: str = None) -> TokenHandler:
    return TokenHandler(api_endpoint=config.get("service.uri"), hint=org or config.get("user.org", None))


async def _get_user() -> Union[ApiTokenInfo, UserInfo]:
    async with ArraylakeHttpClient(api_url=config.get("service.uri")) as client:
        user = await client.get_user()
    return user


@auth.command()
@coro
async def login(
    browser: bool = typer.Option(True, help="Whether to automatically open a browser window."),
    org: str = typer.Option(None, help="Org identifier for custom login provider"),
):
    """**Log in** to Arraylake

    This will automatically open a browser window. If **--no-browser** is specified, a link will be printed.

    **Examples**

    - Log in without automatically opening a browser window

        ```
        $ arraylake auth login --no-browser
        ```
    """
    print_logo()
    handler = _get_auth_handler(org)
    if handler.tokens is not None:
        await handler.refresh_token()
    else:
        url = await handler.get_authorize_url()

        if browser:
            open_new(url)
        else:
            rich_console.print(f"Authorize with this url: {url}")

        code = Prompt.ask("Enter your code :sunglasses:")

        await handler.get_token(code)

    user = await _get_user()
    rich_console.print(user.json())
    rich_console.print(f"✅ Token stored at {handler.token_path}")


@auth.command()
@coro
async def refresh():
    """**Refresh** Arraylake's auth token"""
    print_logo()
    handler = _get_auth_handler()
    if handler.tokens is not None:
        await handler.refresh_token()
        user = await _get_user()  # checks that the new tokens are valid
        rich_console.print(user.json())
        rich_console.print(f"✅ Token stored at {handler.token_path}")
    else:
        error_console.print("Not logged in, log in with `arraylake auth login`")
        raise typer.Exit(code=1)


@auth.command()
def logout(browser: bool = typer.Option(True, help="Whether to also remove the browsers auth cookie.")):
    """**Logout** of Arraylake

    **Examples**

    - Logout of arraylake

        ```
        $ arraylake auth logout
        ```
    """
    print_logo()
    handler = _get_auth_handler()
    try:
        url = handler.get_logout_url()
        if browser:
            open_new(url)
        else:
            rich_console.print(f"To completely log out, open this URL in your browser: {url}")
        handler.purge_cache()
        rich_console.print(f"✅ Token removed from {handler.token_path}")
    except FileNotFoundError:
        error_console.print("Not logged in")
        raise typer.Exit(code=1)


@auth.command()
@coro
async def status():
    """Verify and display information about your authentication **status**"""
    print_logo()

    rich_console.print(f"Arraylake API Endpoint: {config.get('service.uri')}")
    try:
        user = await _get_user()
        rich_console.print(f"  → logged in as {user.email}")
    except AuthException:
        error_console.print("Not logged in, log in with `arraylake auth login`")
        raise typer.Exit(code=1)


@auth.command()
def token():
    """Display your authentication **token**"""
    print_logo()
    handler = _get_auth_handler()
    try:
        rich_console.print(handler.tokens.id_token.get_secret_value())
    except (AuthException, AttributeError):
        error_console.print("Not logged in, log in with `arraylake auth login`")
        raise typer.Exit(code=1)

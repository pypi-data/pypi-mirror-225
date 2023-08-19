from enum import Enum

import typer
from rich import print_json
from rich.table import Table

from arraylake_client import AsyncClient
from arraylake_client.cli.utils import coro, rich_console, simple_progress
from arraylake_client.log_util import get_logger

app = typer.Typer(help="Manage Arraylake repositories")
logger = get_logger(__name__)


class ListOutputType(str, Enum):
    rich = "rich"
    json = "json"


def _repos_table(repos, org):
    table = Table(title=f"Arraylake Repositories for [bold]{org}[/bold]", min_width=80)
    table.add_column("Name", justify="left", style="cyan", no_wrap=True, min_width=45)
    table.add_column("Created", justify="right", style="green", min_width=25)

    for repo in repos:
        table.add_row(repo["name"], repo["created"])

    return table


@app.command(name="list")
@coro
async def list_repos(
    org: str = typer.Argument(..., help="The organization name"), output: ListOutputType = typer.Option("rich", help="Output formatting")
):
    """**List** repositories in the specified organization

    **Examples**

    - List repos in _default_ org

        ```
        $ arraylake repo list my-org
        ```
    """
    with simple_progress(f"Listing repos for [bold]{org}[/bold]...", quiet=(output != "rich")):
        repos = await AsyncClient().list_repos(org)

    if output == "json":
        print_json(data=repos)
    elif repos:
        rich_console.print(_repos_table(repos, org))
    else:
        rich_console.print("\nNo results")


@app.command()
@coro
async def create(repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}")):
    """**Create** a new repository

    **Examples**

    - Create new repository

        ```
        $ arraylake repo create my-org/example-repo
        ```
    """
    with simple_progress(f"Creating repo [bold]{repo_name}[/bold]..."):
        await AsyncClient().create_repo(repo_name)


@app.command()
@coro
async def delete(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    confirm: bool = typer.Option(False, help="confirm deletion without prompting"),
):
    """**Delete** a repository

    **Examples**

    - Delete repository without confirmation prompt

        ```
        $ arraylake repo delete my-org/example-repo --confirm
        ```
    """
    if not confirm:
        confirm = typer.confirm(f"This will permanently remove the {repo_name} repo. Are you sure you want to continue?", abort=True)

    with simple_progress(f"Deleting repo [bold]{repo_name}[/bold]..."):
        await AsyncClient().delete_repo(repo_name, imsure=confirm, imreallysure=confirm)


@app.command()
@coro
async def tree(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    depth: int = typer.Option(10, help="Maximum depth to descend into hierarchy."),
    prefix: str = typer.Option("", help="Path in repo to start the hierarchy, e.g. `root/foo`."),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    """Show tree representation of a repository

    **Examples**

    - Show the tree representation of a repo up to level 5

        ```
        $ arraylake repo tree my-org/example-repo --depth 5
        ```
    """

    client = AsyncClient()
    repo = await client.get_repo(repo_name)
    async with repo:
        await repo.checkout()
        _tree = await repo.tree(prefix=prefix, depth=depth)

    if output == "json":
        print_json(_tree.json())
    else:
        rich_console.print(_tree._as_rich_tree(name=repo_name))

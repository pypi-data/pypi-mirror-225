import asyncio
import inspect
import re
from contextlib import contextmanager
from functools import wraps
from typing import Iterable, Union

import click
import typer.rich_utils
from rich.console import Console, group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from typer.core import MarkupMode
from typer.rich_utils import (
    MARKUP_MODE_MARKDOWN,
    STYLE_HELPTEXT_FIRST_LINE,
    _make_rich_rext,
)

rich_console = Console()
error_console = Console(stderr=True, style="red")


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


# temporary workaround for typer#447
# https://github.com/tiangolo/typer/issues/447
@group()
def _get_custom_help_text(
    *,
    obj: Union[click.Command, click.Group],
    markup_mode: MarkupMode,
) -> Iterable[Union[Markdown, Text]]:
    # Fetch and dedent the help text
    help_text = inspect.cleandoc(obj.help or "")

    # Trim off anything that comes after \f on its own line
    help_text = help_text.partition("\f")[0]

    # Get the first paragraph
    first_line = help_text.split("\n\n")[0]
    # Remove single linebreaks
    if markup_mode != MARKUP_MODE_MARKDOWN and not first_line.startswith("\b"):
        first_line = first_line.replace("\n", " ")
    yield _make_rich_rext(
        text=first_line.strip(),
        style=STYLE_HELPTEXT_FIRST_LINE,
        markup_mode=markup_mode,
    )

    # Get remaining lines, remove single line breaks and format as dim
    remaining_paragraphs = help_text.split("\n\n")[1:]
    if remaining_paragraphs:
        remaining_lines = inspect.cleandoc("\n\n".join(remaining_paragraphs).replace("<br/>", "\\"))
        yield _make_rich_rext(
            text=remaining_lines,
            style="cyan",
            markup_mode=markup_mode,
        )


typer.rich_utils._get_help_text = _get_custom_help_text


LOGO_ART = r""" ___       __  ___             __        ___  __
|__   /\  |__)  |  |__|  |\/| /  \ \  / |__  |__)
|___ /~~\ |  \  |  |  |  |  | \__/  \/  |___ |  \
"""


def print_logo():
    rich_console.print(Panel.fit("[#641c84 bold]" + LOGO_ART, border_style="#f6a004"))


def _parse_exception(e: Exception):
    # extract the HTTP error message and turn it into something more user-friendly
    ex = str(e)
    match = re.search(r"\"detail\":\"(.*)\"", ex)
    if match:
        return match.group(1)
    return ex


@contextmanager
def simple_progress(description, total=1, quiet=False):
    exit_msg = None  # type: Optional[str]
    if quiet:
        yield
    else:
        with Progress(
            SpinnerColumn(finished_text="[bold green]✓[/bold green]"),
            TextColumn("[progress.description]{task.description}"),
            console=rich_console,
        ) as progress:
            task = progress.add_task(description, total=total)
            try:
                yield progress, task
            except Exception as e:
                progress.update(task, advance=0, description=description + "[red bold]failed[/red bold]")
                exit_msg = _parse_exception(e)
            else:
                progress.update(task, advance=1, description=description + "[green bold]succeeded[/green bold]")
    if exit_msg:
        error_console.print(exit_msg)
        exit(1)

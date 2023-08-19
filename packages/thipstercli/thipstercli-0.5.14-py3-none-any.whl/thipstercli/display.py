"""Display functions for the CLI."""
import sys
from importlib.metadata import version as get_version

import typer
from rich import print

from thipstercli.config import state


def error(*args, **kwargs):
    """Print an error message and exit the program."""
    print('[bold][red]Error :[/red][/bold]', *args, file=sys.stderr, **kwargs)
    sys.stderr.flush()
    raise typer.Exit(1)


def warn(*args, **kwargs):
    """Print a warning message."""
    print(
        '[bold][yellow]Warning :[/yellow][/bold]',
        *args, file=sys.stdout, **kwargs,
    )
    sys.stdin.flush()


def print_if_verbose(text: str):
    """Print the given text if the verbose flag is set."""
    print(text) if state.get('verbose', False) else None


def print_start_if_verbose(text: str):
    """Print ' :arrow_forward: {text}... ' if the verbose flag is set."""
    print_if_verbose(f':arrow_forward: {text} ...')


def print_success_if_verbose(text: str):
    """Print ' :white_heavy_check_mark: {text} ' if the verbose flag is set."""
    print_if_verbose(f'{text} :white_heavy_check_mark:')


def print_package_version(package: str):
    """Print the version of the given package."""
    print(f':bookmark: {package} [green]v{get_version(package)}[/green]')

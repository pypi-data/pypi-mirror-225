"""Commands to manage the app config."""
from typing import Annotated

import typer
from rich import print

from thipstercli.config import set_config_file, state, update_config_file
from thipstercli.display import error, print_if_verbose

config_app = typer.Typer(no_args_is_help=True)

__private_config = [
    'appname',
    'auth_provider',
    'repository_recovery_mode',
    'models_repository',
    'models_repository_branch',
]


@config_app.callback()
def _callback():
    """Manage thipster config."""


@config_app.command(name='set')
def set_command(
    name: Annotated[
        str, typer.Argument(
            default=...,
            help='Config key to set',
        ),
    ],
    value: Annotated[
        str, typer.Argument(
            default=...,
            help='Associated value',
        ),
    ],
):
    """Set the value for a key in the configuration file."""
    if name not in state:
        error(f'Key {name} not found')

    if name in __private_config:
        error(f"{name} can't be set using this command")

    state[name] = value
    update_config_file(state)
    print_if_verbose(f'Set {name} to {value}')


@config_app.command(name='unset')
def unset_command(
    name: Annotated[
        str, typer.Argument(
            default=...,
            help='Config key to unset',
        ),
    ],
):
    """Remove a variable from configuration file."""
    if name not in state:
        error(f'Key {name} not found')

    if name in __private_config:
        error(f"{name} can't be unset")

    del state[name]
    set_config_file(state)
    print_if_verbose(f'Unset {name}')


@config_app.command(name='get')
def get_command(
    name: Annotated[
        str, typer.Argument(
            default=...,
            help='Config key to get',
        ),
    ],
):
    """Get value: name from config file."""
    if name not in state:
        error(f'Key {name} not found in config')

    print(f'{name} = {state[name]}')

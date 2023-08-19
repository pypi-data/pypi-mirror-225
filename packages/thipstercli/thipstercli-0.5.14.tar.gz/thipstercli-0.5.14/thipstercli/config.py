"""Configuration module for the application."""
import json
from pathlib import Path

from rich import print
from typer import get_app_dir

from . import constants
from .helpers import check_thipster_module_exists

state = {}

app_dir = get_app_dir(constants.APP_NAME)
config_file: Path = Path(app_dir) / constants.CONFIG_FILE_NAME


def init_parameters() -> None:
    """Initialize the state of the application."""
    if not config_file.is_file():
        set_default_config()
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text(json.dumps(state, sort_keys=True, indent=4))
        return

    state.update(json.loads(config_file.read_text()))

    if not state.get('auth_provider'):
        return

    if not check_thipster_module_exists('auth', state['auth_provider']):
        print(f':rotating_light: User set Auth Provider [red]{state["auth_provider"]}\
[/red] not found')
        state.pop('auth_provider')


def set_default_config() -> None:
    """Set the default values for the user configuration file."""
    state['app_name'] = constants.APP_NAME
    state['verbose'] = constants.VERBOSE
    state['repository_recovery_mode'] = constants.REPOSITORY_RECOVERY_MODE
    state['models_repository'] = constants.MODELS_REPOSITORY
    state['models_repository_branch'] = constants.MODELS_REPOSITORY_BRANCH
    state['input_dir'] = constants.INPUT_DIR
    state['output_dir'] = constants.OUTPUT_DIR


def update_config_file(parameters: dict[str, object]) -> None:
    """Update the config file with the given parameters."""
    if config_file.is_file():
        config: dict[str, object] = json.loads(config_file.read_text())
        config.update(parameters)
    else:
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config = parameters

    config_file.write_text(json.dumps(config, sort_keys=True, indent=4))


def set_config_file(new_config: dict[str, object]) -> None:
    """Update the config file with the given parameters."""
    if not config_file.is_file():
        config_file.parent.mkdir(parents=True, exist_ok=True)

    config = new_config

    config_file.write_text(json.dumps(config, sort_keys=True, indent=4))

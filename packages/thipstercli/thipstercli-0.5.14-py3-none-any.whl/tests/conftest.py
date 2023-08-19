"""Pytest configuration file."""
import json
from pathlib import Path

import pytest
from typer import get_app_dir

import thipstercli.constants as constants
from thipstercli.config import init_parameters


@pytest.fixture
def init_app_state():
    """Initialize the app state."""
    init_parameters()
    yield


@pytest.fixture
def config_path():
    """Return the user config file path."""
    return Path(get_app_dir(constants.APP_NAME)) / constants.CONFIG_FILE_NAME


@pytest.fixture
def create_config_file(config_path):
    """Create a user config file."""
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)

    yield config_path

    if config_path.exists():
        Path(config_path).unlink()


@pytest.fixture
def config_file(
    create_config_file,
):
    """Create a user config file with default values."""
    conf_str = """{
        "app_name": "thipstercli",
        "auth_provider": "google",
        "input_dir": "test/input_directory",
        "local_models_repository_path": "models",
        "models_repository": "THipster/models",
        "models_repository_branch": "main",
        "repository_recovery_mode": "local",
        "output_dir": "test/output_directory",
        "verbose": true
}"""
    create_config_file.write_text(conf_str)

    init_parameters()

    yield json.loads(conf_str)


@pytest.fixture
def empty_config_file(create_config_file):
    """Create an empty user config file."""
    create_config_file.write_text("""{}""")
    init_parameters()
    yield


def get_config_file() -> dict[str, object]:
    """Return the user config file as a dictionary."""
    return json.loads(
        (Path(get_app_dir(constants.APP_NAME)) / constants.CONFIG_FILE_NAME)
        .read_text(),
    )

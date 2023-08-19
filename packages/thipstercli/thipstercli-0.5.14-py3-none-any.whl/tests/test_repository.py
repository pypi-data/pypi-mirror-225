"""Test the repository subcommand."""
from pathlib import Path

import pytest
from typer import get_app_dir
from typer.testing import CliRunner

import thipstercli.constants as constants
from tests.conftest import get_config_file
from thipstercli.commands.repository import repository_app

runner = CliRunner(mix_stderr=False)


@pytest.fixture
def create_models_directory():
    """Create the model subdirectory if needed."""
    models_path = Path(get_app_dir(constants.APP_NAME)) / 'models'
    clean_up = False
    if not models_path.exists():
        clean_up = True
        Path.mkdir(models_path)

    yield models_path

    if clean_up and models_path.exists():
        models_path.rmdir()


@pytest.fixture
def create_example_repo(create_models_directory):
    """Create an example model repository if needed."""
    repo_path = Path(create_models_directory) / 'example'
    clean_up = False
    if not repo_path.exists():
        clean_up = True
        repo_path.mkdir()

    yield 'example'

    if clean_up and repo_path.exists():
        repo_path.rmdir()


def test_list_repositories(create_example_repo):
    """Test `thipster repository list` command."""
    example_repo = create_example_repo

    result = runner.invoke(repository_app, ['list'])

    assert result.exit_code == 0
    assert example_repo in result.stdout.lower()


def test_use_repository(create_example_repo):
    """Test `thipster repository use` command."""
    _ = create_example_repo

    runner.invoke(repository_app, ['use', 'example'])

    assert get_config_file().get('repository_recovery_mode') == 'local'
    assert get_config_file().get('models_repository') == 'example'

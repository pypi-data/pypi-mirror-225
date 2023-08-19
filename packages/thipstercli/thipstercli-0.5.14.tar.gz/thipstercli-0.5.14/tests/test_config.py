"""Test the config subcommand."""

from typer.testing import CliRunner

from tests.conftest import get_config_file
from thipstercli.commands import config_app

runner = CliRunner(mix_stderr=False)


def test_set_config(config_file):
    """Test `thipster config set`."""
    config_file
    key = 'output_dir'
    value = 'test'

    result = runner.invoke(config_app, ['set', key, value])

    assert result.exit_code == 0
    assert get_config_file()[key] == value


def test_get_config(config_file):
    """Test `thipster config get`."""
    config = config_file
    key = 'output_dir'

    result = runner.invoke(config_app, ['get', key])

    assert result.exit_code == 0
    assert get_config_file()[key] == config[key]


def test_unset_config(config_file):
    """Test `thipster config unset`."""
    config_file
    key = 'output_dir'

    result = runner.invoke(config_app, ['unset', key])

    assert result.exit_code == 0
    assert get_config_file().get(key) is None


def test_unset_bad_config(config_file):
    """Test `thipster config unset` with bad variables."""
    config_file
    key = 'models_repository'

    result = runner.invoke(config_app, ['unset', key])

    assert result.exit_code == 1

    key = 'not_found'
    result = runner.invoke(config_app, ['unset', key])

    assert result.exit_code == 1

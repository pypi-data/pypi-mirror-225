"""Test the cli.py module."""
import os
from importlib.metadata import version as get_version
from pathlib import Path

from typer import get_app_dir
from typer.testing import CliRunner

from thipstercli.cli import main_app
from thipstercli.config import state

AUTH_FILE_PATH = 'tests/credentials.json'

runner = CliRunner(mix_stderr=False)


def auth_test(func):
    """Create a temporary credentials file for testing."""
    def wrapper(*args, **kwargs):
        delete_credentials = False
        if (
            not Path.exists(
                Path(get_app_dir('gcloud')) /
                'application_default_credentials.json',
            )
            and (
                os.getenv('GOOGLE_APPLICATION_CREDENTIALS') is not None
                or os.getenv('GOOGLE_APPLICATION_CREDENTIALS') != ''
            )
        ):

            delete_credentials = True
            if os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT') is None:
                no_credentials = 'No credentials available'
                raise Exception(no_credentials)

            with Path(AUTH_FILE_PATH).open('w') as auth_file:
                auth_file.write(
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS_CONTENT'],
                )
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = AUTH_FILE_PATH

        res = func(*args, **kwargs)

        if delete_credentials:
            Path(AUTH_FILE_PATH).unlink()

        return res
    return wrapper


def test_version():
    """Test the version command."""
    result = runner.invoke(main_app, ['version'])
    version = get_version('thipstercli')
    assert result.exit_code == 0
    assert 'THipster-cli' and version in result.output


def test_version_thipster():
    """Test the version command with thipster."""
    result = runner.invoke(main_app, ['version', '--thipster'])
    version = get_version('thipstercli')
    assert result.exit_code == 0
    assert 'THipster-cli' and version in result.output
    version = get_version('thipster')
    assert 'THipster' and version in result.output


def test_run_wrong_local_repository():
    """Test the run command with a wrong local repository path."""
    result = runner.invoke(
        main_app, ['run', 'tests/resources/bucket.thips', '-rl', 'wrong_path'],
    )
    assert result.exit_code != 0
    assert "Couldn't find wrong_path local repository" in result.stderr


def test_run_wrong_file_path():
    """Test the run command with a wrong local repository path."""
    result = runner.invoke(main_app, ['run', 'wrong_path'])
    assert result.exit_code != 0
    assert 'Error : Path not found :' in result.stderr
    assert 'wrong_path' in result.stderr


@auth_test
def test_run_bucket():
    """Test the run command with a gcp bucket resource."""
    result = runner.invoke(
        main_app, [
            'run', 'tests/resources/bucket.thips',
            '-rl', 'tests/resources/models',
        ],
    )

    assert result.exit_code == 0
    assert 'thipster_cli_test_bucket' in result.output
    assert 'Terraform will perform the following actions' \
        in result.output.replace('\n', '')


def test_config_file_verbose(config_file):
    """Test if the value of verbose is correctly set from the config file."""
    _ = config_file
    runner.invoke(main_app, ['--help'])
    assert state.get('verbose', False) is True


def test_config_file_input_dir(config_file):
    """Test if the value of input_dir is correctly set from the config file."""
    _ = config_file
    runner.invoke(main_app, ['--help'])
    assert state.get('input_dir', None) == 'test/input_directory'


def test_config_file_output_dir(config_file):
    """Test if the value of output_dir is correctly set from the config file."""
    _ = config_file
    runner.invoke(main_app, ['--help'])
    assert state.get('output_dir', None) == 'test/output_directory'

"""Test the repository subcommand."""
from pathlib import Path

import pytest
from typer import get_app_dir
from typer.testing import CliRunner

import thipstercli.constants as constants
from thipstercli.commands import info_app
from thipstercli.config import state

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
def create_example_repo(create_models_directory) -> Path:
    """Create an example model repository if needed."""
    repo_path = Path(create_models_directory) / 'example'
    clean_up = False
    if not repo_path.exists():
        clean_up = True
        repo_path.mkdir()

    state['repository_recovery_mode'] = 'local'
    state['models_repository'] = str(repo_path)

    yield repo_path

    if clean_up and repo_path.exists():
        repo_path.rmdir()


@pytest.fixture
def create_sample_models(create_example_repo):
    """Create example models."""
    example_repo: Path = create_example_repo
    vm_path = example_repo/'exampleResource.json'
    with vm_path.open('w') as f:
        f.write("""{
    "dependencies": {
        "toto": {
            "resource": "toto"
        }
    },
    "internalObjects": {
        "tata": {
            "resource" : "exampleResource/tata",
            "var_type": "list[ExampleResourceTata]",
            "default": {}
        }
    },
    "attributes":{
        "foo": {
            "optional": true,
            "default": "foo",
            "cdk_key": "foo",
            "var_type": "typing.List[str]"
        },
        "bar": {
            "optional": false,
            "cdk_key": "bar",
            "var_type": "str"
        }
    },
    "cdk_name_key": "name",

    "cdk_provider":"test_provider",
    "cdk_module":"test_module",
    "cdk_class":"example_class"
}""")

    yield vm_path

    vm_path.unlink()


def test_list_repositories(create_sample_models):
    """Test `thipster repository list` command."""
    example_repo: Path = create_sample_models

    result = runner.invoke(info_app, ['resources'])

    assert result.exit_code == 0
    assert example_repo.name.rstrip('.json') in result.stdout


def test_use_repository(create_sample_models):
    """Test `thipster repository use` command."""
    _ = create_sample_models

    result = runner.invoke(info_app, ['resource', 'exampleResource'])

    assert result.exit_code == 0
    assert 'toto toto' in result.stdout
    assert 'tata exampleResource/tata' in result.stdout
    assert 'foo  typing.List[str]' in result.stdout
    assert 'bar  str' in result.stdout

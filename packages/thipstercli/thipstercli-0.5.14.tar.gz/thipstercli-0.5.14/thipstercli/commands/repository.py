"""Repository subcommand."""
import json
import os
import shutil
from pathlib import Path
from typing import Annotated

import typer
from git import Repo
from rich import print
from rich.panel import Panel

from thipstercli.config import app_dir, state, update_config_file
from thipstercli.constants import LOCAL_MODELS_REPOSITORY_PATH
from thipstercli.display import error, warn

repository_app = typer.Typer(no_args_is_help=True)


@repository_app.callback()
def main():
    """Manage locally installed THipster repositories."""


@repository_app.command('list')
def list_repositories():
    """List all the locally installed THipster repositories."""
    downloaded_repos = list_installed_repos()

    repos_display = ''
    for repo in downloaded_repos:
        repos_display += f'[green]{repo}[/green]\n'
    print(Panel(repos_display, title='Locally installed model repositories'))
    __more_info_repos()


@repository_app.command('use')
def use(
    repository: Annotated[
        str, typer.Argument(
            default=...,
            help='The local repository to use',
        ),
    ],
):
    """Set the repository to use."""
    downloaded_repos = list_installed_repos()

    if repository not in downloaded_repos:
        state['repository_recovery_mode'] = 'online'
        warn('Model repository not locally installed, using online mode')
    else:
        state['repository_recovery_mode'] = 'local'

    state['models_repository'] = repository
    update_config_file(state)


@repository_app.command('download')
def download(
    url: Annotated[
        str,
        typer.Argument(
            default=...,
            help='The thipster repository to download. (*.git link)',
        ),
    ],
):
    """Download an online git repository as THipster repository."""
    if not url.endswith('.git'):
        error('Use .git link to repository')

    repositories_path = Path(app_dir) / LOCAL_MODELS_REPOSITORY_PATH
    if not repositories_path.exists():
        repositories_path.mkdir()

    clone_to = Path('/tmp') / 'thipster'
    Repo.clone_from(url, clone_to)

    with Path.open(Path(clone_to) / 'thipster-config.json') as f:
        config_path = f.read()

    try:
        config_file: dict = json.loads(config_path)
    except Exception as e:
        shutil.rmtree(clone_to)
        raise e

    repo_name = config_file.get('name')
    repo_directory = config_file.get('model_folder')

    if not (repo_name and repo_directory):
        shutil.rmtree(clone_to)
        error('Configuration error in thipster-config.json')

    if Path(repo_name).exists():
        shutil.rmtree(clone_to)
        error(f'Repository named {repo_name} already installed')

    try:
        shutil.move(
            Path(clone_to) / repo_directory,
            Path(repositories_path) / repo_name,
        )
    except Exception:
        shutil.rmtree(clone_to)
        error('Configuration error in thipster-config.json : bad model_folder')

    shutil.rmtree(clone_to)


def list_installed_repos():
    """List all locally installed THipster repository."""
    downloaded_repos = []
    repositories_path = Path(app_dir) / LOCAL_MODELS_REPOSITORY_PATH
    if Path(repositories_path).exists():
        downloaded_repos = os.listdir(repositories_path)

    return downloaded_repos


def __more_info_repos():
    print(
        Panel('For more information about a provider, run: thipster repository info \
<repository>'),
    ) if state.get('verbose') else None

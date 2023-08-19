"""THipster CLI."""
import importlib
import os
from pathlib import Path

import typer
from rich import print

from thipstercli import constants
from thipstercli.commands import providers, repository
from thipstercli.config import app_dir, init_parameters, state
from thipstercli.display import (
    error,
    print_if_verbose,
    print_package_version,
    print_start_if_verbose,
    print_success_if_verbose,
)

init_parameters()

main_app = typer.Typer(
    name=state.get(
        'app_name', constants.APP_NAME,
    ), no_args_is_help=True,
)

module = importlib.import_module('thipstercli.commands')
for command in os.scandir(Path(module.__file__).parent):
    if command.name.startswith('__'):
        continue
    command = command.name[:-3]

    main_app.add_typer(getattr(module, f'{command}_app'), name=command)


@main_app.callback()
def _callback(
    verbose: bool = typer.Option(
        False,
        '--verbose', '-v',
        help='Prints more information about the execution of the THipster CLI',
    ),
):
    """THipster CLI.

    THipster is a tool that allows you to generate Terraform code
    from a simple DSL or yaml file.
    """
    if not state.get('verbose', constants.VERBOSE):
        state['verbose'] = verbose


@main_app.command('version')
def _version(
    thipster: bool = typer.Option(
        False,
        '--thipster', '-t',
        help='Prints the version of the THipster tool',
    ),
):
    """Print the version of the THipster CLI."""
    print_package_version('thipstercli')

    if thipster:
        print_package_version('thipster')


@main_app.command('run')
def _run(
    path: str = typer.Argument(
        state.get('input_dir', constants.INPUT_DIR),
        help='Path to the file or directory to run',
    ),
    local_repository: str = typer.Option(
        None,
        '--repository-local', '-rl',
        help='Runs the THipster Tool using the given local model repository',
    ),
    online_repository: str = typer.Option(
        None,
        '--repository-online', '-ro',
        help='Runs the THipster Tool using the given model repository',
    ),
    repository_branch: str = typer.Option(
        state.get(
            'models_repository_branch',
            constants.MODELS_REPOSITORY_BRANCH,
        ),
        '--repository-branch', '-rb',
        help='Runs the THipster Tool using the given online model repository branch',
    ),
    provider: str = typer.Option(
        None,
        '--provider', '-p',
        help='Runs the THipster Tool using the given provider',
    ),
    apply: bool = typer.Option(
        False,
        '--apply', '-a',
        help='Applies the generated Terraform code',
    ),
):
    from thipster import Engine as ThipsterEngine
    from thipster.auth import Google
    from thipster.engine.exceptions import THipsterError
    from thipster.parser import ParserFactory
    from thipster.terraform import Terraform

    """Run the THipster Tool on the given path."""
    print_if_verbose(f'Running THipster on {path}')

    authentification_provider = providers.get_auth_provider_class(
        providers.check_provider_exists(provider),
    ) if provider else Google

    print_if_verbose(
        f'Provider Auth set to [green]{authentification_provider.__name__}[/green]',
    )

    repo = get_repo(local_repository, online_repository, repository_branch)

    engine = ThipsterEngine(
        ParserFactory(),
        repo,
        authentification_provider,
        Terraform(),
    )
    print_if_verbose('Engine start-up successful! :rocket:')

    try:
        print_start_if_verbose('Parsing files')
        parsed_file = engine.parse_files(path)
        print_success_if_verbose('Parsing successful!')

        print_start_if_verbose('Retrieving models')
        models = engine.get_models(parsed_file)
        print_success_if_verbose('Models retrieved!')

        print_start_if_verbose('Generating Terraform files')
        engine.generate_tf_files(parsed_file, models)
        print_success_if_verbose('Terraform files generated!')

        print_start_if_verbose('Initializing Terraform')
        engine.init_terraform()
        print_success_if_verbose('Terraform initialized!')

        print_start_if_verbose('Creating Terraform plan')
        print(engine.plan_terraform())

        if apply:
            print("Type 'yes' to apply the changes : ")
            print(engine.apply_terraform())

        print_if_verbose('Done! :tada:')

    except THipsterError as e:
        error(e.message)
    except FileNotFoundError as e:
        error(
            f'No such file or directory : [bold][red]{e.filename}[/red][/bold]',
        )
    except Exception as e:
        error(*e.args)


def get_repo(local_path, online_path, branch):
    """Get model repository from cli args or config."""
    from thipster.repository import GithubRepo, LocalRepo
    if local_path:
        if local_path in repository.list_installed_repos():
            repo_path = Path(app_dir) \
                / constants.LOCAL_MODELS_REPOSITORY_PATH \
                / local_path
            print_if_verbose(f'Using local model repository : {repo_path}')
            return LocalRepo(repo_path)

        if Path(local_path).exists():
            print_if_verbose(f'Using local model repository : {local_path}')
            return LocalRepo(local_path)

        error(f"Couldn't find {local_path} local repository")
        return None

    if online_path:
        print_if_verbose(
            f'Using online model repository : {online_path}/{branch}',
        )
        return GithubRepo(
            online_path,
            branch,
        )

    match state.get('repository_recovery_mode'):
        case 'local':
            repo_path = Path(app_dir) / 'models' / \
                state.get('models_repository')
            print_if_verbose(f'Using local model repository : {repo_path}')
            return LocalRepo(repo_path)

        case 'online':
            repo_path = state.get('models_repository')
            print_if_verbose(
                f'Using online model repository : {repo_path}/{branch}',
            )
            return GithubRepo(
                repo_path,
                branch,
            )

    error('No repository set')
    return None


if __name__ == '__main__':
    main_app()

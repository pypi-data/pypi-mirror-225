"""Commands to manage the auth providers."""
import json
import os
from pathlib import Path
from typing import Annotated

import requests
import typer
import validators
from rich import print
from rich.panel import Panel

from thipstercli import constants
from thipstercli.config import app_dir, state
from thipstercli.display import error, print_if_verbose

info_app = typer.Typer(no_args_is_help=True)


@info_app.callback()
def _callback(
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
):
    """Get info about resources."""
    if local_repository:
        state['repository_recovery_mode'] = 'local'
        state['models_repository'] = local_repository

    elif online_repository:
        state['repository_recovery_mode'] = 'online'
        state['models_repository'] = online_repository
        state['models_repository_branch'] = repository_branch


@info_app.command()
def resource(
    resource: Annotated[
        str, typer.Argument(
            default=...,
            help='The local repository to use',
        ),
    ] = None,
):
    """Get info about a given resource."""
    _info_resource(resource)


@info_app.command()
def resources(
):
    """List all the resources in repository."""
    models = _get_models()
    print(
        f'Models in {state.get("repository_recovery_mode")} '
        f'repository {state.get("models_repository")} :',
    )
    for model_name in models:
        print(f'\t{model_name}')


def _get_models():
    models = {}

    match state.get('repository_recovery_mode'):
        case 'local':
            repo_path = Path(app_dir) / 'models' / \
                state.get('models_repository')
            print_if_verbose(f'Using local model repository : {repo_path}')

            with os.scandir(repo_path) as repo_models:
                for model in repo_models:
                    if model.name.endswith('.json'):
                        models[model.name[:-5]] = Path(repo_path) / model.name

        case 'online':
            repo_path = state.get('models_repository')
            branch = state.get('models_repository_branch')
            print_if_verbose(
                f'Using online model repository : {repo_path}/{branch}',
            )

            response = requests.get(
                f'https://api.github.com/repos/{repo_path}/git/trees/{branch}',
            )
            if not response.ok:
                raise Exception

            repo_files = json.loads(response.content)

            for file in repo_files['tree']:
                filename = str(file['path'])
                if file['type'] == 'blob' and filename.endswith('.json'):
                    models[
                        filename[:-5]
                    ] = f'https://raw.githubusercontent.com/{repo_path}/{branch}/{filename}'

    return models


def _info_resource(resource_name: str):
    resource_json = _get_resource_json(resource_name)

    print(f'[bold]{resource_name}[/bold]')
    if resource_json.get('description'):
        print(f'\t{resource_json.get("description")}')

    dependencies_str = __dependencies_info(resource_json)
    dependencies_str = dependencies_str.rstrip('\n')

    attributes_str = __attributes_info(resource_json)
    attributes_str = attributes_str.rstrip('\n')

    if dependencies_str:
        print(Panel(dependencies_str, title='Dependencies'))

    if attributes_str:
        print(Panel(attributes_str, title='Attributes'))


def __attributes_info(resource_json):
    if (
        not resource_json.get('attributes')
        and not resource_json.get('internalObjects')
    ):
        return ''

    attr_len = max([len(k) for k in resource_json.get('attributes')]) \
        if resource_json.get('attributes') else 0
    io_len = max([len(k) for k in resource_json.get('internalObjects')]) \
        if resource_json.get('internalObjects') else 0

    name_width = max(attr_len, io_len)

    attributes_str = 'NAME'.ljust(name_width)
    attributes_str += ' TYPE\n'

    for name, attribute in resource_json.get('attributes').items():
        if not attribute.get('optional'):
            attributes_str += '[bold]'
        attributes_str += name.ljust(name_width)
        if not attribute.get('optional'):
            attributes_str += '[/bold]'
        var_type = str(attribute['var_type']).replace('[', '\\[')
        attributes_str += f' {var_type}\n'

        if attribute.get('default') is not None:
            attributes_str += f'\tDefault value : {attribute.get("default")!s}\n'

        if attribute.get('description'):
            attributes_str += f'\t{attribute.get("description")}\n'

    attributes_str += '\n'

    attributes_str = __internal_object_info(
        resource_json, attributes_str, name_width,
    )
    return attributes_str


def __internal_object_info(resource_json, attributes_str, name_width):
    if not resource_json.get('internalObjects'):
        return ''

    for name, internal_object in resource_json.get('internalObjects').items():
        if not internal_object.get('optional'):
            attributes_str += '[bold]'
        attributes_str += name.ljust(name_width)
        if not internal_object.get('optional'):
            attributes_str += '[/bold]'
        var_type = str(internal_object['resource']).replace('[', '\\[')
        attributes_str += f' {var_type}\n'

        defaults = internal_object.get('defaults')
        if defaults is not None and defaults != []:
            attributes_str += f'\tDefault value : {internal_object.get("defaults")!s}\n'

        if internal_object.get('description'):
            attributes_str += f'\t{internal_object.get("description")}\n'

    return attributes_str


def __dependencies_info(resource_json):
    if not resource_json.get('dependencies'):
        return ''

    name_width = max([len(k) for k in resource_json.get('dependencies')])

    deps_str = 'NAME'.ljust(name_width)
    deps_str += ' TYPE\n'

    for name, dependency in resource_json.get('dependencies').items():
        deps_str += f'[bold]{name.ljust(name_width)}[/bold] {dependency["resource"]}\n'

        if dependency.get('defaults') is not None:
            deps_str += f'\tDefault value : {dependency.get("default")!s}\n'

        if dependency.get('description'):
            deps_str += f'\t{dependency.get("description")}\n'

    return deps_str


def _get_resource_json(resource_name: str):
    models = _get_models()
    resource_model_location = ''
    if resource_name not in models:
        if resource_name.split('/')[0] not in models:
            error('Resource not found')

        resource_name += '.json'
        match state.get('repository_recovery_mode'):
            case 'local':
                resource_model_location = Path(app_dir) / 'models' / \
                    state.get('models_repository') / resource_name

            case 'online':
                resource_model_location = f'https://raw.githubusercontent.com/{state.get("models_repository")}/{state.get("models_repository_branch")}/{resource_name}'

            case _:
                msg = 'Unhandled recovery mode'
                raise Exception(msg)

    else:
        resource_model_location = models[resource_name]

    if isinstance(resource_model_location, Path):
        with resource_model_location.open() as f:
            return json.loads(f.read())

    elif validators.url(resource_model_location):
        response = requests.get(resource_model_location)
        if not response.ok:
            raise Exception

        return json.loads(response.content)

    error('Error while recovering the resource data')
    raise Exception

# THipster CLI

CLI tool to interact and use [THipster](https://github.com/THipster/THipster), build with [Typer](https://typer.tiangolo.com/).

THipster is a tool dedicated to simplifying the ordeal associated with writing Terraform files.
It allows users to write infrastructure as code in a simplified format, using either YAML (with JINJA) or the dedicated Thipster DSL.

Written entirely in Python, it leverages the Python CDK for Terraform to create Terraform files and apply them to the chosen provider.

<p align="center">
  <a href="https://github.com/THipster/THipster-cli/blob/main/LICENSE" target="_blank" alt="License">
    <img src="https://img.shields.io/github/license/THipster/THipster-cli" alt="License">
  </a>
  <a href="https://thipster-cli.readthedocs.io/en/latest/?badge=latest" target="_blank" alt="Read the docs documentation">
    <img src="https://readthedocs.org/projects/thipster-cli/badge/?version=latest" alt="Read the docs documentation">
  </a>
  <a href="https://pypi.org/project/thipstercli/" target="_blank" alt="PyPi package">
    <img src="https://img.shields.io/pypi/v/thipstercli?color=brightgreen&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://pypi.org/project/thipstercli/" target="_blank" alt="PyPi package">
    <img src="https://img.shields.io/pypi/pyversions/thipstercli?color=brightgreen" alt="Supported Python versions">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;">
  </a>
</p>

## Technology Stack
Written in Python 3.11, thipster-cli is build using [Typer](https://typer.tiangolo.com/).

## Project Status
THipster-cli is currently in an active development state. If you want to know more, please check the [CHANGELOG](https://github.com/THipster/THipster-cli/blob/main/CHANGELOG.md) for more details.

## Dependencies

To use the CLI, you will need to have all the required THipster dependencies installed on your machine. Please refer to the [THipster documentation](https://github.com/THipster/THipster#dependencies) for more details.

## Installation

The project is designed to be simply installed using [pip](https://pip.pypa.io/en/stable/).

```bash
pip install thipstercli
```

The list of available versions can be found on [PyPI](https://pypi.org/project/thipstercli/).

### Configuration

The CLI can be configured using a configuration file. A default `config.json` file will be created in the `/home/<user>/.config/thipstercli` directory the first time the CLI is used.

Example of a configuration file:
```json
{
    "app_name": "thipstercli",
    "auth_provider": "google",
    "input_dir": ".",
    "local_models_repository_path": "models",
    "models_repository": "THipster/models",
    "models_repository_branch": "main",
    "models_repository_provider": "local",
    "output_dir": ".",
    "verbose": false
}
```

## Usage

The cli is composed of 3 main commands:
- `version`: display the current version of the package
```bash
thipster version -t
```

- `providers`: subcommand group tp handle all tasks related to infrastructure providers
```bash
thipster providers --help
```

- `run`: main command to execute the thipster tool
```bash
thipster run --help
```

You can also check the [thipster package documentation](https://github.com/THipster/THipster/tree/main#usage) for more details on the main features and purpose of the tool.

## How to test the software

To test the CLI, you can run the following command:

```bash
pip install -e .[test]
pytest tests
```

## Known issues

All known issues, bugs, improvements, etc. are tracked as [GitHub issues](https://github.com/THipster/THipster-cli/issues).

## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's [Issue Tracker](https://github.com/THipster/THipster-cli/issues).

## Getting involved

To install the project in development mode, run the following command:

```bash
pip install -e .[dev,test]
pre-commit install && pre-commit run --all-files
```

If you would like to be involved in the project feel free to check the [CONTRIBUTING](https://github.com/THipster/THipster-cli/blob/main/CONTRIBUTING.md) file. We will be happy to have you onboard.

## Open source licensing info
1. [LICENSE](https://github.com/THipster/THipster-cli/blob/main/LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)

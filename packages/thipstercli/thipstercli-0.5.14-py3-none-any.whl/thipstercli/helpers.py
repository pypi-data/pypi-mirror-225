"""Functions to get thipster classes and modules."""
import importlib
import os
from pathlib import Path


def get_thipster_class(
    parent_module_name: str,
    module_name: str,
    class_name_extension: str,
) -> type:
    """Get the class from the given thipster module.

    Parameters
    ----------
    parent_module_name : str
        The path to the module relative to the thipster package.
    module_name : str
        The name of the module.
    class_name_extension : str
        The class name extension (e.g. 'Auth' for 'GoogleAuth' class in the google
        module), if the class name differs from the module name.

    Returns
    -------
    type
        The thipster class.
    """
    module = importlib.import_module(
        f'thipster.{parent_module_name.lower()}.{module_name.lower()}',
    )
    return getattr(
        module,
        (module_name.capitalize() if module_name.islower() else module_name) +
        class_name_extension,
    )


def check_thipster_module_exists(parent_module_name: str, module_name: str) -> bool:
    """Check if the given thipster module exists.

    Parameters
    ----------
    parent_module_name : str
        The path to the module relative to the thipster package.
    module_name : str
        The name of the module to check.

    Returns
    -------
    bool
        True if the module exists, False otherwise.
    """
    try:
        importlib.import_module(
            f'thipster.{parent_module_name.lower()}.{module_name.lower()}',
        )
        return True
    except ModuleNotFoundError:
        return False


def get_thipster_module_class_list(module_name: str) -> list[str]:
    """Get the list of classes in the given thipster module.

    Parameters
    ----------
    module_name : str
        The path to the module relative to the thipster package. (e.g. 'auth' for
        thipster.auth)

    Returns
    -------
    list[str]
        The list of classes contained in the module.
    """
    module = importlib.import_module(
        f'thipster.{module_name.lower()}',
    )
    module_class_list = []
    with os.scandir(Path(module.__file__).parent) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.py') and not \
                    entry.name.startswith('__'):
                module_class = entry.name.capitalize() if entry.name.islower() else \
                    entry.name
                module_class_list.append(module_class)
    return module_class_list


def get_auth_provider_class(provider: str) -> type:
    """Get the auth provider class from the given provider name."""
    return get_thipster_class('auth', provider, 'Auth')

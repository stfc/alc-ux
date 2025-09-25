"""Contains utility functions used throughout the python package."""

import pathlib
from importlib import import_module
from os import getenv

from IPython.display import Javascript, display


def get_py_app_dir() -> pathlib.Path:
    """
    Return the absolute path for the AiiDAlab ALC app python package.

    Returns
    -------
    pathlib.Path
        The path to the root python package directory.
    """
    return pathlib.Path(__file__).parent.resolve()


def get_app_dir() -> pathlib.Path:
    """
    Return the absolute path for the root directory of this project.

    Return the path to the root of the AiiDAlab application where
    the jupyter notebooks are contained to enable navigation between
    notebooks. This assumes that the environment variable AIIDALAB_APPS
    has been configured to point at the directory containing the app
    source code.

    Returns
    -------
    pathlib.Path
        The path to the root AiiDAlab application directory.
    """
    return (
        pathlib.Path(getenv("AIIDALAB_APPS", getenv("HOME", "") + "/apps/")) / "alc-ux/"
    )


def get_chem_shell_params(key: str) -> tuple:
    """
    Return the ChemShell input dictionary keys defined by the aiida-chemshell plugin.

    Parameters
    ----------
    key :   str
        The input field to be queried ("sp": "Single Point", "op":
        "Geometry Optimisation", "qm": "Quantum Mechanics", "mm":
        "Molecular Mechanics")

    Returns
    -------
    tuple
        A list of the input dictionary keys for the requested input field
        as defined by the aiida-chemshell plugin.
    """
    try:
        from aiida_chemshell.calculations import ChemShellCalculation
    except ImportError:
        return []
    else:
        if key == "sp":
            return ChemShellCalculation.get_valid_calculation_parameters()
        if key == "op":
            return ChemShellCalculation.get_valid_optimisation_parameters()
        if key == "qm":
            return ChemShellCalculation.get_valid_QM_parameters().keys()
        if key == "mm":
            return ChemShellCalculation.get_valid_MM_parameters().keys()
    return []


def open_link_in_new_tab(path: str, _=None) -> None:
    """
    Open a given link in a new browser tab.

    Parameters
    ----------
    path :  str
        The link to be opened.
    """
    js_code = f"window.open('{path}', '_blank');"
    display(Javascript(js_code))
    return


def test_aiida_chemsh_import() -> bool:
    """
    Test if the aiida-chemshell plugin is installed.

    Returns
    -------
    bool
        True if the aiida-chemshell plugin is installed, False otherwise.
    """
    try:
        import_module("aiida_chemshell")
    except ImportError:
        return False
    except Exception as e:
        raise e
    else:
        return True

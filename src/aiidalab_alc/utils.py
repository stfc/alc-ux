import pathlib 


def getPyAppDir() -> pathlib.Path:
    """
    Returns the absolute path for the AiiDAlab ALC app python package.
    """
    return pathlib.Path(__file__).parent.resolve()

def getAppDir() -> pathlib.Path:
    """
    Returns the absolute path for the root directory of this project where the jupyter notebooks are contained.
    """
    return getPyAppDir() / "../.." 


def getChemShellParams(key: str) -> tuple: 
    """
    Returns the ChemShell input dictionary keys for various input options defined by the aiida-chemshell plugin. 

    Parameters
    ----------
    key:    str 
        The input field to be queried ("sp": "Single Point", "op": "Geometry Optimisation", "qm": "Quantum Mechanics", "mm": "Molecular Mechanics")

    Returns 
    -------
    params: tuple 
        A list of the input dictionary keys for the requested input field as defined by the aiida-chemshell plugin. 
    """
    try:
        from aiida_chemshell.calculations import ChemShellCalculation 
    except ImportError:
        raise ImportError
        return tuple()
    else:
        if   (key == "sp"):
            return ChemShellCalculation.get_valid_calculation_parameters()
        elif (key == "op"):
            return ChemShellCalculation.get_valid_optimisation_parameters()
        elif (key == "qm"):
            return ChemShellCalculation.get_valid_QM_parameters().keys()
        elif (key == "mm"):
            return ChemShellCalculation.get_valid_MM_parameters().keys()
    return tuple()

def openLinkInNewTab(path: str, _ = None) -> None:
    """
    Opens a given link in a new browser tab. 

    Parameters 
    ----------
    path:   str 
        The link to be opened.
    """
    jsCode = f"window.open('{path}', '_blank');"
    from IPython.display import Javascript, display 
    display(Javascript(jsCode))
    return 
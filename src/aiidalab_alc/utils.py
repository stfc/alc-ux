import pathlib 


def getPyAppDir() -> pathlib.Path:
    return pathlib.Path(__file__).parent.resolve()

def getAppDir() -> pathlib.Path:
    return getPyAppDir() / ".." 


def getChemShellParams(key: str) -> tuple: 
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
    jsCode = f"window.open('{path}', '_blank');"
    from IPython.display import Javascript, display 
    display(Javascript(jsCode))
    return 
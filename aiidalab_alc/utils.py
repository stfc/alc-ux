import pathlib 


def getPyAppDir() -> pathlib.Path:
    return pathlib.Path(__file__).parent.resolve()

def getAppDir() -> pathlib.Path:
    return getPyAppDir() / ".." 


def getChemShellParams(cls) -> dict:
    params = {} 
    try:
        from aiida_chemshell import ChemShellCalculation 
    except ImportError:
        return None 
    else:
        params["sp"] = ChemShellCalculation.get_valid_calculation_parameters()
        params["opt"] = ChemShellCalculation.get_valid_optimisation_parameters()
        params["qm"] = ChemShellCalculation.get_valid_QM_parameters()
        params["mm"] = ChemShellCalculation.get_valid_MM_parameters()
    return params  

def openLinkInNewTab(path: str, _ = None) -> None:
    jsCode = f"window.open('{path}', '_blank');"
    from IPython.display import Javascript, display 
    display(Javascript(jsCode))
    return 
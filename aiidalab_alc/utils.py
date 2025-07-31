import pathlib 


def getPyAppDir() -> pathlib.Path:
    return pathlib.Path(__file__).parent.resolve()

def getAppDir() -> pathlib.Path:
    return getPyAppDir() / ".." 

def getCodesDir() -> pathlib.Path:
    return getAppDir() / ".codes" 

def test_import():
    """
    Test whether the python package can be successfully imported. 
    """
    import aiidalab_alc 
    assert aiidalab_alc.__version__ is not None 

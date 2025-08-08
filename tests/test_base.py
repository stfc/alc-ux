"""Test the base python package (i.e. has it been installed correctly)."""

import aiidalab_alc


def test_import():
    """Test whether the python package can be successfully imported."""
    assert aiidalab_alc.__version__ is not None

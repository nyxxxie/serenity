import os
import pytest

RELATIVE_DIR = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture()
def singlestruct():
    """
    This returns the path to the basictemplate.stf file.
    """
    path = os.path.join(RELATIVE_DIR, "testdata", "basictemplate.stf")
    yield path

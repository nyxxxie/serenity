import os
import pytest

RELATIVE_DIR = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture()
def singlestruct():
    """This returns the path to the singlestruct.stf file."""
    path = os.path.join(RELATIVE_DIR, "testdata", "singlestruct.stf")
    yield path

def singlestruct_target():
    """This returns the path to the singlestruct_target file."""
    path = os.path.join(RELATIVE_DIR, "testdata", "singlestruct_target")
    yield path

import os
import pytest
from spade import template
from spade.typesystem.types import int32

RELATIVE_DIR = os.path.dirname(os.path.realpath(__file__))


def get_testdata_file(filename):
    return os.path.join(RELATIVE_DIR, "testdata", filename)

@pytest.fixture()
def comments():
    """This returns the path to the comments.stf file."""
    yield get_testdata_file("comments.stf")

@pytest.fixture()
def emptyfile():
    """This returns the path to the emptyfile.stf file."""
    yield get_testdata_file("emptyfile.stf")

@pytest.fixture()
def emptystruct():
    """This returns the path to the emptystruct.stf file."""
    yield get_testdata_file("emptystruct.stf")

@pytest.fixture()
def incompletefield():
    """This returns the path to the incompletefield.stf file."""
    yield get_testdata_file("incompletefield.stf")

@pytest.fixture()
def singlestruct():
    """This returns the path to the singlestruct.stf file."""
    yield get_testdata_file("singlestruct.stf")

@pytest.fixture()
def singlestruct_target():
    """This returns the path to the singlestruct_target file."""
    yield get_testdata_file("singlestruct_target")

@pytest.fixture()
def multistruct1():
    """This returns the path to the multistruct1.stf file."""
    yield get_testdata_file("multistruct1.stf")

@pytest.fixture()
def multistruct1_target():
    """This returns the path to the multistruct1_target file."""
    yield get_testdata_file("multistruct1_target")

@pytest.fixture()
def staticarrayfield():
    """This returns the path to the multistruct1.stf file."""
    yield get_testdata_file("staticarrayfield.stf")

@pytest.fixture()
def staticarrayfield_target():
    """This returns the path to the multistruct1_target file."""
    yield get_testdata_file("staticarrayfield.bin")

import os
import pytest
from spade import template
from spade.typesystem.types import int32

RELATIVE_DIR = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture()
def singlestruct():
    """This returns the path to the singlestruct.stf file."""
    path = os.path.join(RELATIVE_DIR, "testdata", "singlestruct.stf")
    yield path

@pytest.fixture()
def singlestruct_target():
    """This returns the path to the singlestruct_target file."""
    path = os.path.join(RELATIVE_DIR, "testdata", "singlestruct_target")
    yield path

@pytest.fixture()
def multistruct():
    """This returns the path to the multistruct.stf file."""
    path = os.path.join(RELATIVE_DIR, "testdata", "multistruct.stf")
    yield path

@pytest.fixture()
def multistruct_target():
    """This returns the path to the multistruct_target file."""
    path = os.path.join(RELATIVE_DIR, "testdata", "multistruct_target")
    yield path

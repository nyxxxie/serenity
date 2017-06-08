import os
import pytest
from shutil import copyfile
from spade.core.project import Project

RELATIVE_DIR = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture()
def basictemplate():
    """
    This returns the path to the basictemplate.stf file.
    """
    path = os.path.join(RELATIVE_DIR, "testdata", "basictemplate.stf")
    yield path

@pytest.fixture()
def emptytemplate():
    """
    This returns the path to the emptytemplate.stf file.
    """
    path = os.path.join(RELATIVE_DIR, "testdata", "emptytemplate.stf")
    yield path

@pytest.fixture()
def templatewithstructs():
    """
    This returns the path to the templatewithstructs.stf file.
    """
    path = os.path.join(RELATIVE_DIR, "testdata", "templatewithstructs.stf")
    yield path

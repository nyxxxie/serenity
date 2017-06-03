import os
import pytest
from shutil import copyfile
from spade.core.project import Project

DB_FILE = "testdb.sdb"
RELATIVE_DIR = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture()
def testfile1():
    """
    This fixture creates a copy of testfile1 that can be read and written to
    and yields a usable path to it.  It also deletes the file when the test
    concludes.
    """
    # copy test file from template, yield path
    orig_path = os.path.join(RELATIVE_DIR, "testdata", "testfile1")
    path = "_testfile1"
    copyfile(orig_path, path)
    yield path
    if os.path.exists(path): # We might have already deleted the file in a test
        os.remove(path)

@pytest.fixture()
def testfile2():
    """
    This fixture creates a copy of testfile2 that can be read and written to
    and yields a usable path to it.  It also deletes the file when the test
    concludes.
    """
    # copy test file from template, yield path
    orig_path = os.path.join(RELATIVE_DIR, "testdata", "testfile2")
    path = "_testfile2"
    copyfile(orig_path, path)
    yield path
    if os.path.exists(path): # We might have already deleted the file in a test
        os.remove(path)

@pytest.fixture()
def project():
    """
    This fixture creates and yields a project for use in tests.
    """
    project = Project(DB_FILE)
    yield project
    os.remove(DB_FILE)


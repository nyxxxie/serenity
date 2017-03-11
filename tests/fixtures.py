import os
import pytest
from shutil import copyfile
from spade.core.project import Project

dbfile = "testdb.sdb"

@pytest.fixture()
def testfile1():
    """
    This fixture creates a copy of testfile1 that can be read and written to
    and yields a usable path to it.  It also deletes the file when the test
    concludes.
    """
    # copy test file from template, yield path
    orig_path = "tests/resources/testfile1"
    path = "testfile1"
    copyfile(orig_path, path)
    yield path
    os.remove(path)

@pytest.fixture()
def testfile2():
    """
    This fixture creates a copy of testfile2 that can be read and written to
    and yields a usable path to it.  It also deletes the file when the test
    concludes.
    """
    # copy test file from template, yield path
    orig_path = "tests/resources/testfile1"
    path = "testfile2"
    copyfile(orig_path, path)
    yield path
    os.remove(path)

@pytest.fixture()
def project():
    """
    This fixture creates and yields a project for use in tests.
    """
    project = Project(dbfile)
    yield project
    os.remove(dbfile)

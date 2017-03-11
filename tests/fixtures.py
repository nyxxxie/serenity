import os
import pytest
from shutil import copyfile
from spade.core.project import Project

dbfile = "testdb.sdb"

@pytest.fixture()
def testfile1():
    # copy test file from template, yield path
    orig_path = "tests/resources/testfile1"
    path = "testfile1"
    copyfile(orig_path, path)
    yield path
    os.remove(path)

@pytest.fixture()
def testfile2():
    # copy test file from template, yield path
    orig_path = "tests/resources/testfile1"
    path = "testfile2"
    copyfile(orig_path, path)
    yield path
    os.remove(path)

@pytest.fixture()
def project():
    project = Project(dbfile)
    yield project
    os.remove(dbfile)

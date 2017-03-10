import os
import pytest
from shutil import copyfile
from spade.core.file import sfile
from spade.core.project import Project

@pytest.fixture()
def testfile1():
    # copy test file from template, yield path
    orig_path = "tests/resources/testfile1"
    path = "testfile1"
    copyfile(orig_path, path)
    yield path
    os.remove(path)

@pytest.fixture()
def project():
    dbfile = "dbfile.sdb"
    project = Project(dbfile)
    yield project
    os.remove(dbfile)

def testfile1_openclose1(testfile1, project):
    f = project.open_file(testfile1)
    assert f is not None
    assert type(f) is sfile
    f.close()
    assert f._closed

def testfile1_openclose2(testfile1, project):
    with project.open_file(testfile1) as f:
        assert f is not None
        assert type(f) is sfile
    assert f._closed

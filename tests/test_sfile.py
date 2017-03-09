import pytest
from shutil import copyfile
from spade.core.project import Project

@pytest.fixture()
def testfile1():
    print("PRE-TEST")
    # copy test file from template, yield path
    orig_path = "tests/resources/testfile1"
    path = "testfile1"
    copyfile(orig_path, path)
    yield path

    print("POST-TEST")
    os.remove(path)

def testfile1_open():
    pass

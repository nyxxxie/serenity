from spade.core.file import SFile
from spade.core.project import Project
from tests.core.fixtures import testfile1, project

def testfile1_openclose1(testfile1, project):
    f = project.open_file(testfile1)
    assert f
    assert isinstance(f, SFile)
    f.close()
    assert f._closed

def testfile1_openclose2(testfile1, project):
    with project.open_file(testfile1) as f:
        assert f
        assert isinstance(f, SFile)
    assert f._closed

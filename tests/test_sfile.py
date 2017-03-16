from spade.core.file import sfile
from spade.core.project import Project
from .fixtures import testfile1, project

# NOTE: just test the specific functions implemented for sfile, don't test write and etc until we modify it

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

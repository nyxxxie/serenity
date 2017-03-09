import os
import pytest
from spade.core.project import Project
from .utils.project_sql import check_table

dbfile = "testdb.sdb"

@pytest.fixture()
def cleanup():
    print("PRE-TEST")
    yield
    print("POST-TEST")
    if os.path.isfile(dbfile):
        os.remove(dbfile)

def test_project_initialization(cleanup):
    project = Project(dbfile)
    assert project is not None

    # Verify default tables exist
    assert check_table(dbfile, "project_info")
    assert check_table(dbfile, "files")

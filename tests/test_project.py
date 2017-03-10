import os
import pytest
from spade.core.project import Project
from .utils.project_sql import check_table

dbfile = "testdb.sdb"

@pytest.fixture()
def cleanup():
    yield
    if os.path.isfile(dbfile):
        os.remove(dbfile)

@pytest.mark.usefixtures("cleanup")
def test_project_initialization():
    project = Project(dbfile)
    assert project is not None

    # Verify default tables exist
    assert check_table(dbfile, "project_info")
    assert check_table(dbfile, "project_files")

@pytest.mark.usefixtures("cleanup")
def test_project_reopen():
    project = Project(dbfile)
    assert project is not None

    # Verify default tables exist
    assert check_table(dbfile, "project_info")
    assert check_table(dbfile, "project_files")

    # Reopen project
    project = Project(dbfile)
    assert project is not None

    # Verify default tables exist
    assert check_table(dbfile, "project_info")
    assert check_table(dbfile, "project_files")

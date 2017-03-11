import os
import pytest
from shutil import copyfile
from spade.core.file import sfile, filemode
from spade.core.project import Project, SCHEMA_VERSION
from .utils.project_sql import check_table
from .fixtures import testfile1, testfile2, project

def test_project_initialization(testfile1, project):
    assert project is not None
    dbfile = project.db_file

    # Verify default tables exist
    assert check_table(dbfile, "project_info")
    assert check_table(dbfile, "project_files")

def test_project_reopen(testfile1, project):
    assert project is not None
    dbfile = project.db_file

    # Verify default tables exist
    assert check_table(dbfile, "project_info")
    assert check_table(dbfile, "project_files")

    # Reopen project
    project = Project(dbfile)
    assert project is not None

    # Verify default tables exist
    assert check_table(dbfile, "project_info")
    assert check_table(dbfile, "project_files")

def test_project_check_files(testfile1, testfile2, project):
    assert project is not None

    # Open files
    f1 = project.open_file(testfile1, filemode.read)
    assert f1 is not None
    f2 = project.open_file(testfile2, filemode.read)
    assert f2 is not None

    paths = project.files()
    assert len(paths) == 2
    assert testfile1 in paths
    assert testfile2 in paths

def test_project_get_all_info(project):
    assert project is not None
    info = project.get_info()
    assert info is not None
    assert len(info) == 3
    assert info["schema_version"] == SCHEMA_VERSION

def test_project_get_info(project):
    assert project is not None
    version = project.get_info("schema_version")
    assert version is not None
    assert version == SCHEMA_VERSION

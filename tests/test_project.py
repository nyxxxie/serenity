import os
import pytest
from shutil import copyfile
from spade.core.file import sfile, filemode
from spade.core.project import Project, SpadeProjectException, SCHEMA_VERSION
from .utils.project_sql import check_table
from .fixtures import testfile1, testfile2, project, dbfile

def test_initialization(testfile1, project):
    assert project is not None
    dbfile = project.db_file

    # Verify default tables exist
    assert check_table(dbfile, "project_info")
    assert check_table(dbfile, "project_files")

def test_reopen(project):
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

def test_fail_reopen_not_a_db(testfile1):
    caught = False
    try:
        project = Project(testfile1) # Ideally, this file shouldn't be a sqlite db
    except Exception as e:
        caught = True

    assert caught

def test_fail_reopen_unsupported_schema_ver(project):
    pass # TODO: make a project with a messed up version, then try to reopen it

def test_open_files(testfile1, testfile2, project):
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

def test_fail_modified_file(testfile1, testfile2, project):
    assert project is not None

    # Open file (and thereby register it in the project)
    f1 = project.open_file(testfile1, filemode.read)
    assert f1 is not None
    f1.close()

    # Simulate modifying the file externally
    with open(testfile1, "wb+") as f:
        f.write(b"DO YOU BELIEVE IN SOCIETY'S LIES??")

    # Try to open new project and check to see if this fails
    caught = False
    try:
        project = Project(dbfile)
    except SpadeProjectException as e:
        caught = True

    assert caught

def test_fail_deleted_file(testfile1, project):
    assert project is not None

    # Open file (and thereby register it in the project)
    f1 = project.open_file(testfile1, filemode.read)
    assert f1 is not None
    f1.close()

    # Simulate an external delete
    os.remove(testfile1)

    caught = False
    try:
        project = Project(dbfile)
    except SpadeProjectException as e:
        caught = True

    assert caught

def test_get_all_info(project):
    assert project is not None
    info = project.get_info()
    assert info is not None
    assert len(info) == 3
    assert info["schema_version"] == SCHEMA_VERSION

def test_get_specific_info(project):
    assert project is not None
    version = project.get_info("schema_version")
    assert version is not None
    assert version == SCHEMA_VERSION

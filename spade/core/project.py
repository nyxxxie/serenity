import sqlite3

class Project:
    """Represents an open session for spade."""

    def __initialize_db(self, db):
        """
        Creates default tables for a newly created spade project
        """

        # Get cursor for db
        c = db.cursor()

        # Execute initialization query
        rc = db.execute("""
        PRAGMA foreign_keys = ON; -- need this to use foreign keys

        CREATE TABLE project_info(
            key TEXT UNIQUE,
            val TEXT
        );

        CREATE TABLE files(
            id   INT AUTO_INCREMENT,
            path TEXT,           -- relative or absolute path to this file
            hash BLOB,           -- sha256 hash of file contents on last change
            head_change BLOB,    -- head change the file is at.  default NULL
            UNIQUE (path),
            PRIMARY KEY (id)
        );

        CREATE TABLE changes(
            file_id INTEGER,     -- file_id of the file we apply changes to
            hash        BLOB,    -- sha256 of this change
            parent      BLOB,    -- sha256 of parent (previous) change
            file_pos,   INTEGER,
            change_type INTEGER, -- '+' = insert, '-' = erase, '!' = replace
            change      BLOB,    -- bytes that were inserted or erased
            FOREIGN KEY (file_id) REFERENCES files (id)
            UNIQUE (hash)
        );

        CREATE TABLE changes_comments(
            hash    BLOB,        -- sha256 of the change this comment refers to
            comment TEXT,
            FOREIGN KEY (hash) REFERENCES changes (hash)
        );
        """)

    def __create_db(self, dbfile):
        db = sqlite3.connect(dbfile)
        return db;

    def __init__(self, dbfile):
        self.__dbfile = dbfile
        self.__db = self.__create_db(dbfile)
        # must send query PRAGMA foreign_keys = ON;

    def add_file(self, path):
        """
        Adds a file to the project.  Fails on adding duplicate files.  Can take
        both the path to a valid file and a currently open file object.
        """
        pass

    def remove_file(self, f):
        """
        Removes a file from the project.
        """
        pass

    def db(self):
        return self.__db

    def files(self):
        """
        Returns a list of files in the project.  Does not print files that have been added but closed.
        """
        pass

    def add_template(self, template):
        """
        Adds a template to the project.  Fails on adding duplicate templates.
        Can take both the path to a valid file and a currently open file object.
        """
        pass

    def remove_template(self, template):
        """
        Remove template from project.
        """
        pass

    def templates(self):
        """
        Returns a list of templates in the project.
        """
        pass

    def set_template_for_file(self, f, template):
        """
        Associates a template with a file.
        """
        pass

    def get_template_for_file(self, f, template):
        """
        Gets the associated template for a file.
        """
        pass

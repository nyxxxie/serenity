import sqlite3

class Project:
    """Represents an open session for spade."""

    def __create_db_default_tables(self, dbfile):
        c = self.db.cursor()
        c.execute("""
        CREATE TABLE files
        (path TEXT,
         hash BINARY(32),  # sha256 hash of file contents on first add
         head BINARY(32),  # head of change the file is set to, default NULL
         PRIMARY KEY(hash));
        """)
        c.execute("""
        CREATE TABLE changes
        (file   BINARY(32),  # sha256 of file we apply changes to
         this   BINARY(32),  # sha256 of this change
         parent BINARY(32),  # sha256 of parent (previous) change
         at     BIGINT,      # position (relative to parent) change is at
         type   BIT,         # '0' = insertion, '1' = erasure
         change BLOB,        # bytes that were inserted or erased
         com    TEXT,        # user's comment, annotation or whatever else
         FOREIGN KEY (file) REFERENCES files (hash));
        """)

    def __create_db(self, dbfile):
        return sqlite3.connect(self.dbfile)

    def __init__(self, dbfile):
        self.dbfile = dbfile;
        self.db = self.__create_db(dbfile)
        # must send query PRAGMA foreign_keys = ON;

    def _add_file(self, f):
        """
        Adds a file to the project.  Fails on adding duplicate files.  Can take
        both the path to a valid file and a currently open file object.
        """
        pass

    def _remove_file(self, f):
        """
        Removes a file from the project.
        """
        pass

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

    def set_template_for_file(self, f, template):
        """
        Associates a template with a file.
        """

    def get_template_for_file(self, f, template):
        """
        Gets the associated template for a file.
        """

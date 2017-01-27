import sqlite3

class Project:
    """Represents an open session for spade."""

    def __create_db_default_tables(self):
        self.db.execute("""
        CREATE TABLE project_info
        (key TEXT UNIQUE,
         val TEXT);
        """)
        self.db.execute("""
        CREATE TABLE files
        (id          INT AUTO_INCREMENT,
         path        TEXT,
         hash        BINARY(32),  -- sha256 hash of file contents on last change
         head_change BINARY(32),  -- head change the file is at.  default NULL
         UNIQUE (path),
         PRIMARY KEY (id));
        """)
        self.db.execute("""
        CREATE TABLE changes
        (id          INT,         -- id of the file we apply changes to
         hash        BINARY(32),  -- sha256 of this change
         parent      BINARY(32),  -- sha256 of parent (previous) change
         file_pos    BIGINT,
         change_type CHARACTER,   -- '+' = insert, '-' = erase, '!' = replace
         change      BLOB,        -- bytes that were inserted or erased
         PRIMARY KEY (id, hash),
         FOREIGN KEY (id) REFERENCES files (id));
        """)
        self.db.execute("""
        CREATE TABLE changes_comments
        (id      INT,
         hash    BINARY(32),
         comment TEXT,
         UNIQUE (id, hash),
         FOREIGN KEY (id, hash) REFERENCES changes (id, hash));
        """)

    def __create_db(self):
        return sqlite3.connect(self.dbfile)

    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.db = self.__create_db()
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

    def db(self):
        return db

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

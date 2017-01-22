import sqlite3

class Project:
    """Represents an open session for spade."""

    def __create_db_default_tables(self, dbfile):
        pass

    def __create_db(self, dbfile):
        pass

    def __init__(self, dbfile):
        self.name   = name;
        self.dbfile = dbfile;
        self.db = sqlite3.connect(self.dbfile)

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

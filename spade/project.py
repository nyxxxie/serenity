import sqlite3

class Project:
    """Represents an open session for spade."""

    def __init__(self, name="(default)", dbfile=":memory:"):
        self.name   = name;
        self.ismem  = (dbfile == ":memory:")
        self.dbfile = dbfile;
        self.db = sqlite3.connect(self.dbfile)

    def save(self, dbfile):
        """
        Saves the state of a project to a file.
        """
        pass

    def load(self, dbfile):
        """
        Loads a project from a stored .sdb saved using the save() function.
        """
        pass

    def add_file(self, f):
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

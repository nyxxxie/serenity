import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Binary, Integer, String, ForeignKey

class Project:
    """Represents an open session for spade."""

    def __init_db(self, engine):
        """
        Creates default tables for a newly created spade project
        """
        metadata = MetaData()

        # Define project_info table
        self.table_pinfo = Table("project_info", metadata,
            Column("key", String, primary_key=True),
            Column("value", String)
        )

        # Define files table
        self.table_files = Table("files", metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("path", String, unique=True),                # Relative or absolute path to this file
            Column("hash", Binary),                             # sha256 hash of file contents on last change
            Column("head_change", Binary, server_default=None), # head change file is at
        )

        # Define changes table
        self.table_changes = Table("changes", metadata,
            Column("file_id", None, ForeignKey("files.id")),    # id of file we apply changes to
            Column("hash", Binary),                             # sha256 of this change
            Column("parent", Binary),                           # sha256 of previous change
            Column("file_pos", Integer),                        # position in file where change occured
            Column("change_type", Integer),                     # change type (TODO: make this enum).  '+' = insert, '-' = erase, '!' = replace
            Column("change", Binary)                            # bytes that were inserted or erased
        )

        # Define change_comments table
        self.table_change_comments = Table("change_comments", metadata,
            Column("change", None, ForeignKey("changes.hash")), # hash of the change this comment refers to
            Column("text", String)                              # comment text
        )

        # Add all tables to the database
        metadata.create_all(engine)

        return True

    def __add_info(self, key, value, nomodify=False):
        # TODO: handle nomodify var
        ins = self.table_pinfo.insert()
        conn = self.__db_engine.connect()
        conn.execute(ins, key=key, value=value) # TODO: might cause problems?

    def __init__(self, dbfile):
        self.__dbfile = dbfile
        self.__db_engine = create_engine("sqlite:///"+dbfile)
        self.__init_db(self.__db_engine)
        self.__add_info("schema_version", "1")
        date = datetime.datetime.now()
        self.__add_info("creation_datetime", date, True)
        self.__add_info("update_datetime", date)

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

    def db_engine(self):
        return self.__db_engine

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

import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Binary, Integer, String, ForeignKey

SCHEMA_VERSION = "0.0a"


class ProjectException(Exception):

    pass


class Project:
    """Represents an open session for spade."""

    def __init__(self, dbfile):
        self.__dbfile = dbfile
        self.__db_engine = create_engine("sqlite:///"+dbfile)
        self.__init_db(self.__db_engine)
        self.__add_info("schema_version", "1")
        self.__add_info("creation_datetime", datetime.datetime.now(), True)
        self.__add_info("update_datetime", datetime.datetime.now())

    def db(self):
        return self._db

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
        Returns a list of files in the project.  Does not print files that
        have been added but closed.
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

    def __add_info(self, key, value, nomodify=False):
        # TODO(nyxxxie): handle nomodify var
        ins = self.table_pinfo.insert()
        conn = self.__db_engine.connect()
        conn.execute(ins, key=key, value=value) # TODO: might cause problems?

    def __init_db(self, engine):
        """
        Creates default tables for a newly created spade project
        """
        file_hash_len = 256/8
        change_hash_len = 256/8
        metadata = MetaData()
        # Define project_info table
        self.table_pinfo = Table("project_info", metadata,
            Column("key", String, primary_key=True),
            Column("value", String)
        )
        # Define files table
        self.table_files = Table("files", metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            # Relative or absolute path to this file
            Column("path", String, unique=True),
            # sha256 hash of file contents on last change
            Column("hash", Binary),
            # head change file is at
            Column("head_change", Binary, server_default=None)
        )
        # Define changes table
        self.table_changes = Table("changes", metadata,
            # id of file we apply changes to
            Column("file_id", None, ForeignKey("files.id")),
            # sha256 of this change
            Column("hash", Binary),
            # sha256 of previous change
            Column("parent", Binary),
            # position in file where change occured
            Column("file_pos", Integer),
            # NOTE(fst3a): Already solved this
            # change type.  '+' = insert, '-' = erase, '!' = replace
            Column("change_type", Integer),
            # bytes that were inserted or erased
            Column("change", Binary)
        )
        # FIXME(fst3a): This is plain wrong, one project can have multiple files
        # and two or more files can have exactly same change hashes that would
        # collide in current scheme.  Therefore, this table is still undecided
        # and should not be created in Project db yet.  NOTE: the ForeignKey
        # should be made compound out of "files.id" and "changes.hash".
        #
        # # Define change_comments table
        # self.table_change_comments = Table("change_comments", metadata,
        #     # hash of the change this comment refers to
        #     Column("change", None, ForeignKey("changes.hash")),
        #     # comment text
        #     Column("text", String)
        # )
        #
        # Add all tables to the database
        metadata.create_all(engine)
        return True

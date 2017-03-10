import datetime
import hashlib
from .file import sfile, filemode
from sqlalchemy import create_engine, MetaData, Table, Column, Binary, Integer, String, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy import sql

SCHEMA_VERSION = "0.1"

class SpadeProjectException(Exception): pass

class Project:
    """Represents an open session for spade."""

    def __init__(self, dbfile):
        # TODO: specify that dbfile is a temporary storage file, can be :memory:
        self._dbfile = dbfile
        self._engine = create_engine("sqlite:///" + dbfile, echo=True)
        self._init_db()
        self._update_project_info()

    def save(self, path: str=None):
        if path is None:
            path = self._dbfile

        if path == ":memory:":
            raise SpaceProjectException("Can't save to memory-mapped database...")

        raise SpadeProjectException("Can't save project, operation not implemented.")

    def open_file(self, path: str, mode: filemode=filemode.rw):
        return sfile(self, path, mode)

    def db_engine(self):
        return self._engine

    def files(self):
        """
        Returns a list of files in the project.  Tuple format is (id, path,
        contents hash, base change, head change).
        """
        s = sql.select([table_files.path])

        paths = []
        with self.db_engine().connect() as conn:
            conn.execute(ins)
        result = con

        return paths

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

    def _add_info(self, key, value, update=False):
        ins = self.table_pinfo.insert().values(
            key=key,
            value=value)

        with self.db_engine().connect() as conn:
            conn.execute(ins)

    def _register_file(self, path, hash_):
        ins = self.table_files.insert().values(
            path=path,
            hash=hash_)

        with self.db_engine().connect() as conn:
            conn.execute(ins)

    def _init_db(self):
        """
        Table metadata creation.
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
            # Relative or absolute path to this file
            Column("path", String),
            # sha256 hash of file contents on last change
            Column("hash", Binary(32)),
        )

        # Add all tables to the database
        metadata.create_all(self.db_engine())

        return True

    def _update_project_info(self):
        date = datetime.datetime.now()
        if self._engine.has_table("project_info"):
            self._add_info("schema_version", SCHEMA_VERSION)
            self._add_info("creation_datetime", date, nomodify=True)
            self._add_info("update_datetime", date)
        else:
            self._add_info("update_datetime", date)

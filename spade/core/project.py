import datetime
import hashlib

from sqlalchemy import create_engine, MetaData, Table, Column, Binary, Integer, String, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.sql import select

from . import file

SCHEMA_VERSION = "0.0"


class SpadeProjectException(Exception): pass

class Project:
    """Represents an open session for spade."""

    def __init__(self, dbfile):
        self._dbfile = dbfile
        self._db_engine = create_engine("sqlite:///" + dbfile, echo=True)
        self._init_db()
        self._add_info("schema_version", SCHEMA_VERSION)
        date = datetime.datetime.now()
        self._add_info("creation_datetime", date, nomodify=True)
        self._add_info("update_datetime", date)
        # TODO: Enable VACUUM

    def add_file(self, path):
        pass

    def open_file(self, path, mode):
        pass

    def db_engine(self):
        pass

    def files(self):
        """
        Returns a list of files in the project.  Tuple format is (id, path,
        contents hash, base change, head change).
        """
        sel = select([self.table_files.c.id,
                      self.table_files.c.path, self.table_files.c.hash,
                      self.table_files.c.base, self.table_files.c.head])
        # if ids is not None:
        #     sel = sel.where(self.table_files.c._id.in_(ids))
        with self.db_engine().connect() as conn:
            result = conn.execute(sel)
            files = list(result)
            result.close()
            return files

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

    def _add_info(self, key, value, nomodify=False):
        # TODO(nyxxxie): handle nomodify var
        ins = self.table_pinfo.insert() \
                              .values(key=key, value=value)
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
            # base change file is at
            Column("base", Binary(32), server_default=None),
            # head change file was left at
            Column("head", Binary(32), server_default=None)
        )
        # Define changes table
        self.table_changes = Table("changes", metadata,
            # id of file we apply changes to
            Column("file_id", None),
            # sha256 of this change
            Column("hash", Binary(32)),
            # sha256 of previous change
            Column("parent", Binary(32)),
            # position in file where change occured
            Column("file_pos", Integer),
            # change type.  '+' = insert, '-' = erase, '!' = replace
            Column("change_type", String(1)),
            # bytes that were inserted or erased
            Column("change", Binary),
            # hash must be unique for each file
            UniqueConstraint("file_id", "hash"),
            # update changes tree if parent record in files is updated
            # FIXME(fst3a): this doesn't work, changes stay there
            ForeignKeyConstraint(["file_id"], ["files.id"],
                                 onupdate="CASCADE",
                                 ondelete="CASCADE")
        )
        # Add all tables to the database
        metadata.create_all(self.db_engine())
        return True

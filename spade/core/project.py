import datetime
import hashlib

from sqlalchemy import create_engine, MetaData, Table, Column, Binary, Integer, String, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.sql import select

from . import file

SCHEMA_VERSION = "0.0"


class ProjectException(Exception):

    pass


class ProjectDBException(ProjectException):

    pass


class ProjectIOException(ProjectException):

    pass


class ProjectFileAlteredException(ProjectException):

    pass


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
        """
        Adds a file to the project.  Fails on adding duplicate files.  Can take
        both the path to a valid file and a currently open file object.
        """
        try:
            with open(path, "rb") as f:
                hasher = hashlib.sha256()
                for chunk in iter(lambda: f.read(0x1000), b""):
                    hasher.update(chunk)
                ins = self.table_files.insert() \
                                      .values(path=path, hash=hasher.digest())
                with self.db_engine().connect() as conn:
                    result = conn.execute(ins)
                    (id,) = result.inserted_primary_key
                    return id
        except OSError as e:
            raise ProjectIOException("Failed to add file (" + e.msg + ")")

    def open_file(self, id, mode, primary=False, cache=(1024, 0x1000)):
        """
        Opens a file specified by id in mode with cache tuple (number of pages,
        size of each page).  Primary _File will update head on any new change.
        """
        if mode not in (file.RDONLY, file.RDWR):
            raise ProjectIOException("Bad mode")
        sel = select([self.table_files.c.path, self.table_files.c.hash,
                      self.table_files.c.base, self.table_files.c.head]) \
              .where(self.table_files.c.id == id) \
              .limit(1)
        row = None
        with self.db_engine().connect() as conn:
            result = conn.execute(sel)
            row = result.first()
            result.close()
        if row is None:
            raise ProjectDBException("No record of file in DB")
        (path, hash, base, head) = row
        if path is None:
            if mode != file.RDONLY:
                raise ProjectIOException("No-path files can only be read")
            return file.File(self, id, None, base, head,
                             file.RDONLY, primary, cache)
        try:
            fd = open(path, mode, buffering=0)
        except OSError as e:
            raise ProjectIOException("Failed to open file (" + e.msg + ")")
        else:
            try:
                if not fd.seekable():
                    raise ProjectIOException("Must be seekable")
                assert fd.tell() == 0
                hasher = hashlib.sha256()
                for chunk in iter(lambda: fd.read(0x1000), b""):
                    hasher.update(chunk)
                if hasher.digest() != hash:
                    raise ProjectFileAlteredException("File was altered")
                return file._File(self, id, fd, base, head,
                                    mode, primary, cache)
            except ProjectException as e:
                fd.close()
                raise

    def del_file(self, id) -> bool:
        """
        Returns True if delete was successful.
        """
        return self.del_files([id]) == 1

    def del_files(self, ids):
        """
        Removes files in from the project.  Returns number of files removed.
        """
        # FIXME(fst3a): Corresponding changes are not cascadely removed
        delet = self.table_files.delete(self.table_files.c.id.in_(ids))
        with self.db_engine().connect() as conn:
            return conn.execute(delet).rowcount

    def db_engine(self):
        return self._db_engine

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

import os
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .file import sfile, filemode, hash_file
from .models.project import Base, ProjectInfo, ProjectFile

SCHEMA_VERSION = "0.1"

class SpadeProjectException(Exception): pass

class Project:
    """
    Stores the state and data of a Spade session.  Specifically, a project
    stores information on files that were opened, templates, and file metadata.
    Additionally, any data saved by plugins, analysis, etc is stored in a
    project.  Projects by default store this data directly on disk in a sqlite
    database.
    """

    def __init__(self, dbfile):
        self._db_init(dbfile)

    def __str__(self):
        return "<project (dbfile=\"%s\")>" % (self.db_file)

    def open_file(self, path: str, mode: filemode=filemode.rw) -> sfile:
        """
        Opens a file to be tracked by this project.

        :param path: Path to file that should be opened.
        :type  path: str
        :param mode: Mode to open file in (default: read/write).
        :type  mode: :ref:`filemode <file>`
        :return: A :ref:`sfile <file>` object corresponding to the file.
        """
        return sfile(self, path, mode)

    def db_engine(self):
        """
        Returns the sqlalchemy engine currently in use.

        :return: sqlalchemy engine currently in use.
        """
        return self._engine

    def files(self):
        """
        Returns a list of all files tracked by the project.

        :return: A list of all files tracked by the project.
        """
        paths = []
        for entry in self._db_get_files():
            paths.append(entry.path)

        return paths

    def get_info(self, key: str=None):
        """
        Retrieves information about the project (schema version, database path,
        etc).  If no key is specified, this function will return a list of all
        project info available.

        :param key: Key cooresponding to information item to fetch.  If this is
                    None, function will return a map of all info items in the
                    project.
        :type key: str
        :return: The value associated with a key, if given, or a map of all info
                 items in the project.
        """
        # Create db session
        Session = sessionmaker(bind=self._db_engine)
        session = Session()

        if key is None:
            info = {}
            for row in session.query(ProjectInfo):
                info[row.key] = row.value
            return info
        else:
            entry = session.query(ProjectInfo).filter_by(key=key).first()
            if entry is not None:
                return entry.value

        return None

    def _add_info(self, key, value):
        # Create db session
        Session = sessionmaker(bind=self._db_engine)
        session = Session()

        # Add info to table
        info = ProjectInfo(key=key, value=value)
        session.merge(info)
        session.commit()

    def _db_get_files(self):
        # Create db session
        Session = sessionmaker(bind=self._db_engine)
        session = Session()

        # Add info to table
        return session.query(ProjectFile)

    def _register_file(self, path, file_hash):
        # Create db session
        Session = sessionmaker(bind=self._db_engine)
        session = Session()

        # Add info to table
        info = ProjectFile(path=path, sha256=file_hash)
        session.merge(info)
        session.commit()

    def _update_file_hash(self, path, file_hash):
        # Create db session
        Session = sessionmaker(bind=self._db_engine)
        session = Session()

        entry = session.query(ProjectFile).filter_by(path=path).first()
        if entry is None:
            assert SpadeProjectException("Can't update hash, no file registered at \"%s\"." % path)
        entry.sha256 = file_hash

        session.commit()

    def _db_init(self, path: str):
        # Create engine
        engine = create_engine(
            "sqlite:///" + path,         # Create sqlite db and engine for sqlalchemy
            echo=False)                  # TODO: This should probably be commented out at some point
        Base.metadata.create_all(engine) # Adds all of our tables into the sqlite db
        self.db_file = path
        self._db_engine = engine

        # Initialize database or load info
        date = datetime.datetime.now()
        if self.get_info("schema_version") is None:
            self._add_info("schema_version", SCHEMA_VERSION)
            self._add_info("creation_datetime", date)
            self._add_info("update_datetime", date)
        else:
            self._db_validate()
            self._db_update()

    def _db_validate(self):
        # Make sure project version string is compatible with this version of spade
        schema_version = self.get_info("schema_version")
        if schema_version != SCHEMA_VERSION:
            raise SpadeProjectException("Project schema version \"%s\" is incompatible with this version of spade." % schema_version)

        # Make sure all files tracked by his project exist and match their stored hashes
        for entry in self._db_get_files():
            # Make sure file exists
            if not os.path.exists(entry.path):
                raise SpadeProjectException("Could not find tracked file \"%s\"." % entry.path)

            # Make sure file hash matches
            if hash_file(entry.path) != entry.sha256:
                raise SpadeProjectException("File \"%s\" has been modified since last open." % entry.path)

    def _db_update(self):
        if self.get_info("schema_version") is None:
            raise SpadeProjectException("Can't update uninitialized database.")

        date = datetime.datetime.now()
        self._add_info("update_datetime", date)


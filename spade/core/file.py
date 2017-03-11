import hashlib

class SpadeFileException(Exception): pass

class filemode:
    read = "rb"
    write = "wb"
    rw = "wb+"

class sfile:
    """
    Provides an interface to files that is similar to the built-in file type.
    This is required so that the main project class can catch changes to files
    it is tracking.  This also allows for implementing features like change
    history and undo/redo later on.  This class should not be used directly,
    instead use project's open_file method.

    Implementation wise, despite the fact that sfile aims to be a transparent
    wrapper over the built-in file class, we currently reimplement similar
    methods over simply subclassing file.  This is done to place some limits on
    how files can be opened, as well as allows us to assure that any future
    versions of the builtin file type don't add in new functions that evade our
    hooks that plugin developers might use.
    """

    def __init__(self, project, path: str, mode: filemode=filemode.rw):
        self.path = path
        self.mode = mode
        self.project = project
        self._closed = False
        self._file = open(path, mode)
        project._register_file(path, self.sha256())

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def __repr__(self):
        return "<sfile \"%s\">" % self.path

    def __str__(self):
        return self.__repr__()

    def close(self):
        """
        Closes a file.
        """
        self._closed = True
        self._file.close()

    def size(self) -> int:
        """
        Returns the size of the file in bytes.

        :return: Size of file in bytes.
        """
        return os.stat(self.path).st_size

    def tell(self) -> bytes:
        """
        Indicates where the cursor for this file is currently positioned.
        """
        return self._file.tell()

    def seek(self, offset: int=0, from_what: int=0):
        """
        Sets the cursor position relative to some position.

        :param offset: Offset into file relative to from_what parameter.
        :param from_what: Determines what the above offset is relative to.
        :type offset: int
        :type from_what: int
        :return: Cursor position after the seek operation completes.

        The reference point specified by the ``from_what`` parameter should
        take on one of the following values:

            * 0 - Offset from beginning of file.
            * 1 - Offset from current cursor position.
            * 2 - Offset from end of file.

        This parameter may be omitted, and will default to 0 (beginning of
        file).

        """
        return self.seek(offset, from_what)

    def read(self, size: int=None) -> bytes:
        """
        Reads bytes from file.
        """
        return self._file.read(size)

    def write(self, data: bytes):
        """
        Writes bytes to file.
        """
        return self._file.write(data)

    def insert(self, data: bytes):
        """
        Insert bytes into file starting at the current cursor position.
        """
        assert SpaceFileException("Operation \"insert\" unimplemented...")

    def replace(self, data: bytes):
        """
        Replaces bytes in file starting at the current cursor position.
        """
        return self._file.write(data)

    def erase(self, size: int=None):
        """
        Deletes bytes from file.
        """
        assert SpaceFileException("Operation \"erase\" unimplemented...")

    def sha256(self):
        """
        Calculates the sha256 hash of the file.
        """
        m = hashlib.sha256()
        m.update(self._file.read())
        return m.digest()

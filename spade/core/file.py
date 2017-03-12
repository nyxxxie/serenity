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

    def save(self):
        """
        Saves a file that has been modified.  This is requied because, even
        though in the current implementation of sfile we write directly to the
        file on disk, we must inform the project that we've updated it.
        """
        pass

    def close(self, save: bool=True):
        """
        Closes a file.

        :param save: Determines if we should automatically save this file on close.
        :type save: bool
        """
        # Save file before we close it
        if save:
            self.save()

        # Close file and indicate that we've done so
        self._file.close()
        self._closed = True

    def size(self) -> int:
        """
        Returns the size of the file in bytes.

        :return: Size of file in bytes.
        """
        return os.stat(self.path).st_size

    def tell(self) -> int:
        """
        Indicates where the cursor for this file is currently positioned.

        :return: Cursor position.
        """
        return self._file.tell()

    def seek(self, offset: int=0, from_what: int=0):
        """
        Sets the cursor position relative to some position.

        :param offset: Offset into file relative to from_what parameter.
        :type  offset: int
        :param from_what: Determines what the above offset is relative to.
        :type  from_what: int
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

    def read(self, amount: int=None) -> int:
        """
        Reads bytes from file.  If amount is not specified, the function will
        read until the end of the file.

        :param amount: Amount of bytes to read.  If this is None or an amount
                       isn't specified, read will read all bytes after the
                       cursor.
        :return: Amount of bytes read.
        """
        return self._file.read(size)

    def write(self, data: bytes) -> int:
        """
        Writes bytes to file.

        :param data: Bytes to write.
        :type  data: bytes
        :return: Amount of bytes written.
        """
        return self._file.write(data)

    def insert(self, data: bytes) -> int:
        """
        **NOT IMPLEMENTED**
        Insert bytes into file starting at the current cursor position.

        :param data: Bytes to insert.
        :type  data: bytes
        :return: Amount of bytes inserted.
        """
        assert SpaceFileException("Operation \"insert\" unimplemented...")

    def replace(self, data: bytes) -> int:
        """
        Replaces bytes in file starting at the current cursor position.

        :param data: Bytes to replace.
        :type  data: bytes
        :return: Amount of bytes replaced.
        """
        return self._file.write(data)

    def erase(self, size: int=None) -> int:
        """
        **NOT IMPLEMENTED**
        Deletes bytes from file.

        :param size: Amount of bytes to erase.  If this is None or no amount
                     specified, erase will erase all bytes after the cursor's
                     current position.
        :type size: int
        :return: Amount of bytes erased.
        """
        assert SpaceFileException("Operation \"erase\" unimplemented...")

    def sha256(self) -> bytes:
        """
        Calculates the sha256 hash of the file.

        :return: SHA256 hash (in bytes).
        """
        m = hashlib.sha256()
        m.update(self._file.read())
        return m.digest()

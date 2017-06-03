import hashlib

class SpaceFileException(Exception): pass


class SFile(object):
    """Wrapper over built-in file object that some spade-specific behavior.

    Primarily used to help a spade project track changes and status of a file.
    This object offers all of the functionality found in the original file,
    with a few extra methods modified and added to enable some spade-specific
    functionality.
    """

    mode_read = "rb"
    mode_write = "ab"
    mode_rw = "ab+"

    def __init__(self, project, _file, path: str):
        self.path = path
        self.project = project
        self._closed = False
        self._file = _file
        project._register_file(path, self.sha256())

    def __enter__(self):
        return self

    def __exit__(self, _type, value, tb):
        self.close()

    def __repr__(self):
        return "<sfile \"%s\">" % self.path

    def __str__(self):
        return self.__repr__()

    def __getattr__(self, name):
        """This method is a bit of a hack, so here's an explaination:

        tl;dr this method transparently tries to get attributes that are not
        defined in SFile from the built-in file object.

        The goal of this class is to provide a transparent wrapper over the
        built-in file object that allows us to hook and modify the behavior of
        various methods.  However, since we only modify a few of the methods, we
        can either choose to manually implement all of the other methods that we
        don't really care about or we can leave some unimplemented.  Leaving
        some methods unimplemented ruins the goal of this class being a
        transparent replacement, but implementing all of them means we add a
        bunch of repetitive crap to this class and risk missing some more
        niche items.  To get around that, we can override this method to
        effectively query the underlying file object for attributes we don't
        have but it might.
        """
        return getattr(self._file, name)

    def save(self):
        """Saves a file that has been modified.

        This is requied because, even though in the current implementation of
        SFile we write directly to the file on disk, we must inform the project
        that we've updated it.
        """
        self.project._update_file_hash(self.path, self.sha256())

    def seek(self, offset: int=0, from_what: int=0) -> int:
        """Sets the cursor position relative to some position.

        :param offset: Offset into file relative to from_what parameter.
        :param from_what: Determines what the above offset is relative to.
        :return: Cursor position after the seek operation completes.

        The reference point specified by the ``from_what`` parameter should
        take on one of the following values:

            * 0 - Offset from beginning of file.
            * 1 - Offset from current cursor position.
            * 2 - Offset from end of file.

        The ``from_what`` parameter may be omitted, and will default to 0
        (beginning of file).
        """
        return self._file.seek(offset, from_what)

    def close(self, save: bool=True):
        """Closes a file.

        :param save: Determines if we should automatically save this file on
               close.  Set to True by default because I'm almost 100% sure no
               one's going to read the docs and will complain when their
               projects don't reload properly.  Plus, I imagine there are very
               few scenarios when the common user won't want to save their
               changes to the project.
        :type save: bool
        """
        # Save file before we close it
        if save:
            self.save()

        # Close file and indicate that we've done so
        self._file.close()
        self._closed = True

    def insert(self, data: bytes) -> int:
        """**NOT IMPLEMENTED**
        Insert bytes into file starting at the current cursor position.

        :param data: Bytes to insert.
        :type  data: bytes
        :return: Amount of bytes inserted.
        """
        pass #TODO: implement

    def replace(self, data: bytes) -> int:
        """Replaces bytes in file starting at the current cursor position.

        :param data: Bytes to replace.
        :type  data: bytes
        :return: Amount of bytes replaced.
        """
        return self._file.write(data)

    def erase(self, size: int=None) -> int:
        """**NOT IMPLEMENTED**
        Deletes bytes from file.

        :param size: Amount of bytes to erase.  If this is None or no amount
               specified, erase will erase all bytes after the cursor's
               current position.
        :type size: int
        :return: Amount of bytes erased.
        """
        pass #TODO: implement

    def sha256(self) -> bytes:
        """Calculates the sha256 hash of the file.

        :return: SHA256 hash (in bytes).
        """
        return hash_file(self.path)

    @classmethod
    def open(cls, project, path: str, mode: str=mode_rw):
        f = open(path, mode)
        if not f or not project:
            return None

        return cls(project, f, path)


def hash_file(path: str) -> bytes:
    """Utility function that calculates the hash of a file.

    :param path: Path to the file to hash.
    :type  path: str
    """
    with open(path, "rb") as f:
        f.seek(0,0) # seek to beginning of file
        h = hashlib.sha256()
        h.update(f.read())
        return h.digest()

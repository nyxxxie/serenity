import hashlib
import mmap
from threading import Lock

from . import project


def open_file(project, filename: str, mode: str):
    try:
        fd = open(filename, mode)
        return _File(project, fd)
    except OSError as e:
        raise FileException(e.msg)


class FileException(Exception):

    pass


class _File:
    """
    Provides undo and redo tree history for file.  Think of it as of
    a quantum file that keeps all states of file at the same time.
    """

    def __init__(self, project, fd):
        assert project is not None
        assert fd is not None
        assert fd.readable()
        assert fd.seekable()
        # File should not be calling this
        #project._add_file(self)
        self._project = project
        self._fd = fd
        # Base should be obtained from project's db and only be
        # updated on writes to the file itself.
        self._base = b"\0"*32

    def view(self):
        return FileView(self)

    def base(self):
        return self._base

    def _length(self, base: bytes) -> int:
        pass

    def _read(self, base: bytes, at: int, length: int) -> bytes:
        assert at > 0
        pass

    # NOTE: DO NOT call these methods directly!  They do NOT do extra
    # checks (because of linearly inreasing extreme computational
    # taxes) for out of bounds commits.  Calling these methods
    # directly WILL inevitably hurt changes table inevitably.
    def _insert(self, base: bytes, at: int, data: bytes) -> bytes:
        assert at > 0
        pass

    def _replace(self, base: bytes, at: int, data: bytes) -> bytes:
        assert at > 0
        pass

    def _erase(self, base: bytes, at: int, length: int) -> bytes:
        assert at > 0
        pass


class FileView():
    """
    Provides an ability to view and operate on a file in a specific
    state.  It also provides caching for fast reads since for each
    read call File must apply all changes since file's base to current
    head.
    """

    def __init__(self, f, cache=(16, 0x1000*1024)):
        assert f is not None
        assert len(cache) == 2

        self._f = f
        self._base = self._f.base()
        self._head = self._f.base()
        # Default is 16 pages 4MiB each, that is 64MiB of cache memory
        (self._pagecount, self._pagesize) = cache
        self._pages = []

        cur = self._f.tell()
        self._f.seek(0, SEEK_END)
        self._len = self._f.tell()
        self._f.seek(cur, SEEK_SET)

    def length(self) -> int:
        return self._len

    def read(self, at: int, length: int) -> bytes:
        assert at > 0
        assert length > 1
        if (at + length) >= self._len:
            raise FileException("Read beyond file end")
        # TODO: Should apply changes to what it reads
        # TODO: Should use cache to avoid poor performance on big diff
        self._f.seek(at, SEEK_SET)
        return self._f.read(length)

    def insert(self, at: int, data: bytes):
        assert at > 0
        self._len += len(data)
        pass

    def replace(self, at: int, data: bytes):
        assert at > 0
        if (at + len(data)) >= self._len:
            raise FileException("Replace beyond file end")
        pass

    def erase(self, at: int, length: int):
        assert at > 0
        if length == 0:
            return
        self._len -= length
        pass

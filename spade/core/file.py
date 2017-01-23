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
        pass

    def _insert(self, base: bytes, at: int, data: bytes) -> bytes:
        pass

    def _erase(self, base: bytes, at: int, length: int) -> bytes:
        pass


class FileView():
    """
    Provides an ability to view and operate on a file in a specific
    state.  It also provides caching for fast reads since for each
    read call File must apply all changes since file's base to current
    head.
    """

    def __init__(self, f, cache=(16, 0x1000*1024)):
        self._f = f
        self._base = self._f.base()
        self._head = self._f.base()
        # Default is 16 pages 4MiB each, that is 64MiB of cache memory
        (self._pagecount, self._pagesize) = cache
        self._pages = []

    def length(self) -> int:
        cur = self._f.tell()
        self._f.seek(0, SEEK_END)
        len = self._f.tell()
        self._f.seek(cur, SEEK_SET)
        return len

    def read(self, at: int, length: int) -> bytes:
        # TODO: Should apply changes to what it reads
        # TODO: Should use cache to avoid poor performance on big diff
        self._f.seek(at, SEEK_SET)
        return self._f.read(length)

    def insert(self, at: int, data: bytes):
        pass

    def replace(self, at: int, data: bytes):
        pass

    def erase(self, at: int, length: int):
        pass

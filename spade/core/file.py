import hashlib
import mmap
from threading import Lock

from . import project


class FileException(Exception):

    pass


class _File:
    """
    Provides undo and redo tree history for file.  Think of it as of
    a quantum file that keeps all states of file at the same time. It
    is slow to read from and unsafe to write to, so you need to
    create a _FileView using _File.view() first.
    """

    def __init__(self, project, id):
        self._id = id
        self._project = project
        self._e = self._project.db_engine()
        (path, self._base) = self._querypb()
        try:
            self._fd = open(path, "rb")
        except OSError as e:
            raise FileException(e.msg)

    def view(self):
        """
        Returns newly created instance of _FileView.
        """
        return _FileView(self)

    def base(self) -> bytes:
        """
        Returns base change for this file.
        """
        return self._base

    def _querypb(self) -> (str, bytes):
        """
        Returns (path, base_change) tuple of this file.
        """
        # c = self._db.cursor()
        # c.execute("SELECT path, head_change FROM files WHERE id = ?;",
        #           (self._id,))
        # info = c.fetchone()
        # assert info is not None, "Bad id"
        # return tuple(info)

    def _changes(self, base: bytes, head: bytes) -> list:
        """
        Returns list of changes from base to head.
        """
        # c = self._db.cursor()
        # c.execute("SELECT hash, parent FROM changes WHERE id = ?;",
        #           (self._id,))
        # changes = c.fetchall()
        # return []

    def _change(self, base: bytes, at: int, change_type, data: bytes) -> bytes:
        """
        Commits a change to this file and returns its hash.
        """
        assert change_type in ('+', '-', '!')
        hasher = hashlib.sha256()
        hasher.update(base)
        hasher.update(at.to_bytes(8, byteorder="big"))
        hasher.update(ord(change_type))
        hasher.update(data)
        current = hasher.digest()
        # ins = self._e.insert()
        # conn = self._e.connect()
        # conn.execute(ins,

        # c = self._db.cursor()
        # c.execute("""
        # INSERT INTO changes (id, hash, parent, file_pos, change_type, change)
        # VALUES (?, ?, ?, ?, ?, ?);
        # """, (self._id, current, base, at, change_type, data))
        # self._db.commit()
        # return h


class _FileView():
    """
    Provides an ability to view and operate on a file in a specific
    state.  It also provides caching for fast reads since for each
    read call File must apply all changes since file's base to current
    head.
    """

    def __init__(self, f, cache=(4096, 0x1000)):
        assert len(cache) == 2

        self._f = f
        self._db = self._f._project.db
        self._base = self._f.base()
        self._head = self._f.base()

        cur = self._f._fd.tell()
        self._f._fd.seek(0, 2)
        self._len = self._f._fd.tell()
        self._f._fd.seek(cur, 0)

    def length(self) -> int:
        return self._len

    def read(self, at: int, length: int) -> bytes:
        assert at >= 0
        assert length >= 0
        if (at + length) >= self._len:
            raise FileException("Read beyond file end")
        self._f._fd.seek(at, 0)
        return self._f._fd.read()

    def insert(self, at: int, data: bytes):
        assert at >= 0
        self._head = self._f._change(self._head, at, '+', data)
        self._len += len(data)

    def replace(self, at: int, data: bytes):
        assert at >= 0
        if (at + len(data)) >= self._len:
            raise FileException("Replace beyond file end")
        cur = self.read(at, len(data))
        diff = bytes([a ^ b for (a, b) in zip(cur, data)])
        self._head = self._f._change(self._head, at, '!', diff)

    def erase(self, at: int, length: int):
        assert at >= 0
        assert length >= 0
        if (at + length) >= self._len:
            raise FileException("Erase beyond file end")
        cur = self.read(at, length)
        self._head = self._f._change(self._head, at, '-', cur)
        self._len -= length

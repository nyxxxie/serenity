import hashlib
from threading import Lock

from sqlalchemy import and_
from sqlalchemy.sql import select

from . import project

# On miss update cache
CACHE_UPDATE=0
# On miss load page from file but do not update cache
CACHE_NOUPDATE=1

# End node could be in the way of start node
HINT_UP=-1
# Assume nodes are siblings
HINT_NONE=0
# Start node could be in the way of end node
HINT_DOWN=1


class _File:
    """
    Provides undo and redo tree history for file.
     """

    def __init__(self, project, id, fd, base, head, primary, cache):
        self._project = project
        self._id = id
        self._fd = fd
        self._base = base
        self._head = head
        self._primary = primary
        self._cache = cache
        self._xioread = Lock()
        (self._xpgread, self._xpgwrite) = (Lock(), Lock())
        self._pages = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def tell() -> bytes:
        pass

    def seek(self, hash: bytes):
        pass

    def length(self) -> int:
        self._fd.seek(0, 2)
        return self._fd.tell()

    def read(self, at: int, length: int, policy=CACHE_UPDATE) -> bytes:
        self._fd.seek(at)
        return self._fd.read(length)

    def insert(self, at: int, data: bytes):
        self._fd.seek(at)
        buf = self._fd.read()
        self._fd.seek(at)
        self._fd.write(data + buf)
        self._fd.flush()

    def replace(self, at: int, data: bytes):
        self._fd.seek(at)
        self._fd.write(data)
        self._fd.flush()

    def erase(self, at: int, length: int):
        self._fd.seek(at + length)
        buf = self._fd.read()
        self._fd.seek(at)
        self._fd.write(buf)
        self._fd.truncate()
        self._fd.flush()

    def close(self):
        self._fd.close()

    def _read(self, hash: bytes, at: int, length: int) -> bytes:
        with self._xioread:
            self._fd.seek(at)
            return self._fd.read(length)

    def _changes(self, start: bytes, end: bytes) -> list:
        """
        Returns list of changes needed to be applied from start to end.
        """
        (path_start, path_end) = ([], [])
        # with self._project.db_engine().connect() as conn:
        #     table_changes = self._project.table_changes
        #     sel = select([table_changes]) \
        #           .where(and_(table_changes.c.file_id == self._id,
        #                       table_changes.c.hash == start))
        #     conn.execute(sel)

    def _change(self, parent: bytes, at: int, change_type, data: bytes) -> bytes:
        """
        Commits a change to this file and returns its hash.
        """
        assert change_type in ('+', '-', '!')
        hasher = hashlib.sha256()
        if parent is not None:
            hasher.update(parent)
        hasher.update(at.to_bytes(8, byteorder="big"))
        hasher.update(change_type.encode("latin1"))
        hasher.update(data)
        current = hasher.digest()
        with self._project.db_engine().connect() as conn:
            ins = self._project.table_changes.insert()
            conn.execute(ins,
                         file_id=self._id, hash=current, parent=parent,
                         file_pos=at, change_type=ord(change_type), change=data)
        return current


class __FileView():
    """
    Provides an ability to view and operate on a file in a specific
    state.  It also provides caching for fast reads since for each
    read call File must apply all changes since file's base to current
    head.
    """

    def __init__(self, file, primary, cache=(4096, 0x1000)):
        self._file = file
        self._base = self._file.base()
        self._head = self._file.base()
        self._primary = primary

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

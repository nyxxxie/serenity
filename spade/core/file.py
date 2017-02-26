import hashlib
from itertools import takewhile
from threading import Lock

from sqlalchemy import and_
from sqlalchemy.sql import select

from . import project

RDONLY = "rb"
RDWR = "r+b"

# On miss update cache
CACHE_UPDATE = 0
# On miss load page from file but do not update cache
CACHE_NOUPDATE = 1

# End node could be in the way of start node
HINT_UP = -1
# Nodes are siblings
HINT_NONE = 0
# Start node could be in the way of end node
HINT_DOWN = 1


class _File:
    """
    Provides undo and redo tree history for file.
    """

    def __init__(self, project, id, fd, base, head, mode, primary, cache):
        self._project = project
        self._id = id
        self._fd = fd
        self._mode = mode
        self._primary = primary
        self._cache = cache
        self._xio = Lock()
        (self._xpgread, self._xpgwrite) = (Lock(), Lock())
        self._pages = []
        (self._base, self._head) = (base, base)
        self._sz = 0
        self.seek(head)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def base(self) -> bytes:
        return self._base

    def tell(self) -> bytes:
        return self._head

    def seek(self, hash: bytes):
        self._head = hash
        self._sz = self._size(self._head)

    def size(self) -> int:
        return self._sz

    def read(self, at: int, size: int) -> bytes:
        return self._read(self._head, at, size)

    def insert(self, at: int, data: bytes) -> bytes:
        self._sz += len(data)
        self._head = self._change(self._head, at, '+', data)
        return self._head

    def replace(self, at: int, data: bytes) -> bytes:
        delta = bytes(a ^ b for (a, b) in zip(self.read(at, len(data)), data))
        self._head = self._change(self._head, at, '!', delta)
        return self._head

    def erase(self, at: int, size: int) -> bytes:
        self._sz -= length
        self._head = self._change(self._head, at, '-', self.read(at, size))
        return self._head

    def close(self):
        self._fd.close()

    def _size(self, hash: bytes) -> int:
        self._fd.seek(0, 2)
        return self._fd.tell()

    def _read(self, hash: bytes, at: int, size: int) -> bytes:
        self._fd.seek(at)
        return self._fd.read(size)

    def _path(self, root: bytes, hash: bytes) -> list:
        if root == hash:
            return []
        with self._project.db_engine().connect() as conn:
            table_changes = self._project.table_changes
            path = []
            while True:
                if hash == root:
                    return path
                if hash is None:
                    raise Exception("Nigger")
                sel = select([table_changes]) \
                      .where(and_(table_changes.c.file_id == self._id,
                                  table_changes.c.hash == hash))
                result = conn.execute(sel)
                (_, _, parent, file_pos, type, change) = result.first()
                path.insert(0, (type, file_pos, change))
                hash = parent

    def _inv(self, changes: list) -> list:
        swap = {'+': '-', '-': '+', '!': '!'}
        return [(swap[type], file_pos, change)
                for (type, file_pos, change)
                in changes]

    def _changes(self, start: bytes, end: bytes) -> list:
        """
        Returns sequence of changes needed to turn data at start into data at
        end.
        """
        path_start = self._path(self.base(), start)
        path_end = self._path(self.base(), end)
        # counts how many common changes both paths have at their beginning
        norm = sum(1 for _ in
                   takewhile(lambda x: x[0] == x[1], zip(path_start, path_end)))
        return self._inv(path_start[norm:]) + path_end[norm:]

    def _change(self, parent: bytes, at: int, change_type, data: bytes) -> bytes:
        """
        Commits a change to this file and returns its hash.
        """
        assert change_type in ('+', '-', '!')
        hasher = hashlib.sha256()
        hasher.update(self._id.to_bytes(4, byteorder="big"))
        if parent is not None:
            hasher.update(parent)
        hasher.update(at.to_bytes(8, byteorder="big"))
        hasher.update(change_type.encode())
        hasher.update(data)
        current = hasher.digest()
        with self._project.db_engine().connect() as conn:
            ins = self._project.table_changes.insert()
            conn.execute(ins,
                         file_id=self._id, hash=current, parent=parent,
                         file_pos=at, change_type=change_type, change=data)
        return current

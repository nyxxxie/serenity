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


class FileAccessException(Exception):

    pass


class _FileCache:

    def __init__(self, max_pages, page_size):
        self.setparams(max_pages, page_size)

    def setparams(max_pages, page_size):
        self._max_pages = max_pages
        self._page_size = page_size

    def getparams():
        return (self._max_pages, self._page_size)


class _File:
    """
    Provides undo and redo tree history for file.
    """

    def __init__(self, project, id, fd, base, head, mode, primary, cacheparams):
        self._project = project
        self._id = id
        self._fd = fd
        self._mode = mode
        self._primary = primary
        self._xio = Lock()
        # pages should be readers-writer locked
        (self._xpg, self._xpgwrite) = (Lock(), Lock())
        (self._base, self._head) = (base, base)
        self._sz = self._size()
        self._pages = [self._read(0, self._sz)]
        self.seek(head)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def base(self) -> bytes:
        return self._base

    def tell(self) -> bytes:
        return self._head

    def write_inplace(self) -> bytes:
        if self._mode != RDWR:
            raise FileAccessException("Opened in a read-only mode")
        for (type, file_pos, change) in self._changes(self._base, self._head):
            if type == '!':
                self._fd.seek(file_pos)
                self._fd.write(change)
            elif type == '+':
                self._fd.seek(file_pos)
                self._fd.write(change + self._fd.read())
            elif type == '-':
                self._fd.seek(file_pos + len(change))
                rest = self._fd.read()
                self._fd.seek(file_pos)
                self._fd.write(rest)
                self._fd.truncate()
            self._fd.flush()

    def seek(self, hash: bytes) -> bytes:
        with self._xpg:
            for (type, file_pos, change) in self._changes(self._head, hash):
                if type == '!':
                    self._pages[0] = (self._pages[0][:file_pos]
                                      + change
                                      + self._pages[0][file_pos+len(change)-1:])
                elif type == '+':
                    self._pages[0] = (self._pages[0][:file_pos]
                                      + change
                                      + self._pages[0][file_pos:])
                    self._sz += len(change)
                elif type == '-':
                    self._pages[0] = (self._pages[0][:file_pos]
                                      + self._pages[0][file_pos+len(change):])
                    self._sz -= len(change)
            assert self._sz == len(self._pages[0])
            self._head = hash
            return self._head

    def size(self) -> int:
        return self._sz

    def read(self, at: int, size: int) -> bytes:
        return self._pages[0][at:at+size]

    def insert(self, at: int, data: bytes) -> bytes:
        self._sz += len(data)
        self._head = self._change(self._head, at, '+', data)
        return self._head

    def replace(self, at: int, data: bytes) -> bytes:
        delta = bytes(a ^ b for (a, b) in zip(self.read(at, len(data)), data))
        self._head = self._change(self._head, at, '!', delta)
        return self._head

    def erase(self, at: int, size: int) -> bytes:
        self._sz -= size
        self._head = self._change(self._head, at, '-', self.read(at, size))
        return self._head

    def close(self):
        self._fd.close()

    def _size(self) -> int:
        with self._xio:
            self._fd.seek(0, 2)
            return self._fd.tell()

    def _read(self, at: int, size: int) -> bytes:
        with self._xio:
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
        # FIXME: For now it only works if both start and end are below the base
        # in time.
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

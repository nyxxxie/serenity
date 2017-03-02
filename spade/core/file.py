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


class FileChangeException(Exception):

    pass


class FileBoundsException(Exception):

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
        """
        Return change the on-disk file is at.
        """
        return self._base

    def write_inplace(self, hash: bytes):
        """
        Write hash changes to the current file.  File must be open in RDWR mode
        and hash must be valid.  Throws FileAccessException if file is not in
        RDWR mode and SomethingElseException if hash change does not exist.
        Returns number of bytes written.  WARNING: this operation is not atomic
        at all and will corrupt the file if interrupted during write.
        """
        # FIXME: Must operate on small blocks
        block_size = 0x10000
        if self._mode != RDWR:
            raise FileAccessException("Opened in a read-only mode")
        with self._xio:
            for (type, file_pos, change) in self._changes(self._base, hash):
                print(type)
                if type == '!':
                    self._fd.seek(file_pos)
                    self._fd.write(change)
                    self._fd.flush()
                elif type == '+':
                    # FIXME: This will eat memory
                    self._fd.seek(file_pos)
                    rest = self._fd.read()
                    self._fd.seek(file_pos)
                    self._fd.write(change)
                    self._fd.write(rest)
                    self._fd.flush()
                elif type == '-':
                    change_len = len(change)
                    for i in range(file_pos, self._size() - change_len,
                                   block_size):
                        self._fd.seek(i + change_len)
                        tmp = self._fd.read(block_size)
                        print(i, len(tmp))
                        self._fd.seek(i)
                        self._fd.write(tmp)
                        self._fd.flush()
                    self._fd.truncate()
                else:
                    assert False
            self._fd.seek(0)
            hasher = hashlib.sha256()
            for chunk in iter(lambda: self._fd.read(0x1000), b""):
                hasher.update(chunk)
            table_files = self._project.table_files
            upd = table_files.update() \
                             .values(hash=hasher.digest(), base=hash) \
                             .where(table_files.c.id == self._id)
            with self._project.db_engine().connect() as conn:
                conn.execute(upd)

    def write_to(self, fd, hash: bytes):
        pass

    def seek(self, to: bytes) -> bytes:
        """
        Changes head to to and updates cache.  hash must be valid, otherwise
        SomethingElseException is thrown.  Returns new head.
        """
        # FIXME: Fails if to is younger than base
        for (type, file_pos, change) in self._changes(self._base, to):
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
        self._head = to
        return self._head

    def size(self) -> int:
        """
        Returns size of file at current head.
        """
        return self._sz

    def read(self, at: int, size: int) -> bytes:
        # FIXME: Make it use cache properly
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
        """
        On-disk file length.
        """
        self._fd.seek(0, 2)
        return self._fd.tell()

    def _read(self, at: int, size: int) -> bytes:
        """
        Reads from on-disk file.
        """
        self._fd.seek(at)
        return self._fd.read(size)

    def _path(self, root: bytes, hash: bytes) -> list:
        """
        Finds path of hash change from root.
        """
        # FIXME: Good exception types
        if root == hash:
            return []
        path = []
        while True:
            if hash == root:
                return path
            if hash is None:
                raise Exception("Reached root of the tree")
            table_changes = self._project.table_changes
            sel = select([table_changes]) \
                  .where(and_(table_changes.c.file_id == self._id,
                              table_changes.c.hash == hash))
            with self._project.db_engine().connect() as conn:
                result = conn.execute(sel).first()
                if result is not None:
                    (_, _, parent, file_pos, type, change) = result
                    path.insert(0, (type, file_pos, change))
                    hash = parent
                else:
                    raise FileChangeException("No change")

    def _changes(self, start: bytes, end: bytes) -> list:
        """
        Returns sequence of changes needed to turn data at start into data at
        end.
        """
        # FIXME: For now it only works if both start and end are below the base
        # in time.
        path_start = self._path(self._base, start)
        path_end = self._path(self._base, end)
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
        ins = self._project.table_changes.insert()
        with self._project.db_engine().connect() as conn:
            conn.execute(ins,
                         file_id=self._id, hash=current, parent=parent,
                         file_pos=at, change_type=change_type, change=data)
        return current

    def _inv(self, changes: list) -> list:
        """
        Returns list of inverted changes.
        """
        swap = {'+': '-', '-': '+', '!': '!'}
        return [(swap[type], file_pos, change)
                for (type, file_pos, change) in changes]

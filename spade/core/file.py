class SpadeFileException(Exception): pass

class sfile:
    """
    Provides an interface to files that is similar to the built-in file type.
    This is required so that the main project class can catch changes to files
    it is tracking.  This also allows for implementing features like change
    history and undo/redo later on.  This class should never be used directly.
    """

    def __init__(self, project, path: str):
        pass

    def close(self):
        pass

    #def __enter__(self):
    #    pass

    #def __exit__(self, _, _, _):
    #    pass

    def seek(self, to: bytes) -> bytes:
        pass

    def size(self) -> int:
        pass

    def read(self, at: int, size: int) -> bytes:
        pass

    def write(self, fd, change: bytes):
        pass

    def insert(self, at: int, data: bytes) -> bytes:
        pass

    def replace(self, at: int, data: bytes) -> bytes:
        pass

    def erase(self, at: int, size: int) -> bytes:
        pass

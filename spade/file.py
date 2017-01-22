class File:
    """
    Represents an open file descriptor, provides mmap and cursor layers and undo
    history (aka commit history).
    """

    def __init__(self, filename: str, flags):
        pass

    def map(self, address, size):
        pass

    def unmap(self, mapped_map):
        pass

    def read(self, at):
        pass

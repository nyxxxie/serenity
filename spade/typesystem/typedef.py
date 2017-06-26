class SpadeTypeException(Exception): pass

class TypeDef(object):
    """Parent class for type implementations."""
    size = 0

    def __init__(self, data=None, size=0):
        self._string = None
        self._bytes = None
        self.convert(data)

    def convert(self, data):
        self._string = self.to_string(data)
        self._bytes = self.to_bytes(data)

    def __str__(self):
        return self.string()

    def string(self) -> str:
        return self._string

    def bytes(self) -> bytes:
        return self._bytes

    #def size(self) -> int:
    #    return self._size

    def to_string(self, data) -> str:
        """TODO: Implement this method for your custom type."""
        pass

    def to_bytes(self, data) -> bytes:
        """TODO: Implement this method for your custom type."""
        pass

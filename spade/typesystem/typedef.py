class SpadeTypeException(Exception): pass

class TypeDef:
    def __init__(self, data=None, size=0):
        self._string = None
        self._bytes = None
        self._size = size
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

    def size(self) -> int:
        return self._size

    def to_string(data) -> str:
        """
        TODO: Implement this method for your custom type.
        """
        return None

    def to_bytes(data) -> bytes:
        """
        TODO: Implement this method for your custom type.
        """
        return None

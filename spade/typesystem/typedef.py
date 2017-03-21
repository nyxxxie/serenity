class TypeDef:
    def __init__(self, names: list):
        self.names = names
        self.size = 0 # This MUST be defined in type

    def to_string(self, byte_array: bytes) -> str:
        """ Converts an input array of bytes into a string representation of
            the type.  Implement this if your type should provide this
            functionality.
        """
        return None

    def from_string(self, string: str) -> bytes:
        """ Converts an input string into and array of bytes that translate
            into the binary representation of the type.  Implement this if your
            type should provide this functionality.
        """
        return None


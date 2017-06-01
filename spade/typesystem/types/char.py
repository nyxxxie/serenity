from spade.typesystem import typemanager
from spade.typesystem.typedef import TypeDef, SpadeTypeException

class Char(TypeDef):
    __typenames__ = ["char", "c"]

    def __init__(self, data=None):
        super().__init__(data, 1)

    def to_string(self, data) -> str:
        if not data:
            return None

        if isinstance(data, bytes):
            return data.decode("ascii").upper()
        elif isinstance(data, str):
            return data.upper()
        else:
            raise SpadeTypeException("Data type {} can't be converted.".format(str(type(data))))

    def to_bytes(self, data) -> bytes:
        if not data:
            return None

        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return data.upper().encode("ascii")
        else:
            raise SpadeTypeException("Data type {} can't be converted.".format(str(type(data))))

    def unprintable(self):
        return not self.printable()

    def printable(self):
        if self.size() == 0 or not self.bytes():
            return False

        for char in self.bytes():
            if (0x00 <= char and char <= 0x1F) or char == 0x7F:
                return False

        return True

typemanager.add_type(Char)

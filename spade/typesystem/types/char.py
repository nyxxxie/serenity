import struct
from spade.typesystem import typemanager
from spade.typesystem.typedef import TypeDef, InvalidTypeException, NullDataException

class Char(TypeDef):
    __typenames__ = ["char", "c"]

    def to_string(self, data) -> str:
        if data is None or len(data) == 0:
            return None

        self._size = 1

        if isinstance(data, bytes):
            return data.decode("ascii").upper()
        elif isinstance(data, str):
            return data.upper()
        else:
            raise InvalidTypeException("Data type {} can't be converted.".format(str(type(data))))

    def to_bytes(self, data) -> bytes:
        if data is None or len(data) == 0:
            return None

        self._size = 1

        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return data.upper().encode("ascii")
        else:
            raise InvalidTypeException("Data type {} can't be converted.".format(str(type(data))))

    @staticmethod # TODO: make this static, apply towards single character
    def unprintable(self):
        return False 

    def printable(self):
        return not unprintable()

typemanager.add_type(Char)

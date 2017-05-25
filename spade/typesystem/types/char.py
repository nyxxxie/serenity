from spade.typesystem import typemanager
from spade.typesystem.typedef import TypeDef, InvalidTypeException, NullDataException

class Char(TypeDef):
    __typenames__ = ["char", "c"]

    def to_string(self, data) -> str:
        if data is None or len(data) == 0:
            return None

        self._size = 4

        if isinstance(data, bytes):
            return None
        elif isinstance(data, str):
            return None
        else:
            raise InvalidTypeException("Data type {} can't be converted.".format(str(type(data))))

    def to_bytes(self, data) -> bytes:
        if data is None or len(data) == 0:
            return None

        self._size = 4

        if isinstance(data, bytes):
            return None
        elif isinstance(data, str):
            return None
        else:
            raise InvalidTypeException("Data type {} can't be converted.".format(str(type(data))))

typemanager.add_type(Char)

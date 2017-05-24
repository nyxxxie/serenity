from spade.typesystem import typemanager
from spade.typesystem.typedef import TypeDef, InvalidTypeException, NullDataException

class Int32(TypeDef):
    __typenames__ = ["int32", "int", "i32", "i32le"]

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
            return bytes.fromhex(data);
        else:
            raise InvalidTypeException("Data type {} can't be converted.".format(str(type(data))))

typemanager.add_type(Int32)

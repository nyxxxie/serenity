from spade.typesystem import typemanager
from spade.typesystem.typedef import TypeDef, InvalidTypeException, NullDataException
import struct

class Byte(TypeDef):
    def to_string(self, data) -> str:
        if data is None or len(data) == 0:
            return None

        self._size = 1

        if isinstance(data, bytes):
            ret = ""
            for byte in data:
                ret += "%02x" % (byte)
            return ret.upper()
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
            return bytes.fromhex(data);
        else:
            raise InvalidTypeException("Data type {} can't be converted.".format(str(type(data))))

typemanager.add_type(Byte, ["byte"])

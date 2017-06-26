from spade.typesystem import typemanager
from spade.typesystem.typedef import TypeDef, SpadeTypeException

class Byte(TypeDef):
    __typenames__ = ["byte", "b"]

    size = 1

    def __init__(self, data=None):
        super().__init__(data, 1)

    def to_string(self, data) -> str:
        if not data:
            return None

        if isinstance(data, bytes):
            ret = ""
            for byte in data:
                ret += "%02x" % (byte)
            return ret.upper()
        elif isinstance(data, str):
            return data.upper()
        else:
            raise SpadeTypeException("Can't convert {}.".format(type(data)))

    def to_bytes(self, data) -> bytes:
        if not data:
            return None

        if isinstance(data, bytes):
            return data
        elif isinstance(data, str):
            return bytes.fromhex(data)
        else:
            raise SpadeTypeException("Can't convert {}.".format(type(data)))

typemanager.add_type(Byte)

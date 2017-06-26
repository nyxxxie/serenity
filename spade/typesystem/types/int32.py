import struct
from spade.typesystem import typemanager
from spade.typesystem.typedef import TypeDef, SpadeTypeException

class Int32(TypeDef):
    __typenames__ = ["int32", "int", "i32", "i32le"]

    size = 4

    def __init__(self, data=None):
        super().__init__(data)

    def to_string(self, data) -> str:
        if not data:
            return None

        if isinstance(data, bytes):
            if len(data) != self.size:
                return None
            try:
                data_bytes = struct.unpack('>i', data)
                if data_bytes:
                    return str(data_bytes[0])
            except struct.error:
                #raise SpadeTypeException("Data input size {} != 4 bytes.".format(len(data)))
                return None
            raise SpadeTypeException("output of struct.unpack was None.")
        elif isinstance(data, str):
            return data
        else:
            raise SpadeTypeException("Can't convert {}.".format(type(data)))

    def to_bytes(self, data) -> bytes:
        if not data:
            return None

        if isinstance(data, bytes):
            if len(data) == 4:
                return data
        elif isinstance(data, str):
            return struct.pack(">i", int(data))
        else:
            raise SpadeTypeException("Can't convert {}.".format(type(data)))

        return None

typemanager.add_type(Int32)

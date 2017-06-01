import struct
from spade.typesystem import typemanager
from spade.typesystem.typedef import TypeDef, InvalidTypeException, NullDataException

class Int32(TypeDef):
    __typenames__ = ["int32", "int", "i32", "i32le"]

    def __init__(self, data=None):
        super().__init__(data, 4)

    def to_string(self, data) -> str:
        if not data:
            return None

        if isinstance(data, bytes):
            if len(data) != 4:
                return None
            try:
                b = struct.unpack('>i', data)
                if b:
                    return str(b[0])
            except struct.error:
                #raise InvalidTypeException("Data input size {} != 4 bytes.".format(len(data)))
                return None
            raise InvalidTypeException("output of struct.unpack was None.")
        elif isinstance(data, str):
            return data
        else:
            raise InvalidTypeException("Data type {} can't be converted.".format(str(type(data))))

    def to_bytes(self, data) -> bytes:
        if not data:
            return None

        if isinstance(data, bytes):
            if len(data) == 4:
                return data
            else:
                return None
        elif isinstance(data, str):
            return struct.pack(">i", int(data))
        else:
            raise InvalidTypeException("Data type {} can't be converted.".format(str(type(data))))

typemanager.add_type(Int32)

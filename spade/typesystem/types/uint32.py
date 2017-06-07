import struct
from spade.typesystem import typemanager
from spade.typesystem.typedef import TypeDef, SpadeTypeException

class UInt32(TypeDef):
    __typenames__ = ["uint32", "uint", "ui32", "ui32le"]

    def __init__(self, data=None):
        super().__init__(data, 4)

    def to_string(self, data) -> str:
        if not data:
            return None

        if isinstance(data, bytes):
            if len(data) != 4:
                return None
            try:
                data_bytes = struct.unpack('>I', data)
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
            return struct.pack(">I", int(data))
        else:
            raise SpadeTypeException("Can't convert {}.".format(type(data)))

        return None

typemanager.add_type(UInt32)

from spade.typesystem.typedef import TypeDef
from spade.typesystem.types import default_types
import struct

class Byte(TypeDef):
    def __init__(self):
        super().__init__(["byte"])
        self.size = 1

    def to_string(self, byte_array: bytes) -> str:
        if byte_array is None or len(byte_array) != 1:
            return None

        ret = ""
        for byte in byte_array:
            ret += "%02x" % (byte)

        return ret

    def from_string(self, string: str) -> bytes:
        if string is None or len(string) != 2: # TODO: support 0x and h prefixes
            return None

        return bytes.fromhex(string);

default_types.append(Byte())

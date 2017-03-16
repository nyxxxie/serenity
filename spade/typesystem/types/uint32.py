from spade.typesystem.typedef import TypeDef
from spade.typesystem.types import default_types

class UInt32(TypeDef):
    def __init__(self):
        self.size = 4

    def to_string(self, byte_array):
        return ""

    def from_string(self, byte_array):
        return ""

default_types.append(UInt32)

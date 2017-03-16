from spade.typesystem.typedef import TypeDef
from spade.typesystem.types import default_types

class Byte(TypeDef):
    def __init__(self):
        self.size = 1

    def to_string(self, byte_array):
        return ""

    def from_string(self, byte_array):
        return ""

default_types.append(Byte)

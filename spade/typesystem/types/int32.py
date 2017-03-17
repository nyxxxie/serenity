from spade.typesystem.typedef import TypeDef
from spade.typesystem.types import default_types

class Int32(TypeDef):
    def __init__(self):
        super().__init__("int32")
        self.size = 4

    def to_string(self, byte_array: bytes) -> str:
        return ""

    def from_string(self, string: str) -> bytes:
        return ""

default_types.append(Int32())

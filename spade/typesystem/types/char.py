from spade.typesystem.typedef import TypeDef
from spade.typesystem.types import default_types

class Char(TypeDef):
    def __init__(self):
        super().__init__("char")
        self.size = 1

    def to_string(self, byte_array: bytes) -> str:
        return ""

    def from_string(self, string: str) -> bytes:
        return ""

default_types.append(Char())

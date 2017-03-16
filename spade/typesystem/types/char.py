from spade.typesystem.typedef import TypeDef
from spade.typesystem.types import default_types

class Char(TypeDef):
    def __init__(self):
        self.size = 1

    def to_string(self, byte):
        return ""

    def from_string(self, byte):
        return ""

default_types.append(Char)

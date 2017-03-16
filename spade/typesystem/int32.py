from .typedef import TypeDef
from .manager import default_types

class Int32(TypeDef):
    def __init__(self):
        self.size = 4

    def to_string(self, byte_array):
        return ""

    def from_string(self, byte_array):
        return ""

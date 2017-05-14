#from spade.typesystem.typedef import TypeDef
#from spade.typesystem.types import default_types
#
#class Int32(TypeDef):
#    def __init__(self):
#        super().__init__(["i32", "i32le", "int32"])
#        self.size = 4
#
#    def to_string(self, byte_array: bytes) -> str:
#        if byte_array is None or len(byte_array) != self.size:
#            return None
#
#        # NOTE: this converter doesn't work, needs to be fixed
#        number = 0
#        string = ""
#
#        negative = (byte_array[0] >> 7) == 1
#        if negative:
#            # The below steps negate our negative number to make it positive.
#            # Negation of a 2's complement little endian interger is done by
#            # notting it and then adding it by one.  That is what the below
#            # two lines accomplish.
#            byte_array = bytes([(~x) & 0xFF for x in byte_array])
#            number = 1
#
#            string = "-"
#
#        bit_offset = 0
#        for b in byte_array:
#            for bit in range(0,8):
#                mask = 1 << bit
#                if b & mask:
#                    number += 1 << (bit_offset + bit)
#            bit_offset += 8
#
#        string = string + str(number)
#
#        return string
#
#    def from_string(self, string: str) -> bytes:
#        if string is None or len(string) == 0:
#            return None
#
#        return ""
#
#default_types.append(Int32())

from spade.typesystem import typemanager
from spade.typesystem.types.byte import Byte

# ---------------------------
# INIT AND ODD CASES
# ---------------------------
def test_init():
    byte = Byte()
    assert byte.size() == 0
    assert byte.string() is None
    assert byte.bytes() is None
    assert byte.unprintable()

def test_none():
    byte = Byte(None)
    assert byte.size() == 0
    assert byte.string() is None
    assert byte.bytes() is None
    assert byte.unprintable()

def test_empty_bytes():
    byte = Byte(bytes([]))
    assert byte.size() == 0
    assert byte.string() is None
    assert byte.bytes() is None
    assert byte.unprintable()

def test_empty_string():
    byte = Byte("")
    assert byte.size() == 0
    assert byte.string() is None
    assert byte.bytes() is None
    assert byte.unprintable()


# ---------------------------
# CONVERT A
# ---------------------------
def test_convert_letter_string_lower():
    byte = Byte("A")
    assert byte.size() == 1
    assert byte.string() == "A"
    assert byte.bytes() == bytes([0x41])
    assert not byte.unprintable()

def test_convert_letter_string_lower():
    byte = Byte("a")
    assert byte.size() == 1
    assert byte.string() == "A"
    assert byte.bytes() == bytes([0x41])
    assert not byte.unprintable()

def test_convert_letter_bytes():
    byte = Byte(bytes([0x41]))
    assert byte.size() == 1
    assert byte.string() == "A"
    assert byte.bytes() == bytes([0x41])
    assert not byte.unprintable()


# ---------------------------
# CONVERT 7
# ---------------------------
def test_convert_number_string():
    byte = Byte("7")
    assert byte.size() == 1
    assert byte.string() == "7"
    assert byte.bytes() == bytes([0x37])
    assert not byte.unprintable()

def test_convert_number_bytes():
    byte = Byte(bytes([0x37]))
    assert byte.size() == 1
    assert byte.string() == "7"
    assert byte.bytes() == bytes([0x37])
    assert not byte.unprintable()


# ---------------------------
# CONVERT UNPRINTABLE
# ---------------------------
def test_convert_number_string():
    byte = Byte("\n")
    assert byte.size() == 1
    assert byte.string() == "\n"
    assert byte.bytes() == bytes([0x01])
    assert byte.unprintable()

def test_convert_number_bytes():
    byte = Byte(bytes([0x01]))
    assert byte.size() == 1
    assert byte.string() == "\n"
    assert byte.bytes() == bytes([0x01])
    assert byte.unprintable()

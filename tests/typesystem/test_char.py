from spade.typesystem import typemanager
from spade.typesystem.types.char import Char

# ---------------------------
# INIT AND ODD CASES
# ---------------------------
def test_init():
    char = Char()
    assert char.size() == 0
    assert char.string() is None
    assert char.bytes() is None
    assert char.unprintable()

def test_none():
    char = Char(None)
    assert char.size() == 0
    assert char.string() is None
    assert char.bytes() is None
    assert char.unprintable()

def test_empty_chars():
    char = Char(bytes([]))
    assert char.size() == 0
    assert char.string() is None
    assert char.bytes() is None
    assert char.unprintable()

def test_empty_string():
    char = Char("")
    assert char.size() == 0
    assert char.string() is None
    assert char.bytes() is None
    assert char.unprintable()


# ---------------------------
# CONVERT A
# ---------------------------
def test_convert_letter_string_lower():
    char = Char("A")
    assert char.size() == 1
    assert char.string() == "A"
    assert char.bytes() == bytes([0x41])
    assert not char.unprintable()

def test_convert_letter_string_lower():
    char = Char("a")
    assert char.size() == 1
    assert char.string() == "A"
    assert char.bytes() == bytes([0x41])
    assert not char.unprintable()

def test_convert_letter_chars():
    char = Char(bytes([0x41]))
    assert char.size() == 1
    assert char.string() == "A"
    assert char.bytes() == bytes([0x41])
    assert not char.unprintable()


# ---------------------------
# CONVERT 7
# ---------------------------
def test_convert_number_string():
    char = Char("7")
    assert char.size() == 1
    assert char.string() == "7"
    assert char.bytes() == bytes([0x37])
    assert not char.unprintable()

def test_convert_number_chars():
    char = Char(bytes([0x37]))
    assert char.size() == 1
    assert char.string() == "7"
    assert char.bytes() == bytes([0x37])
    assert not char.unprintable()


# ---------------------------
# CONVERT UNPRINTABLE
# ---------------------------
def test_convert_number_string():
    char = Char("\n")
    assert char.size() == 1
    assert char.string() == "\n"
    assert char.bytes() == bytes([0x0A])
    assert char.unprintable()

def test_convert_number_chars():
    char = Char(bytes([0x0A]))
    assert char.size() == 1
    assert char.string() == "\n"
    assert char.bytes() == bytes([0x0A])
    assert char.unprintable()

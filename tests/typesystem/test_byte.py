import pytest
from spade.typesystem import typemanager
from spade.typesystem.types.byte import Byte

test_data = [
    ("00", 0x00), # Smallest value
    ("FF", 0xFF), # 
    ("fF", 0xFF),
    ("Ff", 0xFF),
    ("ff", 0xFF),
    ("CD", 0xCD),
    ("43", 0x43),
    ("C8", 0xC8),
    ("c8", 0xC8),
    ("6A", 0x6A),
    ("6a", 0x6A),
]

# ---------------------------
# INIT AND ODD CASES
# ---------------------------
def test_init():
    byte = Byte()
    assert byte.size == 1
    assert byte.string() is None
    assert byte.bytes() is None

def test_none():
    byte = Byte(None)
    assert byte.size == 1
    assert byte.string() is None
    assert byte.bytes() is None

def test_empty_bytes():
    byte = Byte(bytes([]))
    assert byte.size == 1
    assert byte.string() is None
    assert byte.bytes() is None

def test_empty_string():
    byte = Byte("")
    assert byte.size == 1
    assert byte.string() is None
    assert byte.bytes() is None

# ---------------------------
# TO BYTE
# ---------------------------
@pytest.mark.parametrize("string,byte", test_data)
def test_convert_to_byte(string, byte):
    b = Byte(string)
    assert b.size == 1
    assert b.string() == string.upper()
    assert b.bytes() == bytes([byte])

# ---------------------------
# TO STRING
# ---------------------------
@pytest.mark.parametrize("string,byte", test_data)
def test_convert_to_string(string, byte):
    b = Byte(bytes([byte]))
    assert b.size == 1
    assert b.string() == string.upper()
    assert b.bytes() == bytes([byte])

# ---------------------------
# TYPESYSTEM INTEGRATION
# ---------------------------
def test_typemanager_added():
    for name in Byte.__typenames__:
        assert typemanager.get_type(name) is not None

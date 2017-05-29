import pytest
from spade.typesystem import typemanager
from spade.typesystem.types.uint32 import UInt32

# ---------------------------
# INIT AND ODD CASES
# ---------------------------
def test_init():
    uint32 = UInt32()
    assert uint32.size() == 4
    assert uint32.string() is None
    assert uint32.bytes() is None

def test_none():
    uint32 = UInt32()
    assert uint32.size() == 4
    assert uint32.string() is None
    assert uint32.bytes() is None

def test_empty_bytes():
    uint32 = UInt32(bytes([]))
    assert uint32.size() == 4
    assert uint32.string() is None
    assert uint32.bytes() is None

def test_empty_string():
    uint32 = UInt32("")
    assert uint32.size() == 4
    assert uint32.string() is None
    assert uint32.bytes() is None

def test_too_few_bytes():
    uint32 = UInt32(bytes([0x13, 0x37]))
    assert uint32.size() == 4
    assert uint32.string() is None
    assert uint32.bytes() is None

def test_too_many_bytes():
    uint32 = UInt32(bytes([0x00, 0x00, 0x00, 0x01, 0x00]))
    assert uint32.size() == 4
    assert uint32.string() is None
    assert uint32.bytes() is None


# ---------------------------
# CONVERT ZERO
# ---------------------------
def test_convert_zero_string():
    uint32 = UInt32("0")
    assert uint32.size() == 4
    assert uint32.string() == "0"
    assert uint32.bytes() == bytes([0x00, 0x00, 0x00, 0x00])

def test_convert_zero_bytes():
    uint32 = UInt32(bytes([0x00, 0x00, 0x00, 0x00]))
    assert uint32.size() == 4
    assert uint32.string() == "0"
    assert uint32.bytes() == bytes([0x00, 0x00, 0x00, 0x00])


# ---------------------------
# CONVERT MIN
# ---------------------------
def test_convert_min_string():
    uint32 = UInt32("1")
    assert uint32.size() == 4
    assert uint32.string() == "1"
    assert uint32.bytes() == bytes([0x00, 0x00, 0x00, 0x01])

def test_convert_min_bytes():
    uint32 = UInt32(bytes([0x00, 0x00, 0x00, 0x01])) #TODO: get binary value for this
    assert uint32.size() == 4
    assert uint32.string() == "1"
    assert uint32.bytes() == bytes([0x00, 0x00, 0x00, 0x01])


# ---------------------------
# CONVERT MAX
# ---------------------------
def test_convert_max_string():
    uint32 = UInt32("4294967295")
    assert uint32.size() == 4
    assert uint32.string() == "4294967295"
    assert uint32.bytes() == bytes([0xFF, 0xFF, 0xFF, 0xFF])

def test_convert_max_bytes():
    uint32 = UInt32(bytes([0xFF, 0xFF, 0xFF, 0xFF]))
    assert uint32.size() == 4
    assert uint32.string() == "4294967295"
    assert uint32.bytes() == bytes([0xFF, 0xFF, 0xFF, 0xFF])


# ---------------------------
# TYPESYSTEM INTEGRATION
# ---------------------------
def test_typemanager_byte_added_all_names():
    for name in UInt32.__typenames__:
        assert typemanager.get_type(name) is not None

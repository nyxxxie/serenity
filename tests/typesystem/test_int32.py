import pytest
from spade.typesystem import typemanager
from spade.typesystem.types.int32 import Int32

# ---------------------------
# INIT AND ODD CASES
# ---------------------------
def test_init():
    int32 = Int32()
    assert int32.size() == 0
    assert int32.string() is None
    assert int32.bytes() is None

def test_none():
    int32 = Int32()
    assert int32.size() == 0
    assert int32.string() is None
    assert int32.bytes() is None

def test_empty_bytes():
    int32 = Int32(bytes([]))
    assert int32.size() == 0
    assert int32.string() is None
    assert int32.bytes() is None

def test_empty_string():
    int32 = Int32("")
    assert int32.size() == 0
    assert int32.string() is None
    assert int32.bytes() is None

def test_too_few_bytes():
    int32 = Int32(bytes([0x13, 0x37]))
    assert int32.size() == 0
    assert int32.string() is None
    assert int32.bytes() is None

def test_too_many_bytes():
    int32 = Int32(bytes([0x00, 0x00, 0x00, 0x01, 0x00]))
    assert int32.size() == 4
    assert int32.string() == "1"
    assert int32.bytes() == bytes([0x00, 0x00, 0x00, 0x01])


# ---------------------------
# CONVERT ZERO
# ---------------------------
def test_convert_zero_string():
    int32 = Int32("0")
    assert int32.size() == 4
    assert int32.string() == "0"
    assert int32.bytes() == bytes([0x00, 0x00, 0x00, 0x00])

def test_convert_zero_bytes():
    int32 = Int32(bytes([0x00, 0x00, 0x00, 0x00]))
    assert int32.size() == 4
    assert int32.string() == "0"
    assert int32.bytes() == bytes([0x00, 0x00, 0x00, 0x00])


# ---------------------------
# CONVERT MIN
# ---------------------------
def test_convert_min_string():
    int32 = Int32("-2147483648")
    assert int32.size() == 4
    assert int32.string() == "-2147483648"
    assert int32.bytes() == bytes([0x80, 0x00, 0x00, 0x01])

def test_convert_min_bytes():
    int32 = Int32(bytes([0x80, 0x00, 0x00, 0x01])) #TODO: get binary value for this
    assert int32.size() == 4
    assert int32.string() == "-2147483648"
    assert int32.bytes() == bytes([0x80, 0x00, 0x00, 0x01])


# ---------------------------
# CONVERT MAX
# ---------------------------
def test_convert_max_string():
    int32 = Int32("2147483647")
    assert int32.size() == 4
    assert int32.string() == "2147483647"
    assert int32.bytes() == bytes([0x7F, 0xFF, 0xFF, 0xFF])

def test_convert_max_bytes():
    int32 = Int32(bytes([0x7F, 0xFF, 0xFF, 0xFF]))
    assert int32.size() == 4
    assert int32.string() == "2147483647"
    assert int32.bytes() == bytes([0x7F, 0xFF, 0xFF, 0xFF])


# ---------------------------
# CONVERT NEGATIVE
# ---------------------------
def test_convert_negative_string():
    int32 = Int32("-1")
    assert int32.size() == 4
    assert int32.string() == "-1"
    assert int32.bytes() == bytes([0xFF, 0xFF, 0xFF, 0xFF])

def test_convert_negative_bytes():
    int32 = Int32(bytes([0xFF, 0xFF, 0xFF, 0xFF]))
    assert int32.size() == 4
    assert int32.string() == "-1"
    assert int32.bytes() == bytes([0xFF, 0xFF, 0xFF, 0xFF])


# ---------------------------
# CONVERT POSITIVE
# ---------------------------
def test_convert_positive_string():
    int32 = Int32("1")
    assert int32.size() == 4
    assert int32.string() == "1"
    assert int32.bytes() == bytes([0x00, 0x00, 0x00, 0x01])

def test_convert_positive_bytes():
    int32 = Int32(bytes([0x00, 0x00, 0x00, 0x01]))
    assert int32.size() == 4
    assert int32.string() == "1"
    assert int32.bytes() == bytes([0x00, 0x00, 0x00, 0x01])


# ---------------------------
# TYPESYSTEM INTEGRATION
# ---------------------------
def test_typemanager_byte_added_all_names():
    for name in Int32.__typenames__:
        assert typemanager.get_type(name) is not None

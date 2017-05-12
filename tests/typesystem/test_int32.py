#from .fixtures import int32
#
#def test_init(int32):
#    assert "int32" in int32.names
#    assert int32.size == 4
#
#def test_to_string_zero(int32):
#    int32.to_string(bytes([]))
#
#def test_to_string_bad_size(int32):
#    s = int32.to_string(bytes([0xFF, 0xFF]))
#    assert s is None
#
#def test_to_string_positive(int32):
#    s = int32.to_string(bytes([0x00, 0x00, 0x00, 0x01]))
#    assert s == "1"
#
#def test_to_string_negative(int32):
#    s = int32.to_string(bytes([0xFF, 0xFF, 0xFF, 0xFF]))
#    assert s == "-1"
#
#def test_to_string_min(int32):
#    s = int32.to_string(bytes([0x7F, 0xFF, 0xFF, 0xFF]))
#    assert s == "2147483647"
#
#def test_to_string_max(int32):
#    s = int32.to_string(bytes([0x80, 0x00, 0x00, 0x00]))
#    assert s == "-2147483648"
#
#def test_to_string_none_bytes(int32):
#    s = int32.to_string(None)
#    assert s is None
#
#def test_from_string_zero(int32):
#    s = int32.from_string("")
#    assert s is None
#
#def test_from_string_positive(int32):
#    s = int32.from_string("1")
#    assert s == bytes([0x00, 0x00, 0x00, 0x01])
#
#def test_from_string_negative(int32):
#    s = int32.from_string("-1")
#    assert s == bytes([0xFF, 0xFF, 0xFF, 0xFF])
#
#def test_from_string_min(int32):
#    s = int32.from_string("2147483647")
#    assert s == bytes([0x7F, 0xFF, 0xFF, 0xFF])
#
#def test_from_string_max(int32):
#    s = int32.from_string("-2147483648")
#    assert s == bytes([0x80, 0x00, 0x00, 0x00])
#
#def test_to_string_bigger_than_4_bytes(int32):
#    s = int32.from_string("9999999999999999")
#    assert s is None
#
#def test_from_string_null_bytes(int32):
#    s = int32.from_string(None)
#    assert s is None

#from .fixtures import char
#
#def test_init(char):
#    assert "char" in char.names
#    assert char.size == 1
#
#def test_to_string_none(char):
#    s = char.to_string(None)
#    assert s is None
#
#def test_from_string_none(char):
#    s = char.from_string(None)
#    assert s is None
#
#def test_from_string_empty(char):
#    s = char.from_string("")
#    assert s is None
#
#def test_from_string_A(char):
#    s = char.from_string("A")
#    assert s is not None
#    assert len(s) == 1
#    assert s[0] == 0x41 # hex for 'A' in utf-8 & ascii
#
#def test_from_string_unprintable(char):
#    s = char.from_string("\n")
#    assert s is not None
#    assert len(s) == 1
#    assert s[0] == 0x2e # hex for '.' in utf-8 & ascii
#
#def test_to_string_empty(char):
#    s = char.from_string(bytes([]))
#    assert s is None
#
#def test_to_string_A(char):
#    pass

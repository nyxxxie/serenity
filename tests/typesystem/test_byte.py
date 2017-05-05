from tests.utils import try_convert_inverse
from .fixtures import byte

def test_init(byte):
    assert "byte" in byte.names
    assert byte.size == 1

def test_empty(byte):
    assert byte.to_string(bytes([])) is None
    assert byte.from_string("") is None

def test_none(byte):
    assert byte.to_string(None) is None
    assert byte.from_string(None) is None

def test_convert_min(byte):
    try_convert_inverse(byte, "00", bytes([0x00]))

def test_convert_max(byte):
    try_convert_inverse(byte, "FF", bytes([0xFF]))
    try_convert_inverse(byte, "ff", bytes([0xFF]))

def test_convert_all_numbers(byte):
    try_convert_inverse(byte, "43", bytes([0x43]))

def test_convert_all_letters(byte):
    try_convert_inverse(byte, "CD", bytes([0xCD]))
    try_convert_inverse(byte, "Cd", bytes([0xCD]))
    try_convert_inverse(byte, "cD", bytes([0xCD]))
    try_convert_inverse(byte, "cd", bytes([0xCD]))

def test_convert_letter_number(byte):
    try_convert_inverse(byte, "C8", bytes([0xC8]))
    try_convert_inverse(byte, "c8", bytes([0xC8]))

def test_convert_number_letter(byte):
    try_convert_inverse(byte, "6A", bytes([0x6A]))
    try_convert_inverse(byte, "6a", bytes([0x6A]))

def test_from_string_not_hex(byte):
    assert byte.from_string("not hex") is None

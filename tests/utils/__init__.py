import pytest

def try_convert_inverse(type, str_expected: str, bytes_expected: bytes):
    """
    Nice utility function to help test type conversions whose to_string and
    from_string operations are functionally inverses of each other.
    """
     # From string to bytes
    b = type.from_string(str_expected)
    if b is None:
        pytest.fail("String -> Byte result was None.")

    if len(b) != len(bytes_expected):
        pytest.fail("String -> Byte result size ({}) is not the correct size ({}).".format(len(b), len(bytes_expected)))

    if b != bytes_expected:
        pytest.fail("String -> Byte result does not match what was expected [{!r} != {!r}].".format(b, bytes_expected))

    # From bytes to string
    s = type.to_string(b)
    if s is None:
        pytest.fail("Byte -> String result was None")

    if len(s) != len(str_expected):
        pytest.fail("Byte -> String result size {} (\"{}\") is not the correct size {} (\"{}\").".format(len(s), s, len(str_expected), str_expected))

    if s != str_expected.lower():
        pytest.fail("Byte -> String result does not match what was expected [{!r} != {!r}].".format(s, str_expected))

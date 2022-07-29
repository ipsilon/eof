from eip3670 import is_valid_code, validate_code, ValidationException
import pytest

def is_invalid_with_error(code: bytes, error: str):
    with pytest.raises(ValidationException, match=error):
        validate_code(code)

def test_valid_opcodes():
    assert is_valid_code(b'\x30\x00') == True
    assert is_valid_code(b'\x50\x00') == True
    assert is_valid_code(b'\xfe\x00') == True
    assert is_valid_code(b'\xff\x00') == True

def test_push_valid_immediate():
    assert is_valid_code(b'\x60\x00\x00') == True
    assert is_valid_code(b'\x61' + b'\x00' * 2 + b'\x00') == True
    assert is_valid_code(b'\x62' + b'\x00' * 3 + b'\x00') == True
    assert is_valid_code(b'\x63' + b'\x00' * 4 + b'\x00') == True
    assert is_valid_code(b'\x64' + b'\x00' * 5 + b'\x00') == True
    assert is_valid_code(b'\x65' + b'\x00' * 6 + b'\x00') == True
    assert is_valid_code(b'\x66' + b'\x00' * 7 + b'\x00') == True
    assert is_valid_code(b'\x67' + b'\x00' * 8 + b'\x00') == True
    assert is_valid_code(b'\x68' + b'\x00' * 9 + b'\x00') == True
    assert is_valid_code(b'\x69' + b'\x00' * 10 + b'\x00') == True
    assert is_valid_code(b'\x6a' + b'\x00' * 11 + b'\x00') == True
    assert is_valid_code(b'\x6b' + b'\x00' * 12 + b'\x00') == True
    assert is_valid_code(b'\x6c' + b'\x00' * 13 + b'\x00') == True
    assert is_valid_code(b'\x6d' + b'\x00' * 14 + b'\x00') == True
    assert is_valid_code(b'\x6e' + b'\x00' * 15 + b'\x00') == True
    assert is_valid_code(b'\x6f' + b'\x00' * 16 + b'\x00') == True
    assert is_valid_code(b'\x70' + b'\x00' * 17 + b'\x00') == True
    assert is_valid_code(b'\x71' + b'\x00' * 18 + b'\x00') == True
    assert is_valid_code(b'\x72' + b'\x00' * 19 + b'\x00') == True
    assert is_valid_code(b'\x73' + b'\x00' * 20 + b'\x00') == True
    assert is_valid_code(b'\x74' + b'\x00' * 21 + b'\x00') == True
    assert is_valid_code(b'\x75' + b'\x00' * 22 + b'\x00') == True
    assert is_valid_code(b'\x76' + b'\x00' * 23 + b'\x00') == True
    assert is_valid_code(b'\x77' + b'\x00' * 24 + b'\x00') == True
    assert is_valid_code(b'\x78' + b'\x00' * 25 + b'\x00') == True
    assert is_valid_code(b'\x79' + b'\x00' * 26 + b'\x00') == True
    assert is_valid_code(b'\x7a' + b'\x00' * 27 + b'\x00') == True
    assert is_valid_code(b'\x7b' + b'\x00' * 28 + b'\x00') == True
    assert is_valid_code(b'\x7c' + b'\x00' * 29 + b'\x00') == True
    assert is_valid_code(b'\x7d' + b'\x00' * 30 + b'\x00') == True
    assert is_valid_code(b'\x7e' + b'\x00' * 31 + b'\x00') == True
    assert is_valid_code(b'\x7f' + b'\x00' * 32 + b'\x00') == True

def test_valid_code_terminator():
    assert is_valid_code(b'\x00') == True
    assert is_valid_code(b'\xf3') == True
    assert is_valid_code(b'\xfd') == True
    assert is_valid_code(b'\xfe') == True

def test_invalid_code():
    # Empty code
    assert is_valid_code(b'') == False

    # Valid opcode, but invalid as terminator
    is_invalid_with_error(b'\x5b', "no terminating instruction")
    # Invalid opcodes
    is_invalid_with_error(b'\x0c\x00', "undefined instruction")
    is_invalid_with_error(b'\x0d\x00', "undefined instruction")
    is_invalid_with_error(b'\x0e\x00', "undefined instruction")
    is_invalid_with_error(b'\x0f\x00', "undefined instruction")

    is_invalid_with_error(b'\x1e\x00', "undefined instruction")
    is_invalid_with_error(b'\x1f\x00', "undefined instruction")

    is_invalid_with_error(b'\x21\x00', "undefined instruction")
    is_invalid_with_error(b'\x22\x00', "undefined instruction")
    is_invalid_with_error(b'\x23\x00', "undefined instruction")
    is_invalid_with_error(b'\x24\x00', "undefined instruction")
    is_invalid_with_error(b'\x25\x00', "undefined instruction")
    is_invalid_with_error(b'\x26\x00', "undefined instruction")
    is_invalid_with_error(b'\x27\x00', "undefined instruction")
    is_invalid_with_error(b'\x28\x00', "undefined instruction")
    is_invalid_with_error(b'\x29\x00', "undefined instruction")
    is_invalid_with_error(b'\x2a\x00', "undefined instruction")
    is_invalid_with_error(b'\x2b\x00', "undefined instruction")
    is_invalid_with_error(b'\x2c\x00', "undefined instruction")
    is_invalid_with_error(b'\x2d\x00', "undefined instruction")
    is_invalid_with_error(b'\x2e\x00', "undefined instruction")
    is_invalid_with_error(b'\x2f\x00', "undefined instruction")

    is_invalid_with_error(b'\x49\x00', "undefined instruction")
    is_invalid_with_error(b'\x4a\x00', "undefined instruction")
    is_invalid_with_error(b'\x4b\x00', "undefined instruction")
    is_invalid_with_error(b'\x4c\x00', "undefined instruction")
    is_invalid_with_error(b'\x4d\x00', "undefined instruction")
    is_invalid_with_error(b'\x4e\x00', "undefined instruction")
    is_invalid_with_error(b'\x4f\x00', "undefined instruction")

    is_invalid_with_error(b'\x5c\x00', "undefined instruction")
    is_invalid_with_error(b'\x5d\x00', "undefined instruction")
    is_invalid_with_error(b'\x5e\x00', "undefined instruction")
    is_invalid_with_error(b'\x5f\x00', "undefined instruction")

    is_invalid_with_error(b'\xa5\x00', "undefined instruction")
    is_invalid_with_error(b'\xa6\x00', "undefined instruction")
    is_invalid_with_error(b'\xa7\x00', "undefined instruction")
    is_invalid_with_error(b'\xa8\x00', "undefined instruction")
    is_invalid_with_error(b'\xa9\x00', "undefined instruction")
    is_invalid_with_error(b'\xaa\x00', "undefined instruction")
    is_invalid_with_error(b'\xab\x00', "undefined instruction")
    is_invalid_with_error(b'\xac\x00', "undefined instruction")
    is_invalid_with_error(b'\xad\x00', "undefined instruction")
    is_invalid_with_error(b'\xae\x00', "undefined instruction")
    is_invalid_with_error(b'\xaf\x00', "undefined instruction")

    is_invalid_with_error(b'\xb0\x00', "undefined instruction")
    is_invalid_with_error(b'\xb1\x00', "undefined instruction")
    is_invalid_with_error(b'\xb2\x00', "undefined instruction")
    is_invalid_with_error(b'\xb3\x00', "undefined instruction")
    is_invalid_with_error(b'\xb4\x00', "undefined instruction")
    is_invalid_with_error(b'\xb5\x00', "undefined instruction")
    is_invalid_with_error(b'\xb6\x00', "undefined instruction")
    is_invalid_with_error(b'\xb7\x00', "undefined instruction")
    is_invalid_with_error(b'\xb8\x00', "undefined instruction")
    is_invalid_with_error(b'\xb9\x00', "undefined instruction")
    is_invalid_with_error(b'\xba\x00', "undefined instruction")
    is_invalid_with_error(b'\xbb\x00', "undefined instruction")
    is_invalid_with_error(b'\xbc\x00', "undefined instruction")
    is_invalid_with_error(b'\xbd\x00', "undefined instruction")
    is_invalid_with_error(b'\xbe\x00', "undefined instruction")
    is_invalid_with_error(b'\xbf\x00', "undefined instruction")

    is_invalid_with_error(b'\xc0\x00', "undefined instruction")
    is_invalid_with_error(b'\xc1\x00', "undefined instruction")
    is_invalid_with_error(b'\xc2\x00', "undefined instruction")
    is_invalid_with_error(b'\xc3\x00', "undefined instruction")
    is_invalid_with_error(b'\xc4\x00', "undefined instruction")
    is_invalid_with_error(b'\xc5\x00', "undefined instruction")
    is_invalid_with_error(b'\xc6\x00', "undefined instruction")
    is_invalid_with_error(b'\xc7\x00', "undefined instruction")
    is_invalid_with_error(b'\xc8\x00', "undefined instruction")
    is_invalid_with_error(b'\xc9\x00', "undefined instruction")
    is_invalid_with_error(b'\xca\x00', "undefined instruction")
    is_invalid_with_error(b'\xcb\x00', "undefined instruction")
    is_invalid_with_error(b'\xcc\x00', "undefined instruction")
    is_invalid_with_error(b'\xcd\x00', "undefined instruction")
    is_invalid_with_error(b'\xce\x00', "undefined instruction")
    is_invalid_with_error(b'\xcf\x00', "undefined instruction")

    is_invalid_with_error(b'\xd0\x00', "undefined instruction")
    is_invalid_with_error(b'\xd1\x00', "undefined instruction")
    is_invalid_with_error(b'\xd2\x00', "undefined instruction")
    is_invalid_with_error(b'\xd3\x00', "undefined instruction")
    is_invalid_with_error(b'\xd4\x00', "undefined instruction")
    is_invalid_with_error(b'\xd5\x00', "undefined instruction")
    is_invalid_with_error(b'\xd6\x00', "undefined instruction")
    is_invalid_with_error(b'\xd7\x00', "undefined instruction")
    is_invalid_with_error(b'\xd8\x00', "undefined instruction")
    is_invalid_with_error(b'\xd9\x00', "undefined instruction")
    is_invalid_with_error(b'\xda\x00', "undefined instruction")
    is_invalid_with_error(b'\xdb\x00', "undefined instruction")
    is_invalid_with_error(b'\xdc\x00', "undefined instruction")
    is_invalid_with_error(b'\xdd\x00', "undefined instruction")
    is_invalid_with_error(b'\xde\x00', "undefined instruction")
    is_invalid_with_error(b'\xdf\x00', "undefined instruction")

    is_invalid_with_error(b'\xe0\x00', "undefined instruction")
    is_invalid_with_error(b'\xe1\x00', "undefined instruction")
    is_invalid_with_error(b'\xe2\x00', "undefined instruction")
    is_invalid_with_error(b'\xe3\x00', "undefined instruction")
    is_invalid_with_error(b'\xe4\x00', "undefined instruction")
    is_invalid_with_error(b'\xe5\x00', "undefined instruction")
    is_invalid_with_error(b'\xe6\x00', "undefined instruction")
    is_invalid_with_error(b'\xe7\x00', "undefined instruction")
    is_invalid_with_error(b'\xe8\x00', "undefined instruction")
    is_invalid_with_error(b'\xe9\x00', "undefined instruction")
    is_invalid_with_error(b'\xea\x00', "undefined instruction")
    is_invalid_with_error(b'\xeb\x00', "undefined instruction")
    is_invalid_with_error(b'\xec\x00', "undefined instruction")
    is_invalid_with_error(b'\xed\x00', "undefined instruction")
    is_invalid_with_error(b'\xee\x00', "undefined instruction")
    is_invalid_with_error(b'\xef\x00', "undefined instruction")

    is_invalid_with_error(b'\xf6\x00', "undefined instruction")
    is_invalid_with_error(b'\xf7\x00', "undefined instruction")
    is_invalid_with_error(b'\xf8\x00', "undefined instruction")
    is_invalid_with_error(b'\xf9\x00', "undefined instruction")
    is_invalid_with_error(b'\xfb\x00', "undefined instruction")
    is_invalid_with_error(b'\xfc\x00', "undefined instruction")

def test_push_truncated_immediate():
    is_invalid_with_error(b'\x60', "truncated immediate")
    is_invalid_with_error(b'\x61' + b'\x00' * 1, "truncated immediate")
    is_invalid_with_error(b'\x62' + b'\x00' * 2, "truncated immediate")
    is_invalid_with_error(b'\x63' + b'\x00' * 3, "truncated immediate")
    is_invalid_with_error(b'\x64' + b'\x00' * 4, "truncated immediate")
    is_invalid_with_error(b'\x65' + b'\x00' * 5, "truncated immediate")
    is_invalid_with_error(b'\x66' + b'\x00' * 6, "truncated immediate")
    is_invalid_with_error(b'\x67' + b'\x00' * 7, "truncated immediate")
    is_invalid_with_error(b'\x68' + b'\x00' * 8, "truncated immediate")
    is_invalid_with_error(b'\x69' + b'\x00' * 9, "truncated immediate")
    is_invalid_with_error(b'\x6a' + b'\x00' * 10, "truncated immediate")
    is_invalid_with_error(b'\x6b' + b'\x00' * 11, "truncated immediate")
    is_invalid_with_error(b'\x6c' + b'\x00' * 12, "truncated immediate")
    is_invalid_with_error(b'\x6d' + b'\x00' * 13, "truncated immediate")
    is_invalid_with_error(b'\x6e' + b'\x00' * 14, "truncated immediate")
    is_invalid_with_error(b'\x6f' + b'\x00' * 15, "truncated immediate")
    is_invalid_with_error(b'\x70' + b'\x00' * 16, "truncated immediate")
    is_invalid_with_error(b'\x71' + b'\x00' * 17, "truncated immediate")
    is_invalid_with_error(b'\x72' + b'\x00' * 18, "truncated immediate")
    is_invalid_with_error(b'\x73' + b'\x00' * 19, "truncated immediate")
    is_invalid_with_error(b'\x74' + b'\x00' * 20, "truncated immediate")
    is_invalid_with_error(b'\x75' + b'\x00' * 21, "truncated immediate")
    is_invalid_with_error(b'\x76' + b'\x00' * 22, "truncated immediate")
    is_invalid_with_error(b'\x77' + b'\x00' * 23, "truncated immediate")
    is_invalid_with_error(b'\x78' + b'\x00' * 24, "truncated immediate")
    is_invalid_with_error(b'\x79' + b'\x00' * 25, "truncated immediate")
    is_invalid_with_error(b'\x7a' + b'\x00' * 26, "truncated immediate")
    is_invalid_with_error(b'\x7b' + b'\x00' * 27, "truncated immediate")
    is_invalid_with_error(b'\x7c' + b'\x00' * 28, "truncated immediate")
    is_invalid_with_error(b'\x7d' + b'\x00' * 29, "truncated immediate")
    is_invalid_with_error(b'\x7e' + b'\x00' * 30, "truncated immediate")
    is_invalid_with_error(b'\x7f' + b'\x00' * 31, "truncated immediate")

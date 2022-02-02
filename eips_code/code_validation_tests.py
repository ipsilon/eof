from typing import Callable

def test_validate_code(validate_func: Callable[[bytes], None], code: bytes) -> bool:
    try:
        validate_func(code)
        return True
    except:
        return False

def test_code_validation(validate_func: Callable[[bytes], None]):
    # Some valid opcodes
    assert test_validate_code(validate_func, b'\x30\x00') == True
    assert test_validate_code(validate_func, b'\x50\x00') == True
    assert test_validate_code(validate_func, b'\xfe\x00') == True
    assert test_validate_code(validate_func, b'\xff\x00') == True

    # PUSHes with valid immediates
    assert test_validate_code(validate_func, b'\x60\x00\x00') == True
    assert test_validate_code(validate_func, b'\x61' + b'\x00' * 2 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x62' + b'\x00' * 3 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x63' + b'\x00' * 4 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x64' + b'\x00' * 5 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x65' + b'\x00' * 6 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x66' + b'\x00' * 7 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x67' + b'\x00' * 8 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x68' + b'\x00' * 9 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x69' + b'\x00' * 10 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x6a' + b'\x00' * 11 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x6b' + b'\x00' * 12 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x6c' + b'\x00' * 13 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x6d' + b'\x00' * 14 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x6e' + b'\x00' * 15 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x6f' + b'\x00' * 16 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x70' + b'\x00' * 17 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x71' + b'\x00' * 18 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x72' + b'\x00' * 19 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x73' + b'\x00' * 20 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x74' + b'\x00' * 21 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x75' + b'\x00' * 22 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x76' + b'\x00' * 23 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x77' + b'\x00' * 24 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x78' + b'\x00' * 25 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x79' + b'\x00' * 26 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x7a' + b'\x00' * 27 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x7b' + b'\x00' * 28 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x7c' + b'\x00' * 29 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x7d' + b'\x00' * 30 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x7e' + b'\x00' * 31 + b'\x00') == True
    assert test_validate_code(validate_func, b'\x7f' + b'\x00' * 32 + b'\x00') == True

    # Valid code terminators
    assert test_validate_code(validate_func, b'\x00') == True
    assert test_validate_code(validate_func, b'\xf3') == True
    assert test_validate_code(validate_func, b'\xfd') == True
    assert test_validate_code(validate_func, b'\xfe') == True


    # Empty code
    assert test_validate_code(validate_func, b'') == False
    # Valid opcode, but invalid as terminator
    assert test_validate_code(validate_func, b'\x5b') == False
    # Invalid opcodes
    assert test_validate_code(validate_func, b'\x0c\x00') == False
    assert test_validate_code(validate_func, b'\x0d\x00') == False
    assert test_validate_code(validate_func, b'\x0e\x00') == False
    assert test_validate_code(validate_func, b'\x0f\x00') == False

    assert test_validate_code(validate_func, b'\x1e\x00') == False
    assert test_validate_code(validate_func, b'\x1f\x00') == False

    assert test_validate_code(validate_func, b'\x21\x00') == False
    assert test_validate_code(validate_func, b'\x22\x00') == False
    assert test_validate_code(validate_func, b'\x23\x00') == False
    assert test_validate_code(validate_func, b'\x24\x00') == False
    assert test_validate_code(validate_func, b'\x25\x00') == False
    assert test_validate_code(validate_func, b'\x26\x00') == False
    assert test_validate_code(validate_func, b'\x27\x00') == False
    assert test_validate_code(validate_func, b'\x28\x00') == False
    assert test_validate_code(validate_func, b'\x29\x00') == False
    assert test_validate_code(validate_func, b'\x2a\x00') == False
    assert test_validate_code(validate_func, b'\x2b\x00') == False
    assert test_validate_code(validate_func, b'\x2c\x00') == False
    assert test_validate_code(validate_func, b'\x2d\x00') == False
    assert test_validate_code(validate_func, b'\x2e\x00') == False
    assert test_validate_code(validate_func, b'\x2f\x00') == False

    assert test_validate_code(validate_func, b'\x49\x00') == False
    assert test_validate_code(validate_func, b'\x4a\x00') == False
    assert test_validate_code(validate_func, b'\x4b\x00') == False
    assert test_validate_code(validate_func, b'\x4c\x00') == False
    assert test_validate_code(validate_func, b'\x4d\x00') == False
    assert test_validate_code(validate_func, b'\x4e\x00') == False
    assert test_validate_code(validate_func, b'\x4f\x00') == False

    assert test_validate_code(validate_func, b'\x5c\x00') == False
    assert test_validate_code(validate_func, b'\x5d\x00') == False
    assert test_validate_code(validate_func, b'\x5e\x00') == False
    assert test_validate_code(validate_func, b'\x5f\x00') == False

    assert test_validate_code(validate_func, b'\xa5\x00') == False
    assert test_validate_code(validate_func, b'\xa6\x00') == False
    assert test_validate_code(validate_func, b'\xa7\x00') == False
    assert test_validate_code(validate_func, b'\xa8\x00') == False
    assert test_validate_code(validate_func, b'\xa9\x00') == False
    assert test_validate_code(validate_func, b'\xaa\x00') == False
    assert test_validate_code(validate_func, b'\xab\x00') == False
    assert test_validate_code(validate_func, b'\xac\x00') == False
    assert test_validate_code(validate_func, b'\xad\x00') == False
    assert test_validate_code(validate_func, b'\xae\x00') == False
    assert test_validate_code(validate_func, b'\xaf\x00') == False

    assert test_validate_code(validate_func, b'\xb0\x00') == False
    assert test_validate_code(validate_func, b'\xb1\x00') == False
    assert test_validate_code(validate_func, b'\xb2\x00') == False
    assert test_validate_code(validate_func, b'\xb3\x00') == False
    assert test_validate_code(validate_func, b'\xb4\x00') == False
    assert test_validate_code(validate_func, b'\xb5\x00') == False
    assert test_validate_code(validate_func, b'\xb6\x00') == False
    assert test_validate_code(validate_func, b'\xb7\x00') == False
    assert test_validate_code(validate_func, b'\xb8\x00') == False
    assert test_validate_code(validate_func, b'\xb9\x00') == False
    assert test_validate_code(validate_func, b'\xba\x00') == False
    assert test_validate_code(validate_func, b'\xbb\x00') == False
    assert test_validate_code(validate_func, b'\xbc\x00') == False
    assert test_validate_code(validate_func, b'\xbd\x00') == False
    assert test_validate_code(validate_func, b'\xbe\x00') == False
    assert test_validate_code(validate_func, b'\xbf\x00') == False

    assert test_validate_code(validate_func, b'\xc0\x00') == False
    assert test_validate_code(validate_func, b'\xc1\x00') == False
    assert test_validate_code(validate_func, b'\xc2\x00') == False
    assert test_validate_code(validate_func, b'\xc3\x00') == False
    assert test_validate_code(validate_func, b'\xc4\x00') == False
    assert test_validate_code(validate_func, b'\xc5\x00') == False
    assert test_validate_code(validate_func, b'\xc6\x00') == False
    assert test_validate_code(validate_func, b'\xc7\x00') == False
    assert test_validate_code(validate_func, b'\xc8\x00') == False
    assert test_validate_code(validate_func, b'\xc9\x00') == False
    assert test_validate_code(validate_func, b'\xca\x00') == False
    assert test_validate_code(validate_func, b'\xcb\x00') == False
    assert test_validate_code(validate_func, b'\xcc\x00') == False
    assert test_validate_code(validate_func, b'\xcd\x00') == False
    assert test_validate_code(validate_func, b'\xce\x00') == False
    assert test_validate_code(validate_func, b'\xcf\x00') == False

    assert test_validate_code(validate_func, b'\xd0\x00') == False
    assert test_validate_code(validate_func, b'\xd1\x00') == False
    assert test_validate_code(validate_func, b'\xd2\x00') == False
    assert test_validate_code(validate_func, b'\xd3\x00') == False
    assert test_validate_code(validate_func, b'\xd4\x00') == False
    assert test_validate_code(validate_func, b'\xd5\x00') == False
    assert test_validate_code(validate_func, b'\xd6\x00') == False
    assert test_validate_code(validate_func, b'\xd7\x00') == False
    assert test_validate_code(validate_func, b'\xd8\x00') == False
    assert test_validate_code(validate_func, b'\xd9\x00') == False
    assert test_validate_code(validate_func, b'\xda\x00') == False
    assert test_validate_code(validate_func, b'\xdb\x00') == False
    assert test_validate_code(validate_func, b'\xdc\x00') == False
    assert test_validate_code(validate_func, b'\xdd\x00') == False
    assert test_validate_code(validate_func, b'\xde\x00') == False
    assert test_validate_code(validate_func, b'\xdf\x00') == False

    assert test_validate_code(validate_func, b'\xe0\x00') == False
    assert test_validate_code(validate_func, b'\xe1\x00') == False
    assert test_validate_code(validate_func, b'\xe2\x00') == False
    assert test_validate_code(validate_func, b'\xe3\x00') == False
    assert test_validate_code(validate_func, b'\xe4\x00') == False
    assert test_validate_code(validate_func, b'\xe5\x00') == False
    assert test_validate_code(validate_func, b'\xe6\x00') == False
    assert test_validate_code(validate_func, b'\xe7\x00') == False
    assert test_validate_code(validate_func, b'\xe8\x00') == False
    assert test_validate_code(validate_func, b'\xe9\x00') == False
    assert test_validate_code(validate_func, b'\xea\x00') == False
    assert test_validate_code(validate_func, b'\xeb\x00') == False
    assert test_validate_code(validate_func, b'\xec\x00') == False
    assert test_validate_code(validate_func, b'\xed\x00') == False
    assert test_validate_code(validate_func, b'\xee\x00') == False
    assert test_validate_code(validate_func, b'\xef\x00') == False

    assert test_validate_code(validate_func, b'\xf6\x00') == False
    assert test_validate_code(validate_func, b'\xf7\x00') == False
    assert test_validate_code(validate_func, b'\xf8\x00') == False
    assert test_validate_code(validate_func, b'\xf9\x00') == False
    assert test_validate_code(validate_func, b'\xfb\x00') == False
    assert test_validate_code(validate_func, b'\xfc\x00') == False

    # PUSHes with truncated immediates
    assert test_validate_code(validate_func, b'\x60\x00') == False
    assert test_validate_code(validate_func, b'\x61' + b'\x00' * 1 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x62' + b'\x00' * 2 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x63' + b'\x00' * 3 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x64' + b'\x00' * 4 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x65' + b'\x00' * 5 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x66' + b'\x00' * 6 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x67' + b'\x00' * 7 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x68' + b'\x00' * 8 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x69' + b'\x00' * 9 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x6a' + b'\x00' * 10 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x6b' + b'\x00' * 11 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x6c' + b'\x00' * 12 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x6d' + b'\x00' * 13 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x6e' + b'\x00' * 14 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x6f' + b'\x00' * 15 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x70' + b'\x00' * 16 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x71' + b'\x00' * 17 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x72' + b'\x00' * 18 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x73' + b'\x00' * 19 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x74' + b'\x00' * 20 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x75' + b'\x00' * 21 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x76' + b'\x00' * 22 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x77' + b'\x00' * 23 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x78' + b'\x00' * 24 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x79' + b'\x00' * 25 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x7a' + b'\x00' * 26 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x7b' + b'\x00' * 27 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x7c' + b'\x00' * 28 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x7d' + b'\x00' * 29 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x7e' + b'\x00' * 30 + b'\x00') == False
    assert test_validate_code(validate_func, b'\x7f' + b'\x00' * 31 + b'\x00') == False


from eip3670 import is_valid_code

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
    assert is_valid_code(b'\x5b') == False
    # Invalid opcodes
    assert is_valid_code(b'\x0c\x00') == False
    assert is_valid_code(b'\x0d\x00') == False
    assert is_valid_code(b'\x0e\x00') == False
    assert is_valid_code(b'\x0f\x00') == False

    assert is_valid_code(b'\x1e\x00') == False
    assert is_valid_code(b'\x1f\x00') == False

    assert is_valid_code(b'\x21\x00') == False
    assert is_valid_code(b'\x22\x00') == False
    assert is_valid_code(b'\x23\x00') == False
    assert is_valid_code(b'\x24\x00') == False
    assert is_valid_code(b'\x25\x00') == False
    assert is_valid_code(b'\x26\x00') == False
    assert is_valid_code(b'\x27\x00') == False
    assert is_valid_code(b'\x28\x00') == False
    assert is_valid_code(b'\x29\x00') == False
    assert is_valid_code(b'\x2a\x00') == False
    assert is_valid_code(b'\x2b\x00') == False
    assert is_valid_code(b'\x2c\x00') == False
    assert is_valid_code(b'\x2d\x00') == False
    assert is_valid_code(b'\x2e\x00') == False
    assert is_valid_code(b'\x2f\x00') == False

    assert is_valid_code(b'\x49\x00') == False
    assert is_valid_code(b'\x4a\x00') == False
    assert is_valid_code(b'\x4b\x00') == False
    assert is_valid_code(b'\x4c\x00') == False
    assert is_valid_code(b'\x4d\x00') == False
    assert is_valid_code(b'\x4e\x00') == False
    assert is_valid_code(b'\x4f\x00') == False

    assert is_valid_code(b'\x5c\x00') == False
    assert is_valid_code(b'\x5d\x00') == False
    assert is_valid_code(b'\x5e\x00') == False
    assert is_valid_code(b'\x5f\x00') == False

    assert is_valid_code(b'\xa5\x00') == False
    assert is_valid_code(b'\xa6\x00') == False
    assert is_valid_code(b'\xa7\x00') == False
    assert is_valid_code(b'\xa8\x00') == False
    assert is_valid_code(b'\xa9\x00') == False
    assert is_valid_code(b'\xaa\x00') == False
    assert is_valid_code(b'\xab\x00') == False
    assert is_valid_code(b'\xac\x00') == False
    assert is_valid_code(b'\xad\x00') == False
    assert is_valid_code(b'\xae\x00') == False
    assert is_valid_code(b'\xaf\x00') == False

    assert is_valid_code(b'\xb0\x00') == False
    assert is_valid_code(b'\xb1\x00') == False
    assert is_valid_code(b'\xb2\x00') == False
    assert is_valid_code(b'\xb3\x00') == False
    assert is_valid_code(b'\xb4\x00') == False
    assert is_valid_code(b'\xb5\x00') == False
    assert is_valid_code(b'\xb6\x00') == False
    assert is_valid_code(b'\xb7\x00') == False
    assert is_valid_code(b'\xb8\x00') == False
    assert is_valid_code(b'\xb9\x00') == False
    assert is_valid_code(b'\xba\x00') == False
    assert is_valid_code(b'\xbb\x00') == False
    assert is_valid_code(b'\xbc\x00') == False
    assert is_valid_code(b'\xbd\x00') == False
    assert is_valid_code(b'\xbe\x00') == False
    assert is_valid_code(b'\xbf\x00') == False

    assert is_valid_code(b'\xc0\x00') == False
    assert is_valid_code(b'\xc1\x00') == False
    assert is_valid_code(b'\xc2\x00') == False
    assert is_valid_code(b'\xc3\x00') == False
    assert is_valid_code(b'\xc4\x00') == False
    assert is_valid_code(b'\xc5\x00') == False
    assert is_valid_code(b'\xc6\x00') == False
    assert is_valid_code(b'\xc7\x00') == False
    assert is_valid_code(b'\xc8\x00') == False
    assert is_valid_code(b'\xc9\x00') == False
    assert is_valid_code(b'\xca\x00') == False
    assert is_valid_code(b'\xcb\x00') == False
    assert is_valid_code(b'\xcc\x00') == False
    assert is_valid_code(b'\xcd\x00') == False
    assert is_valid_code(b'\xce\x00') == False
    assert is_valid_code(b'\xcf\x00') == False

    assert is_valid_code(b'\xd0\x00') == False
    assert is_valid_code(b'\xd1\x00') == False
    assert is_valid_code(b'\xd2\x00') == False
    assert is_valid_code(b'\xd3\x00') == False
    assert is_valid_code(b'\xd4\x00') == False
    assert is_valid_code(b'\xd5\x00') == False
    assert is_valid_code(b'\xd6\x00') == False
    assert is_valid_code(b'\xd7\x00') == False
    assert is_valid_code(b'\xd8\x00') == False
    assert is_valid_code(b'\xd9\x00') == False
    assert is_valid_code(b'\xda\x00') == False
    assert is_valid_code(b'\xdb\x00') == False
    assert is_valid_code(b'\xdc\x00') == False
    assert is_valid_code(b'\xdd\x00') == False
    assert is_valid_code(b'\xde\x00') == False
    assert is_valid_code(b'\xdf\x00') == False

    assert is_valid_code(b'\xe0\x00') == False
    assert is_valid_code(b'\xe1\x00') == False
    assert is_valid_code(b'\xe2\x00') == False
    assert is_valid_code(b'\xe3\x00') == False
    assert is_valid_code(b'\xe4\x00') == False
    assert is_valid_code(b'\xe5\x00') == False
    assert is_valid_code(b'\xe6\x00') == False
    assert is_valid_code(b'\xe7\x00') == False
    assert is_valid_code(b'\xe8\x00') == False
    assert is_valid_code(b'\xe9\x00') == False
    assert is_valid_code(b'\xea\x00') == False
    assert is_valid_code(b'\xeb\x00') == False
    assert is_valid_code(b'\xec\x00') == False
    assert is_valid_code(b'\xed\x00') == False
    assert is_valid_code(b'\xee\x00') == False
    assert is_valid_code(b'\xef\x00') == False

    assert is_valid_code(b'\xf6\x00') == False
    assert is_valid_code(b'\xf7\x00') == False
    assert is_valid_code(b'\xf8\x00') == False
    assert is_valid_code(b'\xf9\x00') == False
    assert is_valid_code(b'\xfb\x00') == False
    assert is_valid_code(b'\xfc\x00') == False

def test_push_truncated_immediate():
    assert is_valid_code(b'\x60\x00') == False
    assert is_valid_code(b'\x61' + b'\x00' * 1 + b'\x00') == False
    assert is_valid_code(b'\x62' + b'\x00' * 2 + b'\x00') == False
    assert is_valid_code(b'\x63' + b'\x00' * 3 + b'\x00') == False
    assert is_valid_code(b'\x64' + b'\x00' * 4 + b'\x00') == False
    assert is_valid_code(b'\x65' + b'\x00' * 5 + b'\x00') == False
    assert is_valid_code(b'\x66' + b'\x00' * 6 + b'\x00') == False
    assert is_valid_code(b'\x67' + b'\x00' * 7 + b'\x00') == False
    assert is_valid_code(b'\x68' + b'\x00' * 8 + b'\x00') == False
    assert is_valid_code(b'\x69' + b'\x00' * 9 + b'\x00') == False
    assert is_valid_code(b'\x6a' + b'\x00' * 10 + b'\x00') == False
    assert is_valid_code(b'\x6b' + b'\x00' * 11 + b'\x00') == False
    assert is_valid_code(b'\x6c' + b'\x00' * 12 + b'\x00') == False
    assert is_valid_code(b'\x6d' + b'\x00' * 13 + b'\x00') == False
    assert is_valid_code(b'\x6e' + b'\x00' * 14 + b'\x00') == False
    assert is_valid_code(b'\x6f' + b'\x00' * 15 + b'\x00') == False
    assert is_valid_code(b'\x70' + b'\x00' * 16 + b'\x00') == False
    assert is_valid_code(b'\x71' + b'\x00' * 17 + b'\x00') == False
    assert is_valid_code(b'\x72' + b'\x00' * 18 + b'\x00') == False
    assert is_valid_code(b'\x73' + b'\x00' * 19 + b'\x00') == False
    assert is_valid_code(b'\x74' + b'\x00' * 20 + b'\x00') == False
    assert is_valid_code(b'\x75' + b'\x00' * 21 + b'\x00') == False
    assert is_valid_code(b'\x76' + b'\x00' * 22 + b'\x00') == False
    assert is_valid_code(b'\x77' + b'\x00' * 23 + b'\x00') == False
    assert is_valid_code(b'\x78' + b'\x00' * 24 + b'\x00') == False
    assert is_valid_code(b'\x79' + b'\x00' * 25 + b'\x00') == False
    assert is_valid_code(b'\x7a' + b'\x00' * 26 + b'\x00') == False
    assert is_valid_code(b'\x7b' + b'\x00' * 27 + b'\x00') == False
    assert is_valid_code(b'\x7c' + b'\x00' * 28 + b'\x00') == False
    assert is_valid_code(b'\x7d' + b'\x00' * 29 + b'\x00') == False
    assert is_valid_code(b'\x7e' + b'\x00' * 30 + b'\x00') == False
    assert is_valid_code(b'\x7f' + b'\x00' * 31 + b'\x00') == False

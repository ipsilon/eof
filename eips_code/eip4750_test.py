from eip4750 import is_valid_code, validate_code_section, ValidationException
import pytest

def is_invalid_with_error(code: bytes, error: str, num_code_sections: int = 1):
    with pytest.raises(ValidationException, match=error):
        validate_code_section(code, num_code_sections)

def test_valid_opcodes():
    assert is_valid_code(b'\x30\x00') == True
    assert is_valid_code(b'\x50\x00') == True
    assert is_valid_code(b'\xfb\x00\x00\x00') == True
    assert is_valid_code(b'\xfc') == True
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

def test_rjump_valid_immediate():
    # offset = 0
    assert is_valid_code(b'\x5c\x00\x00\x00') == True
    # offset = 1
    assert is_valid_code(b'\x5c\x00\x01\x00\x00') == True
    # offset = 4
    assert is_valid_code(b'\x5c\x00\x01\x00\x00\x00\x00\x00') == True
    # offset = 256
    assert is_valid_code(b'\x5c\x01\x00' + b'\x00' * 256 + b'\x00') == True
    # offset = 32767
    assert is_valid_code(b'\x5c\x7f\xff' + b'\x00' * 32767 + b'\x00') == True
    # offset = -3
    assert is_valid_code(b'\x5c\xff\xfd\x00\x00') == True
    # offset = -4
    assert is_valid_code(b'\x00\x5c\xff\xfc\x00') == True
    # offset = -256
    assert is_valid_code(b'\x00' * 253 + b'\x5c\xff\x00\x00') == True
    # offset = -32768
    assert is_valid_code(b'\x00' * 32765 + b'\x5c\x80\x01\x00') == True

def test_rjumpi_valid_immediate():
    # offset = 0
    assert is_valid_code(b'\x60\x01\x5d\x00\x00\x00') == True
    # offset = 1
    assert is_valid_code(b'\x60\x01\x5d\x00\x01\x00\x00') == True
    # offset = 4
    assert is_valid_code(b'\x60\x01\x5d\x00\x01\x00\x00\x00\x00\x00') == True
    # offset = 256
    assert is_valid_code(b'\x60\x01\x5d\x01\x00' + b'\x00' * 256 + b'\x00') == True
    # offset = 32767
    assert is_valid_code(b'\x60\x01\x5d\x7f\xff' + b'\x00' * 32767 + b'\x00') == True
    # offset = -3
    assert is_valid_code(b'\x60\x01\x5d\xff\xfd\x00\x00') == True
    # offset = -5
    assert is_valid_code(b'\x60\x01\x5d\xff\xfb\x00') == True
    # offset = -256
    assert is_valid_code(b'\x00' * 252 + b'\x60\x01\x5d\xff\x00\x00') == True
    # offset = -32768
    assert is_valid_code(b'\x00' * 32763 + b'\x60\x01\x5d\x80\x01\x00') == True
    # RJUMP without PUSH before - still valid
    assert is_valid_code(b'\x5d\x00\x00\x00') == True

def test_callf_valid_immediate():
    assert is_valid_code(b'\xfb\x00\x00\x00') == True
    assert is_valid_code(b'\xfb\x00\x01\x00', 2) == True
    assert is_valid_code(b'\xfb\x00\x00\x00', 10) == True
    assert is_valid_code(b'\xfb\x00\x01\x00', 10) == True
    assert is_valid_code(b'\xfb\x00\x02\x00', 10) == True
    assert is_valid_code(b'\xfb\x00\x03\x00', 10) == True
    assert is_valid_code(b'\xfb\x00\x04\x00', 10) == True
    assert is_valid_code(b'\xfb\x00\x05\x00', 10) == True
    assert is_valid_code(b'\xfb\x00\x06\x00', 10) == True
    assert is_valid_code(b'\xfb\x00\x07\x00', 10) == True
    assert is_valid_code(b'\xfb\x00\x08\x00', 10) == True
    assert is_valid_code(b'\xfb\x00\x09\x00', 10) == True
    assert is_valid_code(b'\xfb\xff\xff\x00', 65536) == True


def test_valid_code_terminator():
    assert is_valid_code(b'\x00') == True
    assert is_valid_code(b'\xf3') == True
    assert is_valid_code(b'\xfc') == True
    assert is_valid_code(b'\xfd') == True
    assert is_valid_code(b'\xfe') == True


def test_invalid_code():
    # Empty code
    assert is_valid_code(b'') == False

    # Valid opcode, but invalid as terminator
    is_invalid_with_error(b'\x5b', "no terminating instruction")
    is_invalid_with_error(b'\xfb\x00\x00', "no terminating instruction")
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

def test_rjump_truncated_immediate():
    is_invalid_with_error(b'\x5c', "truncated relative jump offset")
    is_invalid_with_error(b'\x5c\x00', "truncated relative jump offset")
    is_invalid_with_error(b'\x5c\x00\x00', "relative jump destination out of bounds")

def test_rjumpi_truncated_immediate():
    is_invalid_with_error(b'\x60\x01\x5d', "truncated relative jump offset")
    is_invalid_with_error(b'\x60\x01\x5d\x00', "truncated relative jump offset")
    is_invalid_with_error(b'\x60\x01\x5d\x00\x00', "relative jump destination out of bounds")

def test_callf_truncated_immediate():
    is_invalid_with_error(b'\xfb', "truncated CALLF immediate")
    is_invalid_with_error(b'\xfb\x00', "truncated CALLF immediate")

def test_rjumps_out_of_bounds():
    # RJUMP destination out of bounds
    # offset = 1
    is_invalid_with_error(b'\x5c\x00\x01\x00', "relative jump destination out of bounds")
    # offset = -4
    is_invalid_with_error(b'\x5c\xff\xfc\x00', "relative jump destination out of bounds")
    # RJUMPI destination out of bounds
    # offset = 1
    is_invalid_with_error(b'\x60\x01\x5d\x00\x01\x00', "relative jump destination out of bounds")
    # offset = -6
    is_invalid_with_error(b'\x60\x01\x5d\xff\xfa\x00', "relative jump destination out of bounds")

def test_rjumps_into_immediate():
    for n in range(1, 33):
        for offset in range(1, n + 1):
            code = [0x5c, 0x00, offset] # RJUMP offset
            code += [0x60 + n - 1] # PUSHn
            code += [0x00] * n     # push data
            code += [0x00]         # STOP

            is_invalid_with_error(code, "relative jump destination targets immediate")

            code = [0x60, 0x01, 0x5d, 0x00, offset] # PUSH1 1 RJUMI offset
            code += [0x60 + n - 1] # PUSHn
            code += [0x00] * n     # push data
            code += [0x00]         # STOP

            is_invalid_with_error(code, "relative jump destination targets immediate")

    # RJUMP into RJUMP immediate
    is_invalid_with_error(b'\x5c\x00\x01\x5c\x00\x00\x00', "relative jump destination targets immediate")
    is_invalid_with_error(b'\x5c\x00\x02\x5c\x00\x00\x00', "relative jump destination targets immediate")
    # RJUMPI into RJUMP immediate
    is_invalid_with_error(b'\x60\x01\x5d\x00\x01\x5c\x00\x00\x00', "relative jump destination targets immediate")
    is_invalid_with_error(b'\x60\x01\x5d\x00\x02\x5c\x00\x00\x00', "relative jump destination targets immediate")
    # RJUMP into RJUMPI immediate
    is_invalid_with_error(b'\x5c\x00\x03\x60\x01\x5d\x00\x00\x00', "relative jump destination targets immediate")
    is_invalid_with_error(b'\x5c\x00\x04\x60\x01\x5d\x00\x00\x00', "relative jump destination targets immediate")
    # RJUMPI into RJUMPI immediate
    is_invalid_with_error(b'\x60\x01\x5d\x00\x03\x60\x01\x5d\x00\x00\x00', "relative jump destination targets immediate")
    is_invalid_with_error(b'\x60\x01\x5d\x00\x04\x60\x01\x5d\x00\x00\x00', "relative jump destination targets immediate")
    # RJUMP into CALLF immediate
    is_invalid_with_error(b'\x5c\x00\x01\xfb\x00\x00\x00', "relative jump destination targets immediate")
    is_invalid_with_error(b'\x5c\x00\x02\xfb\x00\x00\x00', "relative jump destination targets immediate")
    # RJUMPI into CALLF immediate
    is_invalid_with_error(b'\x60\x01\x5d\x00\x01\xfb\x00\x00\x00', "relative jump destination targets immediate")
    is_invalid_with_error(b'\x60\x01\x5d\x00\x01\xfb\x00\x00\x00', "relative jump destination targets immediate")

def test_callf_invalid_section_id():
    is_invalid_with_error(b'\xfb\x00\x01\x00', "invalid section id", 1)
    is_invalid_with_error(b'\xfb\x00\x02\x00', "invalid section id", 1)
    is_invalid_with_error(b'\xfb\x00\x0a\x00', "invalid section id", 1)
    is_invalid_with_error(b'\xfb\xff\xff\x00', "invalid section id", 1)
    is_invalid_with_error(b'\xfb\x00\x0a\x00', "invalid section id", 10)
    is_invalid_with_error(b'\xfb\xff\xff\x00', "invalid section id", 65535)

def test_immediate_contains_opcode():
    # 0x5c byte which could be interpreted a RJUMP, but it's not because it's in PUSH data
    assert is_valid_code(b'\x60\x5c\x00\x10\x00') == True
    assert is_valid_code(b'\x61\x00\x5c\x00\x10\x00') == True
    # 0x5d byte which could be interpreted a RJUMPI, but it's not because it's in PUSH data
    assert is_valid_code(b'\x60\x5d\x00\x10\x00') == True
    assert is_valid_code(b'\x61\x00\x5d\x00\x10\x00') == True
    # 0xfb byte which could be interpreted a CALLF, but it's not because it's in PUSH data
    assert is_valid_code(b'\x60\xfb\x00\x10\x00') == True
    assert is_valid_code(b'\x61\x00\xfb\x00\x10\x00') == True

    # 0x60 byte which could be interpreted as PUSH, but it's not because it's in RJUMP data
    # offset = -160
    assert is_valid_code(b'0x00' * 160 + b'\x5c\xff\x60\x00') == True
    # 0x60 byte which could be interpreted as PUSH, but it's not because it's in RJUMPI data
    # offset = -160
    assert is_valid_code(b'0x00' * 160 + b'\x5d\xff\x60\x00') == True
    # 0x60 byte which could be interpreted as PUSH, but it's not because it's in CALLF data
    # section_id = 96
    assert is_valid_code(b'\xfb\x00\x60\x00', 97) == True

    # 0x5c byte which could be interpreted a RJUMP, but it's not because it's in CALLF data
    # section_id = 92
    assert is_valid_code(b'\xfb\x00\x5c\x00\x00', 93) == True
    # 0x5d byte which could be interpreted a RJUMPI, but it's not because it's in CALLF data
    # section_id = 93
    assert is_valid_code(b'\xfb\x00\x5d\x00\x00', 94) == True

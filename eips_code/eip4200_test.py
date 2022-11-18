from eip4200 import is_valid_code, validate_code, ValidationException
import pytest

def is_invalid_with_error(code: bytes, error: str):
    with pytest.raises(ValidationException, match=error):
        validate_code(code)

def test_valid_opcodes():
    assert is_valid_code(bytes.fromhex("3000")) == True
    assert is_valid_code(bytes.fromhex("5000")) == True
    assert is_valid_code(bytes.fromhex("fe00")) == True
    assert is_valid_code(bytes.fromhex("0000")) == True

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
    assert is_valid_code(bytes.fromhex("5c000000")) == True
    # offset = 1
    assert is_valid_code(bytes.fromhex("5c00010000")) == True
    # offset = 4
    assert is_valid_code(bytes.fromhex("5c00010000000000")) == True
    # offset = 256
    assert is_valid_code(bytes.fromhex("5c0100") + b'\x00' * 256 + b'\x00') == True
    # offset = 32767
    assert is_valid_code(bytes.fromhex("5c7fff") + b'\x00' * 32767 + b'\x00') == True
    # offset = -3
    assert is_valid_code(bytes.fromhex("5cfffd0000")) == True
    # offset = -4
    assert is_valid_code(bytes.fromhex("005cfffc00")) == True
    # offset = -256
    assert is_valid_code(b'\x00' * 253 + bytes.fromhex("5cff0000")) == True
    # offset = -32768
    assert is_valid_code(b'\x00' * 32765 + bytes.fromhex("5c800100")) == True

def test_rjumpi_valid_immediate():
    # offset = 0
    assert is_valid_code(bytes.fromhex("60015d000000")) == True
    # offset = 1
    assert is_valid_code(bytes.fromhex("60015d00010000")) == True
    # offset = 4
    assert is_valid_code(bytes.fromhex("60015d00010000000000")) == True
    # offset = 256
    assert is_valid_code(bytes.fromhex("60015d0100") + b'\x00' * 256 + b'\x00') == True
    # offset = 32767
    assert is_valid_code(bytes.fromhex("60015d7fff") + b'\x00' * 32767 + b'\x00') == True
    # offset = -3
    assert is_valid_code(bytes.fromhex("60015dfffd0000")) == True
    # offset = -5
    assert is_valid_code(bytes.fromhex("60015dfffb00")) == True
    # offset = -256
    assert is_valid_code(b'\x00' * 252 + bytes.fromhex("60015dff0000")) == True
    # offset = -32768
    assert is_valid_code(b'\x00' * 32763 + bytes.fromhex("60015d800100")) == True
    # RJUMP without PUSH before - still valid
    assert is_valid_code(bytes.fromhex("5d000000")) == True


def test_valid_code_terminator():
    assert is_valid_code(b'\x00') == True
    assert is_valid_code(b'\xf3') == True
    assert is_valid_code(b'\xfd') == True
    assert is_valid_code(b'\xfe') == True


def test_invalid_code():
    # Empty code
    assert is_valid_code(b'') == False

    # Valid opcode, but invalid as terminator
    is_invalid_with_error(bytes.fromhex("5b"), "no terminating instruction")
    # Invalid opcodes
    is_invalid_with_error(bytes.fromhex("0c00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("0d00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("0e00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("0f00"), "undefined instruction")

    is_invalid_with_error(bytes.fromhex("1e00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("1f00"), "undefined instruction")

    is_invalid_with_error(bytes.fromhex("2100"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2200"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2300"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2400"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2500"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2600"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2700"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2800"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2900"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2a00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2b00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2c00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2d00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2e00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("2f00"), "undefined instruction")

    is_invalid_with_error(bytes.fromhex("4900"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("4a00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("4b00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("4c00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("4d00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("4e00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("4f00"), "undefined instruction")

    is_invalid_with_error(bytes.fromhex("5e00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("5f00"), "undefined instruction")

    is_invalid_with_error(bytes.fromhex("a500"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("a600"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("a700"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("a800"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("a900"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("aa00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ab00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ac00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ad00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ae00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("af00"), "undefined instruction")

    is_invalid_with_error(bytes.fromhex("b000"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("b100"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("b200"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("b300"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("b400"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("b500"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("b600"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("b700"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("b800"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("b900"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ba00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("bb00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("bc00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("bd00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("be00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("bf00"), "undefined instruction")

    is_invalid_with_error(bytes.fromhex("c000"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("c100"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("c200"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("c300"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("c400"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("c500"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("c600"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("c700"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("c800"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("c900"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ca00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("cb00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("cc00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("cd00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ce00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("cf00"), "undefined instruction")

    is_invalid_with_error(bytes.fromhex("d000"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("d100"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("d200"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("d300"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("d400"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("d500"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("d600"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("d700"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("d800"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("d900"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("da00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("db00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("dc00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("dd00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("de00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("df00"), "undefined instruction")

    is_invalid_with_error(bytes.fromhex("e000"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("e100"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("e200"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("e300"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("e400"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("e500"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("e600"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("e700"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("e800"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("e900"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ea00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("eb00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ec00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ed00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ee00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("ef00"), "undefined instruction")

    is_invalid_with_error(bytes.fromhex("f600"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("f700"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("f800"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("f900"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("fb00"), "undefined instruction")
    is_invalid_with_error(bytes.fromhex("fc00"), "undefined instruction")

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
    is_invalid_with_error(bytes.fromhex("5c"), "truncated relative jump offset")
    is_invalid_with_error(bytes.fromhex("5c00"), "truncated relative jump offset")
    is_invalid_with_error(bytes.fromhex("5c0000"), "invalid jump target")

def test_rjumpi_truncated_immediate():
    is_invalid_with_error(bytes.fromhex("60015d"), "truncated relative jump offset")
    is_invalid_with_error(bytes.fromhex("60015d00"), "truncated relative jump offset")
    is_invalid_with_error(bytes.fromhex("60015d0000"), "invalid jump target")

def test_rjumps_out_of_bounds():
    # RJUMP destination out of bounds
    # offset = 1
    is_invalid_with_error(bytes.fromhex("5c000100"), "invalid jump target")
    # offset = -4
    is_invalid_with_error(bytes.fromhex("5cfffc00"), "invalid jump target")
    # RJUMPI destination out of bounds
    # offset = 1
    is_invalid_with_error(bytes.fromhex("60015d000100"), "invalid jump target")
    # offset = -6
    is_invalid_with_error(bytes.fromhex("60015dfffa00"), "invalid jump target")

def test_rjumps_into_immediate():
    for n in range(1, 33):
        for offset in range(1, n + 1):
            code = [0x5c, 0x00, offset] # RJUMP offset
            code += [0x60 + n - 1] # PUSHn
            code += [0x00] * n     # push data
            code += [0x00]         # STOP

            is_invalid_with_error(code, "invalid jump target")

            code = [0x60, 0x01, 0x5d, 0x00, offset] # PUSH1 1 RJUMI offset
            code += [0x60 + n - 1] # PUSHn
            code += [0x00] * n     # push data
            code += [0x00]         # STOP

            is_invalid_with_error(code, "invalid jump target")

    # RJUMP into RJUMP immediate
    is_invalid_with_error(bytes.fromhex("5c00015c000000"), "invalid jump target")
    is_invalid_with_error(bytes.fromhex("5c00025c000000"), "invalid jump target")
    # RJUMPI into RJUMP immediate
    is_invalid_with_error(bytes.fromhex("60015d00015c000000"), "invalid jump target")
    is_invalid_with_error(bytes.fromhex("60015d00025c000000"), "invalid jump target")
    # RJUMP into RJUMPI immediate
    is_invalid_with_error(bytes.fromhex("5c000360015d000000"), "invalid jump target")
    is_invalid_with_error(bytes.fromhex("5c000460015d000000"), "invalid jump target")
    # RJUMPI into RJUMPI immediate
    is_invalid_with_error(bytes.fromhex("60015d000360015d000000"), "invalid jump target")
    is_invalid_with_error(bytes.fromhex("60015d000460015d000000"), "invalid jump target")

def test_immediate_contains_opcode():
    # 0x5c byte which could be interpreted a RJUMP, but it's not because it's in PUSH data
    assert is_valid_code(bytes.fromhex("605c001000")) == True
    assert is_valid_code(bytes.fromhex("61005c001000")) == True
    # 0x5d byte which could be interpreted a RJUMPI, but it's not because it's in PUSH data
    assert is_valid_code(bytes.fromhex("605d001000")) == True
    assert is_valid_code(bytes.fromhex("61005d001000")) == True

    # 0x60 byte which could be interpreted as PUSH, but it's not because it's in RJUMP data
    # offset = -160
    assert is_valid_code(b'0x00' * 160 + bytes.fromhex("5cff6000")) == True
    # 0x60 byte which could be interpreted as PUSH, but it's not because it's in RJUMPI data
    # offset = -160
    assert is_valid_code(b'0x00' * 160 + bytes.fromhex("5dff6000")) == True

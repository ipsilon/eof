from eof1_validation import validate_eof1, ValidationException
import pytest


def is_valid_eof(code: bytes) -> bool:
    try:
        validate_eof1(code)
    except:
        return False
    return True


def is_invalid_eof_with_error(code: bytes, error: str):
    with pytest.raises(ValidationException, match=error):
        validate_eof1(code)


def test_valid_eof1_container():
    # Single code section
    assert is_valid_eof(bytes.fromhex("ef000101000100fe"))
    # Code section and data section
    assert is_valid_eof(bytes.fromhex("ef000101000102000100feaa"))
    # Type section and two code sections
    assert is_valid_eof(bytes.fromhex("ef0001 030004 010001 010003 00 00000001 fe 6000fc"))
    # Type section, two code sections, data section
    assert is_valid_eof(bytes.fromhex("ef0001 030004 010001 010002 020004 00 00000201 fe 50fc aabbccdd"))

    # Example with 3 functions
    assert is_valid_eof(bytes.fromhex("ef0001 030006 01003b 010017 01001d 00 000001010101 "
                                      "60043560e06000351c639fb890d581145d001c6320cb776181145d00065050600080fd50fb000260005260206000f350fb000160005260206000f3"
                                      "600181115d0004506001fc60018103fb000281029050fc 600281115d0004506001fc60028103fb000160018203fb0001019050fc"))


def test_invalid_eof1_container():
    # EIP-3540 violation - malformed container
    is_invalid_eof_with_error(bytes.fromhex("ef0001 010001 020002 00 fe aa"), "container size not equal to sum of section sizes")
    # EIP-3670 violation - undefined opcode
    is_invalid_eof_with_error(bytes.fromhex("ef0001 010002 00 f600"), "undefined instruction")
    # EIP-4200 violation - invalid RJUMP
    is_invalid_eof_with_error(bytes.fromhex("ef0001 010004 00 5c00ff00"), "relative jump destination out of bounds")
    # EIP-4750 violation - invalid CALLF
    is_invalid_eof_with_error(bytes.fromhex("ef0001 030004 010005 010003 00 00000001 fbffff5000 6000fc"), "invalid section id")
    # EIP-5450 violation - stack underflow
    is_invalid_eof_with_error(bytes.fromhex("ef0001 030004 010005 010004 00 00000001 fb00015000 600001fc"), "stack underflow")

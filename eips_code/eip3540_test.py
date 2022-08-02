from eip3540 import is_valid_container, validate_eof, ValidationException
import pytest

def is_invalid_with_error(code: bytes, error: str):
    with pytest.raises(ValidationException, match=error):
        validate_eof(code)

def test_legacy_contracts():
    assert is_valid_container(b'') == True
    assert is_valid_container(b'\x00') == True
    assert is_valid_container(b'\xef') == True  # Magic second byte missing

def test_no_eof_magic():
    # Any value outside the magic second byte
    for m in range(1, 256):
        assert is_valid_container(bytes((0xEF, m))) == True

def test_eof1_container():
    is_invalid_with_error(b'\xef\x00', "invalid version")
    is_invalid_with_error(b'\xef\x00\x01', "no section terminator")
    is_invalid_with_error(b'\xef\x00\x00', "invalid version")
    is_invalid_with_error(b'\xef\x00\x02\x01\x00\x01\x00\xfe', "invalid version") # Valid except version
    is_invalid_with_error(b'\xef\x00\x01\x00', "no code section") # Only terminator
    is_invalid_with_error(b'\xef\x00\x01\x01\x00\x01\x00\xfe\xaa\xbb\xcc\xdd', "container size not equal to sum of section sizes") # Trailing bytes
    is_invalid_with_error(b'\xef\x00\x01\x01', "truncated section size")
    is_invalid_with_error(b'\xef\x00\x01\x01\x00\x01\x02', "truncated section size")
    is_invalid_with_error(b'\xef\x00\x01\x03', "invalid section id")
    is_invalid_with_error(b'\xef\x00\x01\x01\x00', "truncated section size")
    is_invalid_with_error(b'\xef\x00\x01\x01\x00\x01\x02\x00', "truncated section size")
    is_invalid_with_error(b'\xef\x00\x01\x01\x00\x00\x00', "empty section")
    is_invalid_with_error(b'\xef\x00\x01\x01\x00\x01\x02\x00\x00\x00\xfe', "empty section")
    is_invalid_with_error(b'\xef\x00\x01\x01\x00\x01', "no section terminator")
    is_invalid_with_error(b'\xef\x00\x01\x01\x00\x01\x00', "container size not equal to sum of section sizes") # Missing section contents
    is_invalid_with_error(b'\xef\x00\x01\x02\x00\x01\x00\xaa', "data section preceding code section") # Only data section
    is_invalid_with_error(b'\xef\x00\x01\x01\x00\x01\x01\x00\x01\x00\xfe\xfe', "multiple sections with same id") # Multiple code sections
    is_invalid_with_error(b'\xef\x00\x01\x01\x00\x01\x02\x00\x01\x02\x00\x01\x00\xfe\xaa\xbb', "multiple sections with same id") # Multiple data sections
    is_invalid_with_error(b'\xef\x00\x01\x01\x00\x01\x01\x00\x01\x02\x00\x01\x02\x00\x01\x00\xfe\xfe\xaa\xbb', "multiple sections with same id")# Multiple code and data sections
    is_invalid_with_error(b'\xef\x00\x01\x02\x00\x01\x01\x00\x01\x00\xaa\xfe', "data section preceding code section")

    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01\x00\xfe') == True  # Valid format with 1-byte of code
    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01\x02\x00\x01\x00\xfe\xaa') == True  # Code and data section

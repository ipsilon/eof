from eip3540 import is_valid_container

def test_legacy_contracts():
    assert is_valid_container(b'') == True
    assert is_valid_container(b'\x00') == True
    assert is_valid_container(b'\xef') == True  # Magic second byte missing

def test_no_eof_magic():
    # Any value outside the magic second byte
    for m in range(1, 256):
        assert is_valid_container(bytes((0xEF, m))) == True

def test_eof1_container():
    assert is_valid_container(b'\xef\x00') == False  # Only magic
    assert is_valid_container(b'\xef\x00\x01') == False  # Only version
    assert is_valid_container(b'\xef\x00\x00') == False  # Wrong version
    assert is_valid_container(b'\xef\x00\x02\x01\x00\x01\x00\xfe') == False  # Valid except version
    assert is_valid_container(b'\xef\x00\x01\x00') == False  # Only terminator
    assert is_valid_container(b'\xef\x00\x01\x00\x000') == False  # Trailing bytes
    assert is_valid_container(b'\xef\x00\x01\x01') == False  # Truncated section header
    assert is_valid_container(b'\xef\x00\x01\x02') == False  # Truncated section header
    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01\x02') == False  # Truncated section header
    assert is_valid_container(b'\xef\x00\x01\x03') == False  # Invalid section id
    assert is_valid_container(b'\xef\x00\x01\x01\x00') == False  # Truncated code section size
    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01\x02\x00') == False  # Truncated data section size
    assert is_valid_container(b'\xef\x00\x01\x01\x00\x00\x00') == False  # Empty code section size
    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01\x02\x00\x00\x00\xfe') == False  # Empty data section
    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01') == False  # No terminator after section
    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01\x00') == False  # Missing section contents
    assert is_valid_container(b'\xef\x00\x01\x02\x00\x01\x00\xaa') == False  # Only data section
    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01\x01\x00\x01\x00\xfe\xfe') == False  # Multiple code sections
    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01\x02\x00\x01\x02\x00\x01\x00\xfe\xaa\xbb') == False  # Multiple data sections
    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01\x01\x00\x01\x02\x00\x01\x02\x00\x01\x00\xfe\xfe\xaa\xbb') == False  # Multiple code and data sections
    assert is_valid_container(b'\xef\x00\x01\x02\x00\x01\x01\x00\x01\x00\xaa\xfe') == False  # Data section before code section

    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01\x00\xfe') == True  # Valid format with 1-byte of code
    assert is_valid_container(b'\xef\x00\x01\x01\x00\x01\x02\x00\x01\x00\xfe\xaa') == True  # Code and data section

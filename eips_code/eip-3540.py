FORMAT = 0xEF
MAGIC = 0x00
VERSION = 0x01
S_TERMINATOR = 0x00
S_CODE = 0x01
S_DATA = 0x02


# Determines if code is in EOF format of any version.
def is_eof(code: bytes) -> bool:
    return len(code) >= 2 and code[0] == FORMAT and code[1] == MAGIC


# Validate EOF code.
def validate_eof(code: bytes):
    # Check version
    assert len(code) >= 3 and code[2] == VERSION

    # Process section headers
    section_sizes = {S_CODE: 0, S_DATA: 0}
    pos = 3
    while True:
        # Terminator not found
        assert pos < len(code)
        section_id = code[pos]
        pos += 1
        if section_id == S_TERMINATOR:
            break

        # Disallow unknown sections
        assert section_id in section_sizes

        # Data section preceding code section
        assert section_id != S_DATA or section_sizes[S_CODE] != 0

        # Multiple sections with the same id
        assert section_sizes[section_id] == 0

        # Truncated section size
        assert (pos + 1) < len(code)
        section_sizes[section_id] = (code[pos] << 8) | code[pos + 1]
        pos += 2

        # Empty section
        assert section_sizes[section_id] != 0

    # Code section cannot be absent
    assert section_sizes[S_CODE] != 0

    # The entire container must be scanned
    assert len(code) == (pos + section_sizes[S_CODE] + section_sizes[S_DATA])


# Validates any code
def validate_code(code: bytes) -> bool:
    if is_eof(code):
        try:
            validate_eof(code)
        except:
            return False
    return True


# Legacy contracts
assert validate_code(b'') == True
assert validate_code(b'\x00') == True
assert validate_code(b'\xef') == True  # Magic byte missing

# Any value outside the magic
for magic in range(1, 256):
    assert validate_code(bytes((0xEF, magic))) == True

# EOF1 contracts
assert validate_code(b'\xef\x00') == False  # Only magic
assert validate_code(b'\xef\x00\x01') == False  # Only version
assert validate_code(b'\xef\x00\x00') == False  # Wrong version
assert validate_code(b'\xef\x00\x02\x01\x00\x01\x00\xfe') == False  # Valid except version
assert validate_code(b'\xef\x00\x01\x00') == False  # Only terminator
assert validate_code(b'\xef\x00\x01\x00\x000') == False  # Trailing bytes
assert validate_code(b'\xef\x00\x01\x01') == False  # Truncated section header
assert validate_code(b'\xef\x00\x01\x02') == False  # Truncated section header
assert validate_code(b'\xef\x00\x01\x01\x00\x01\x02') == False  # Truncated section header
assert validate_code(b'\xef\x00\x01\x03') == False  # Invalid section id
assert validate_code(b'\xef\x00\x01\x01\x00') == False  # Truncated code section size
assert validate_code(b'\xef\x00\x01\x01\x00\x01\x02\x00') == False  # Truncated data section size
assert validate_code(b'\xef\x00\x01\x01\x00\x00\x00') == False  # Empty code section size
assert validate_code(b'\xef\x00\x01\x01\x00\x01\x02\x00\x00\x00\xfe') == False  # Empty data section
assert validate_code(b'\xef\x00\x01\x01\x00\x01') == False  # No terminator after section
assert validate_code(b'\xef\x00\x01\x01\x00\x01\x00') == False  # Missing section contents
assert validate_code(b'\xef\x00\x01\x02\x00\x01\x00\xaa') == False  # Only data section
assert validate_code(b'\xef\x00\x01\x01\x00\x01\x01\x00\x01\x00\xfe\xfe') == False  # Multiple code sections
assert validate_code(b'\xef\x00\x01\x01\x00\x01\x02\x00\x01\x02\x00\x01\x00\xfe\xaa\xbb') == False  # Multiple data sections
assert validate_code(b'\xef\x00\x01\x01\x00\x01\x01\x00\x01\x02\x00\x01\x02\x00\x01\x00\xfe\xfe\xaa\xbb') == False  # Multiple code and data sections
assert validate_code(b'\xef\x00\x01\x02\x00\x01\x01\x00\x01\x00\xaa\xfe') == False  # Data section before code section

assert validate_code(b'\xef\x00\x01\x01\x00\x01\x00\xfe') == True  # Valid format with 1-byte of code
assert validate_code(b'\xef\x00\x01\x01\x00\x01\x02\x00\x01\x00\xfe\xaa') == True  # Code and data section

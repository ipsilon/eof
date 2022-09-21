MAGIC = b'\xEF\x00'
VERSION = 0x01
S_TERMINATOR = 0x00
S_CODE = 0x01
S_DATA = 0x02


# Determines if code is in EOF format of any version.
def is_eof(code: bytes) -> bool:
    return code.startswith(MAGIC)

# Raises AssertionError on invalid code
def validate_eof(code: bytes):
    # Check version
    assert (len(code) > 2 and code[2] == VERSION), "invalid version"

    # Process section headers
    section_sizes = {S_CODE: 0, S_DATA: 0}
    pos = 3
    while True:
        # Terminator not found
        assert (pos < len(code)), "no section terminator"
        
        section_id = code[pos]
        pos += 1
        if section_id == S_TERMINATOR:
            break

        # Disallow unknown sections
        assert (section_id in section_sizes), "invalid section id"

        # Data section preceding code section
        if section_id == S_DATA:
            assert (section_sizes[S_CODE] != 0), "data section preceding code section"

        # Multiple sections with the same id
        assert (section_sizes[section_id] == 0), "multiple sections with same id"

        # Truncated section size
        assert ((pos + 1) < len(code)), "truncated section size"
        section_sizes[section_id] = (code[pos] << 8) | code[pos + 1]
        pos += 2

        # Empty section
        assert  (section_sizes[section_id] != 0), "empty section"

    # Code section cannot be absent
    assert (section_sizes[S_CODE] != 0), "no code section"

    # The entire container must be scanned
    assert (len(code) == (pos + section_sizes[S_CODE] + section_sizes[S_DATA])), "container size not equal to sum of section sizes"


# Validates any code
def is_valid_container(code: bytes) -> bool:
    if is_eof(code):
        try:
            validate_eof(code)
        except:
            return False
    return True

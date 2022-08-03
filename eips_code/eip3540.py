MAGIC = b'\xEF\x00'
VERSION = 0x01
S_TERMINATOR = 0x00
S_CODE = 0x01
S_DATA = 0x02


# Determines if code is in EOF format of any version.
def is_eof(code: bytes) -> bool:
    return code.startswith(MAGIC)

class ValidationException(Exception):
    pass

# Raises ValidationException on invalid code
def validate_eof(code: bytes):
    # Check version
    if len(code) < 3 or code[2] != VERSION:
        raise ValidationException("invalid version")

    # Process section headers
    section_sizes = {S_CODE: 0, S_DATA: 0}
    pos = 3
    while True:
        # Terminator not found
        if pos >= len(code):
            raise ValidationException("no section terminator")            
        
        section_id = code[pos]
        pos += 1
        if section_id == S_TERMINATOR:
            break

        # Disallow unknown sections
        if not section_id in section_sizes:
            raise ValidationException("invalid section id")

        # Data section preceding code section
        if section_id == S_DATA and section_sizes[S_CODE] == 0:
            raise ValidationException("data section preceding code section")

        # Multiple sections with the same id
        if section_sizes[section_id] != 0:
            raise ValidationException("multiple sections with same id")

        # Truncated section size
        if (pos + 1) >= len(code):
            raise ValidationException("truncated section size")
        section_sizes[section_id] = (code[pos] << 8) | code[pos + 1]
        pos += 2

        # Empty section
        if section_sizes[section_id] == 0:
            raise ValidationException("empty section")

    # Code section cannot be absent
    if section_sizes[S_CODE] == 0:
        raise ValidationException("no code section")

    # The entire container must be scanned
    if len(code) != (pos + section_sizes[S_CODE] + section_sizes[S_DATA]):
        raise ValidationException("container size not equal to sum of section sizes")


# Validates any code
def is_valid_container(code: bytes) -> bool:
    if is_eof(code):
        try:
            validate_eof(code)
        except:
            return False
    return True

# The ranges below are as specified in the Yellow Paper.
# Note: range(s, e) excludes e, hence the +1
valid_opcodes = [
    *range(0x00, 0x0b + 1),
    *range(0x10, 0x1d + 1),
    0x20,
    *range(0x30, 0x3f + 1),
    *range(0x40, 0x48 + 1),
    *range(0x50, 0x5d + 1),
    *range(0x60, 0x6f + 1),
    *range(0x70, 0x7f + 1),
    *range(0x80, 0x8f + 1),
    *range(0x90, 0x9f + 1),
    *range(0xa0, 0xa4 + 1),
    # Note: 0xfe is considered assigned.
    *range(0xf0, 0xf5 + 1), *range(0xfa, 0xff + 1),
]

# STOP, RETURN, RETF, REVERT, INVALID, SELFDESTRUCT
terminating_opcodes = [ 0x00, 0xf3, 0xfc, 0xfd, 0xfe, 0xff ]

immediate_sizes = 256 * [0]
immediate_sizes[0x5c] = 2  # RJUMP
immediate_sizes[0x5d] = 2  # RJUMPI
immediate_sizes[0xfb] = 2  # CALLF
for opcode in range(0x60, 0x7f + 1):  # PUSH1..PUSH32
    immediate_sizes[opcode] = opcode - 0x60 + 1

class ValidationException(Exception):
    pass

# Raises ValidationException on invalid code
def validate_code_section(code: bytes, num_code_sections: int):
    # Note that EOF1 already asserts this with the code section requirements
    assert len(code) > 0

    opcode = 0
    pos = 0
    rjumpdests = set()
    immediates = set()
    while pos < len(code):
        # Ensure the opcode is valid
        opcode = code[pos]
        pos += 1
        if not opcode in valid_opcodes:
            raise ValidationException("undefined instruction")

        if opcode == 0x5c or opcode == 0x5d:
            if pos + 2 > len(code):
                raise ValidationException("truncated relative jump offset")
            offset = int.from_bytes(code[pos:pos+2], byteorder = "big", signed = True)

            rjumpdest = pos + 2 + offset
            if rjumpdest < 0 or rjumpdest >= len(code):
                raise ValidationException("relative jump destination out of bounds")

            rjumpdests.add(rjumpdest)
        elif opcode == 0xfb:
            if pos + 2 > len(code):
                raise ValidationException("truncated CALLF immediate")
            section_id = int.from_bytes(code[pos:pos+2], byteorder = "big", signed = False)

            if section_id >= num_code_sections:
                raise ValidationException("invalid section id")

        # Save immediate value positions
        immediates.update(range(pos, pos + immediate_sizes[opcode]))
        # Skip immediates
        pos += immediate_sizes[opcode]

    # Ensure last opcode's immediate doesn't go over code end
    if pos != len(code):        
        raise ValidationException("truncated immediate")

    # opcode is the *last opcode*
    if not opcode in terminating_opcodes:
        raise ValidationException("no terminating instruction")

    # Ensure relative jump destinations don't target immediates
    if not rjumpdests.isdisjoint(immediates):
        raise ValidationException("relative jump destination targets immediate")


def is_valid_code(code: bytes, num_code_sections: int = 1) -> bool:
    try:
        validate_code_section(code, num_code_sections)
        return True
    except:
        return False

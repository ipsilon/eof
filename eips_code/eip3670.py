from eip3540 import ValidationException

# The ranges below are as specified in the Yellow Paper.
# Note: range(s, e) excludes e, hence the +1
valid_opcodes = [
    *range(0x00, 0x0b + 1),
    *range(0x10, 0x1d + 1),
    0x20,
    *range(0x30, 0x3f + 1),
    *range(0x40, 0x48 + 1),
    *range(0x50, 0x5b + 1),
    *range(0x60, 0x6f + 1),
    *range(0x70, 0x7f + 1),
    *range(0x80, 0x8f + 1),
    *range(0x90, 0x9f + 1),
    *range(0xa0, 0xa4 + 1),
    # Note: 0xfe is considered assigned.
    0xf0, 0xf1, 0xf3, 0xf4, 0xf5, 0xfa, 0xfd, 0xfe
]

# STOP, RETURN, REVERT, INVALID
terminating_opcodes = [0x00, 0xf3, 0xfd, 0xfe]

# Only for PUSH1..PUSH32
immediate_sizes = 256 * [0]
for opcode in range(0x60, 0x7f + 1):  # PUSH1..PUSH32
    immediate_sizes[opcode] = opcode - 0x60 + 1

# Raises ValidationException on invalid code
def validate_code(code: bytes):
    # Note that EOF1 already asserts this with the code section requirements
    assert len(code) > 0

    opcode = 0
    pos = 0
    while pos < len(code):
        # Ensure the opcode is valid
        opcode = code[pos]
        pos += 1
        if not opcode in valid_opcodes:
            raise ValidationException("undefined instruction")

        # Skip immediates
        pos += immediate_sizes[opcode]

    # Ensure last opcode's immediate doesn't go over code end
    if pos != len(code):
        raise ValidationException("truncated immediate")

    # opcode is the *last opcode*
    if not opcode in terminating_opcodes:
        raise ValidationException("no terminating instruction")


def is_valid_code(code: bytes) -> bool:
    try:
        validate_code(code)
        return True
    except:
        return False

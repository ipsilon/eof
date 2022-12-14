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

immediate_sizes = 256 * [0]
immediate_sizes[0x60:0x7f + 1] = range(1, 32 + 1)  # PUSH1..PUSH32


# Raises ValidationException on invalid code
def validate_instructions(code: bytes):
    # Note that EOF1 already asserts this with the code section requirements
    assert len(code) > 0

    pos = 0
    while pos < len(code):
        # Ensure the opcode is valid
        opcode = code[pos]
        if opcode not in valid_opcodes:
            raise ValidationException("undefined instruction")

        # Skip immediate data
        pos += 1 + immediate_sizes[opcode]

    # Ensure last instruction's immediate doesn't go over code end
    if pos != len(code):
        raise ValidationException("truncated immediate")


def is_valid_code(code: bytes) -> bool:
    try:
        validate_instructions(code)
        return True
    except ValidationException:
        return False

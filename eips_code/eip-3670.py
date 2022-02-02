from code_validation_tests import test_code_validation

# The below are ranges as specified in the Yellow Paper.
# Note: range(s, e) excludes e, hence the +1
valid_opcodes = [
    *range(0x00, 0x0b + 1),
    *range(0x10, 0x1d + 1),
    0x20,
    *range(0x30, 0x3f + 1),
    *range(0x40, 0x47 + 1),
    *range(0x50, 0x5b + 1),
    *range(0x60, 0x6f + 1),
    *range(0x70, 0x7f + 1),
    *range(0x80, 0x8f + 1),
    *range(0x90, 0x9f + 1),
    *range(0xa0, 0xa4 + 1),
    # Note: 0xfe is considered assigned.
    *range(0xf0, 0xf5 + 1), 0xfa, 0xfd, 0xfe, 0xff
]
# STOP, RETURN, REVERT, INVALID
terminating_opcodes = [ 0x00, 0xf3, 0xfd, 0xfe ]

immediate_sizes = []
for opcode in range(0x100):
    # PUSH1..PUSH32
    if opcode >= 0x60 and opcode <= 0x7f:
        immediate_sizes.append(opcode - 0x60 + 1)
    else:
        immediate_sizes.append(0)


# Fails with assertion on invalid code
def validate_code(code: bytes):
    # Note that EOF1 already asserts this with the code section requirements
    assert(len(code) > 0)

    opcode = 0
    pos = 0
    while pos < len(code):
        # Ensure the opcode is valid
        opcode = code[pos]
        pos += 1
        assert(opcode in valid_opcodes)

        # Skip immediates
        pos += immediate_sizes[opcode]

    # Ensure last opcode's immediate doesn't go over code end
    assert(pos == len(code))

    # opcode is the *last opcode*
    assert(opcode in terminating_opcodes)

test_code_validation(validate_code)

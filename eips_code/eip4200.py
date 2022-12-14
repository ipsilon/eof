from eip3540 import ValidationException
import eip3670

OP_RJUMP = 0x5c
OP_RJUMPI = 0x5d
OP_RJUMPV = 0x5e

valid_opcodes = eip3670.valid_opcodes.copy() + [OP_RJUMP, OP_RJUMPI, OP_RJUMPV]

# STOP, RETURN, REVERT, INVALID
terminating_opcodes = [0x00, 0xf3, 0xfd, 0xfe]

immediate_sizes = eip3670.immediate_sizes.copy()
immediate_sizes[OP_RJUMP] = 2
immediate_sizes[OP_RJUMPI] = 2


# Raises ValidationException on invalid code
def validate_code(code: bytes):
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

        pc_post_instruction = pos + immediate_sizes[opcode]

        if opcode in (OP_RJUMP, OP_RJUMPI):
            if pos + 2 > len(code):
                raise ValidationException("truncated relative jump offset")
            offset = int.from_bytes(code[pos:pos + 2], byteorder="big", signed=True)

            rjumpdest = pc_post_instruction + offset
            if rjumpdest < 0 or rjumpdest >= len(code):
                raise ValidationException("relative jump destination out of bounds")

            rjumpdests.add(rjumpdest)
        elif opcode == OP_RJUMPV:
            if pos + 1 > len(code):
                raise ValidationException("truncated jump table")
            jump_table_size = code[pos]
            if jump_table_size == 0:
                raise ValidationException("empty jump table")

            pc_post_instruction = pos + 1 + 2 * jump_table_size
            if pc_post_instruction > len(code):
                raise ValidationException("truncated jump table")

            for offset_pos in range(pos + 1, pc_post_instruction, 2):
                offset = int.from_bytes(code[offset_pos:offset_pos + 2], byteorder="big", signed=True)

                rjumpdest = pc_post_instruction + offset
                if rjumpdest < 0 or rjumpdest >= len(code):
                    raise ValidationException("relative jump destination out of bounds")
                rjumpdests.add(rjumpdest)

        # Save immediate value positions
        immediates.update(range(pos, pc_post_instruction))
        # Skip immediates
        pos = pc_post_instruction

    # Ensure last opcode's immediate doesn't go over code end
    if pos != len(code):
        raise ValidationException("truncated immediate")

    # opcode is the *last opcode*
    if not opcode in terminating_opcodes:
        raise ValidationException("no terminating instruction")

    # Ensure relative jump destinations don't target immediates
    if not rjumpdests.isdisjoint(immediates):
        raise ValidationException("relative jump destination targets immediate")


def is_valid_code(code: bytes) -> bool:
    try:
        validate_code(code)
        return True
    except:
        return False

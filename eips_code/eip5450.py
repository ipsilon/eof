from dataclasses import dataclass
from eip3540 import ValidationException
from eip4750 import validate_code_section, valid_opcodes
from eip5450_table import TABLE, OP_RJUMP, OP_RJUMPI, OP_CALLF, OP_RETF


@dataclass
class FunctionType:
    inputs: int
    outputs: int

def validate_function(func_id: int, code: bytes, types: list[FunctionType] = [FunctionType(0, 0)]) -> int:
    assert func_id >= 0
    assert types[func_id].inputs >= 0
    assert types[func_id].outputs >= 0

    try:
        validate_code_section(code, len(types))
    except ValidationException as e:
        if str(e) != "no terminating instruction":
            raise e

    stack_heights = {}
    start_stack_height = types[func_id].inputs
    max_stack_height = start_stack_height

    # queue of instructions to analyze, list of (pos, stack_height) pairs
    worklist = [(0, start_stack_height)]

    while worklist:
        pos, stack_height = worklist.pop(0)
        while True:
            op = code[pos]
            info = TABLE[op]

            # Check if stack height (type arity) at given position is the same
            # for all control flow paths reaching this position.
            if pos in stack_heights:
                if stack_height != stack_heights[pos]:
                    raise ValidationException("stack height mismatch for different paths")
                else:
                    break
            else:
                stack_heights[pos] = stack_height

            stack_height_required = info.stack_height_required
            stack_height_change = info.stack_height_change

            if op == OP_CALLF:
                called_func_id = int.from_bytes(code[pos + 1:pos + 3], byteorder="big", signed=False)
                # Assuming called_func_id is valid due to previous validation in validate_code_section()
                stack_height_required += types[called_func_id].inputs
                stack_height_change += types[called_func_id].outputs - types[called_func_id].inputs

            # Detect stack underflow
            if stack_height < stack_height_required:
                raise ValidationException("stack underflow")

            stack_height += stack_height_change
            max_stack_height = max(max_stack_height, stack_height)

            # Handle jumps
            if op == OP_RJUMP:
                offset = int.from_bytes(code[pos + 1:pos + 3], byteorder="big", signed=True)
                pos += info.immediate_size + 1 + offset  # pos is valid for validated code.

            elif op == OP_RJUMPI:
                offset = int.from_bytes(code[pos + 1:pos + 3], byteorder="big", signed=True)
                # Save True branch for later and continue to False branch.
                worklist.append((pos + 3 + offset, stack_height))
                pos += info.immediate_size + 1

            elif info.is_terminating:
                expected_height = types[func_id].outputs if op == OP_RETF else 0
                if stack_height != expected_height:
                    raise ValidationException("non-empty stack on terminating instruction")
                break

            else:
                pos += info.immediate_size + 1

            if pos >= len(code):
                raise ValidationException("no terminating instruction")

    if max_stack_height >= 1023:
        raise ValidationException("max stack above limit")

    return max_stack_height


@dataclass
class InstrInfo:
    changed: bool
    stack_height: int


def validate_function_jvm(func_id: int, code: bytes, types: list[FunctionType] = [FunctionType(0, 0)]) -> int:
    # Collect instruction offsets.
    instr_offsets = []
    i = 0
    while i < len(code):
        instr_offsets.append(i)
        opcode = code[i]
        if opcode not in valid_opcodes:
            raise ValidationException("undefined instruction")
        i += TABLE[opcode].immediate_size + 1

    # Validate immediate data
    for offset in instr_offsets:
        opcode = code[offset]

        imm_len = TABLE[opcode].immediate_size
        if offset + imm_len > len(code):
            raise ValidationException("incomplete instruction")

        if opcode in (OP_RJUMP, OP_RJUMPI):
            target_offset = int.from_bytes(code[offset + 1:offset + 3], byteorder="big", signed=True)
            target = offset + target_offset + 3
            if target not in instr_offsets:
                raise ValidationException("invalid jump target")

        if opcode == OP_CALLF:
            fid = int.from_bytes(code[offset + 1:offset + 3], byteorder="big")
            if fid >= len(types):
                raise ValidationException("invalid section id")

    # Dataflow analysis
    analysis = []
    for i in range(len(code)):
        analysis.append(InstrInfo(False, -1))
    analysis[0] = InstrInfo(True, types[func_id].inputs)
    while True:
        i = -1
        a = None
        for ii, aa in enumerate(analysis):
            if aa.changed:
                i = ii
                a = aa
                aa.changed = False
                break
        if i == -1:
            break

        opcode = code[i]
        stack_height_required = TABLE[opcode].stack_height_required
        stack_height_change = TABLE[opcode].stack_height_change
        if opcode == OP_CALLF:
            fid = int.from_bytes(code[i + 1:i + 3], byteorder="big", signed=True)
            stack_height_required = types[fid].inputs
            stack_height_change = types[fid].outputs - stack_height_required

        if a.stack_height < stack_height_required:
            raise ValidationException("stack underflow")

        successors = []
        if opcode != OP_RJUMP and not TABLE[opcode].is_terminating:
            next = i + TABLE[opcode].immediate_size + 1
            if next >= len(code):
                raise ValidationException("no terminating instruction")
            successors.append(next)

        if opcode in (OP_RJUMP, OP_RJUMPI):
            target_offset = int.from_bytes(code[i + 1:i + 3], byteorder="big", signed=True)
            target = i + target_offset + 3
            successors.append(target)

        stack_height = a.stack_height + stack_height_change

        for s in successors:
            sa = analysis[s]
            if sa.stack_height == -1:  # visited first time
                sa.stack_height = stack_height
                sa.changed = True
            else:
                if sa.stack_height != stack_height:
                    raise ValidationException("stack height mismatch for different paths")

        if opcode == OP_RETF and stack_height != types[func_id].outputs:
            raise ValidationException("non-empty stack on terminating instruction")
        if opcode != OP_RETF and TABLE[opcode].is_terminating and stack_height != 0:
            raise ValidationException("non-empty stack on terminating instruction")

    max_stack_height = -1
    for a in analysis:
        max_stack_height = max(max_stack_height, a.stack_height)
    if max_stack_height >= 1023:
        raise ValidationException("max stack above limit")
    return max_stack_height

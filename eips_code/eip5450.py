from dataclasses import dataclass
from eip5450_table import TABLE, OP_RJUMP, OP_RJUMPI, OP_CALLF, OP_RETF
from eip4750 import validate_code_section, immediate_sizes

@dataclass
class FunctionType:
    inputs: int
    outputs: int


def validate_function(func_id: int, code: bytes, types: list[FunctionType] = [FunctionType(0, 0)]) -> int:
    assert func_id >= 0
    assert types[func_id].inputs >= 0
    assert types[func_id].outputs >= 0

    validate_code_section(code, len(types))

    stack_heights = {}
    start_stack_height = types[func_id].inputs
    max_stack_height = start_stack_height

    # queue of instructions to analyze, list of (pos, stack_height) pairs
    worklist = [(0, start_stack_height)]

    while worklist:
        pos, stack_height = worklist.pop(0)
        while True:
            # Assuming code ends with a terminating instruction due to previous validation in validate_code_section()
            assert pos < len(code), "code is invalid" 
            op = code[pos]
            info = TABLE[op]

            # Check if stack height (type arity) at given position is the same
            # for all control flow paths reaching this position.
            if pos in stack_heights:
                if stack_height != stack_heights[pos]:
                    return -102
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
                return -101

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
                    return -103
                break

            else:
                pos += info.immediate_size + 1


    if max_stack_height >= 1023:
        return -105

    return max_stack_height

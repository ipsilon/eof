from eip5450 import validate_function, validate_function_jvm, FunctionType, ValidationException, validate_function_2pass, validate_function_1pass
from eip5450_table import *
import pytest


def _validate_function(func_id: int, code: bytes, types: list[FunctionType] = [FunctionType(0, 0)]) -> int:
    ea = None
    eb = None
    try:
        a = validate_function(func_id, code, types)
    except Exception as e:
        assert type(e) is ValidationException
        ea = e
    try:
        b = validate_function_jvm(func_id, code, types)
    except Exception as e:
        assert type(e) is ValidationException
        eb = e

    if ea is not None:
        assert str(eb) == str(ea)
        raise ea
    elif eb is not None:
        assert str(eb) == str(ea)

    assert a == b
    return a


def test_empty():
    assert _validate_function(0, bytes((OP_STOP,))) == 0


def test_stack_empty_at_exit():
    with pytest.raises(ValidationException, match="non-empty stack on terminating instruction"):
        _validate_function(0, bytes((OP_NUMBER, OP_STOP)))
    assert _validate_function(0, bytes((OP_NUMBER, OP_POP, OP_STOP))) == 1
    assert _validate_function(1, bytes((OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(1, 0)]) == 1
    with pytest.raises(ValidationException, match="non-empty stack on terminating instruction"):
        _validate_function(1, bytes((OP_STOP,)), [FunctionType(0, 0), FunctionType(1, 0)])


def test_immediate_bytes():
    assert _validate_function(0, bytes((OP_PUSH1, 0x01, OP_POP, OP_STOP))) == 1


def test_stack_underflow():
    with pytest.raises(ValidationException, match="stack underflow"):
        _validate_function(0, bytes((OP_POP, OP_STOP)))


def test_jump_forward():
    assert _validate_function(0, bytes((OP_RJUMP, 0x00, 0x00, OP_STOP))) == 0
    assert _validate_function(0, bytes((OP_RJUMP, 0x00, 0x01, OP_NUMBER, OP_STOP))) == 0
    assert _validate_function(0, bytes((OP_RJUMP, 0x00, 0x02, OP_NUMBER, OP_POP, OP_STOP))) == 0
    assert _validate_function(0, bytes((OP_RJUMP, 0x00, 0x03, OP_ADD, OP_POP, OP_STOP, OP_PUSH1, 0x01, OP_PUSH1, 0x01, OP_RJUMP, 0xff, 0xf6, OP_STOP))) == 2


def test_jump_backwards():
    assert _validate_function(0, bytes((OP_RJUMP, 0xff, 0xfd, OP_STOP))) == 0
    assert _validate_function(0, bytes((OP_JUMPDEST, OP_RJUMP, 0xff, 0xfc, OP_STOP))) == 0
    with pytest.raises(ValidationException, match="stack height mismatch for different paths"):
        _validate_function(0, bytes((OP_NUMBER, OP_RJUMP, 0xff, 0xfc, OP_POP, OP_STOP)))
    with pytest.raises(ValidationException, match="stack height mismatch for different paths"):
        _validate_function(0, bytes((OP_NUMBER, OP_POP, OP_RJUMP, 0xff, 0xfc, OP_STOP)))
    assert _validate_function(0, bytes((OP_NUMBER, OP_POP, OP_RJUMP, 0xff, 0xfd, OP_STOP))) == 1
    assert _validate_function(0, bytes((OP_NUMBER, OP_POP, OP_JUMPDEST, OP_RJUMP, 0xff, 0xfc, OP_STOP))) == 1
    assert _validate_function(0, bytes((OP_NUMBER, OP_POP, OP_NUMBER, OP_RJUMP, 0xff, 0xfb, OP_POP, OP_STOP))) == 1
    with pytest.raises(ValidationException, match="stack height mismatch for different paths"):
        _validate_function(0, bytes((OP_NUMBER, OP_POP, OP_NUMBER, OP_RJUMP, 0xff, 0xfc, OP_POP, OP_STOP)))


def test_conditional_jump():
    # Each branch ending with STOP
    assert _validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x02, OP_POP, OP_STOP, OP_POP, OP_STOP))) == 2
    # One branch ending with RJUMP
    assert _validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x04, OP_POP, OP_RJUMP, 0x00, 0x01, OP_POP, OP_STOP))) == 2
    # Fallthrough
    assert _validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x04, OP_DUP1, OP_DUP1, OP_POP, OP_POP, OP_POP, OP_STOP))) == 3
    # Offset 0
    assert _validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x00, OP_POP, OP_STOP))) == 2
    # Simple loop (RJUMP offset = -5)
    assert _validate_function(0, bytes((OP_PUSH1, 0x01, OP_PUSH1, 0xff, OP_DUP2, OP_SUB, OP_DUP1, OP_RJUMPI, 0xff, 0xfa, OP_POP, OP_POP, OP_STOP))) == 3
    # One branch increasing max stack more stack than another
    assert _validate_function(0, bytes((OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x07, OP_ADDRESS, OP_ADDRESS, OP_ADDRESS, OP_POP, OP_POP, OP_POP, OP_STOP, OP_ADDRESS, OP_POP, OP_STOP))) == 3
    assert _validate_function(0, bytes((OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x03, OP_ADDRESS, OP_POP, OP_STOP, OP_ADDRESS, OP_ADDRESS, OP_ADDRESS, OP_POP, OP_POP, OP_POP, OP_STOP))) == 3

    # Missing stack argument
    with pytest.raises(ValidationException, match="stack underflow"):
        _validate_function(0, bytes((OP_RJUMPI, 0x00, 0x00, OP_STOP)))
    # Stack underflow in one branch
    with pytest.raises(ValidationException, match="stack underflow"):
        _validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x02, OP_POP, OP_STOP, OP_SUB, OP_POP, OP_STOP)))
    with pytest.raises(ValidationException, match="stack underflow"):
        _validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x02, OP_SUB, OP_STOP, OP_NOT, OP_POP, OP_STOP)))
    # Stack not empty in the end of one branch
    with pytest.raises(ValidationException, match="non-empty stack on terminating instruction"):
        _validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x02, OP_POP, OP_STOP, OP_NOT, OP_STOP)))
    with pytest.raises(ValidationException, match="non-empty stack on terminating instruction"):
        _validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x02, OP_NOT, OP_STOP, OP_POP, OP_STOP)))


def test_callf():
    # 0 inputs, 0 outpus
    assert _validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(0, 0), FunctionType(0, 0)]) == 0
    assert _validate_function(0, bytes((OP_CALLF, 0x00, 0x02, OP_STOP)), [FunctionType(0, 0), FunctionType(1, 1), FunctionType(0, 0)]) == 0

    # more than 0 inputs
    assert _validate_function(0, bytes((OP_ADDRESS, OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(0, 0), FunctionType(1, 0)]) == 1
    # forwarding an argument
    assert _validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(1, 0), FunctionType(1, 0)]) == 1

    # more than 1 inputs
    assert _validate_function(0, bytes((OP_ADDRESS, OP_DUP1, OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(0, 0), FunctionType(2, 0)]) == 2

    # more than 0 outputs
    assert _validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(0, 1)]) == 1
    assert _validate_function(0, bytes((OP_CALLF, 0x00, 0x02, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(0, 0), FunctionType(0, 1)]) == 1

    # more than 1 outputs
    assert _validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_POP, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(0, 2)]) == 2

    # more than 0 inputs, more than 0 outputs
    assert _validate_function(0, bytes((OP_ADDRESS, OP_ADDRESS, OP_CALLF, 0x00, 0x01, OP_POP, OP_POP, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(2, 3)]) == 3

    # recursion
    assert _validate_function(0, bytes((OP_CALLF, 0x00, 0x00, OP_STOP)), [FunctionType(0, 0)]) == 0
    assert _validate_function(0, bytes((OP_CALLF, 0x00, 0x00, OP_STOP)), [FunctionType(2, 0)]) == 2
    assert _validate_function(0, bytes((OP_CALLF, 0x00, 0x00, OP_POP, OP_POP, OP_STOP)), [FunctionType(2, 2)]) == 2
    assert _validate_function(1, bytes((OP_ADDRESS, OP_ADDRESS, OP_CALLF, 0x00, 0x01, OP_POP, OP_POP, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(2, 1)]) == 4

    # multiple CALLFs with different types
    assert _validate_function(0, bytes((OP_PREVRANDAO, OP_CALLF, 0x00, 0x01, OP_DUP1, OP_DUP1, OP_CALLF, 0x00, 0x02,
                                        OP_PREVRANDAO, OP_DUP1, OP_CALLF, 0x00, 0x03, OP_POP, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(1, 1), FunctionType(3, 0), FunctionType(2, 2)]) == 3

    # underflow
    with pytest.raises(ValidationException, match="stack underflow"):
        _validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(0, 0), FunctionType(1, 0)])
    with pytest.raises(ValidationException, match="stack underflow"):
        _validate_function(0, bytes((OP_ADDRESS, OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(0, 0), FunctionType(2, 0)])
    with pytest.raises(ValidationException, match="stack underflow"):
        _validate_function(0, bytes((OP_POP, OP_CALLF, 0x00, 0x00, OP_STOP)), [FunctionType(1, 0)])
    with pytest.raises(ValidationException, match="stack underflow"):
        _validate_function(0, bytes((OP_PREVRANDAO, OP_CALLF, 0x00, 0x01, OP_DUP1, OP_CALLF, 0x00, 0x02, OP_STOP)),
                           [FunctionType(0, 0), FunctionType(1, 1), FunctionType(3, 0)])


def test_retf():
    # 0 outpus
    assert _validate_function(0, bytes((OP_RETF,)), [FunctionType(0, 0), FunctionType(0, 0)]) == 0
    assert _validate_function(1, bytes((OP_RETF,)), [FunctionType(0, 0), FunctionType(0, 0)]) == 0
    assert _validate_function(2, bytes((OP_RETF,)), [FunctionType(0, 0), FunctionType(1, 1), FunctionType(0, 0)]) == 0

    # more than 0 outputs
    assert _validate_function(0, bytes((OP_PREVRANDAO, OP_RETF)), [FunctionType(0, 1), FunctionType(0, 1)]) == 1
    assert _validate_function(1, bytes((OP_PREVRANDAO, OP_RETF)), [FunctionType(0, 1), FunctionType(0, 1)]) == 1

    # more than 1 outputs
    assert _validate_function(1, bytes((OP_PREVRANDAO, OP_DUP1, OP_RETF)), [FunctionType(0, 0), FunctionType(0, 2)]) == 2

    # forwarding return value
    assert _validate_function(0, bytes((OP_RETF,)), [FunctionType(1, 1)]) == 1
    assert _validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_RETF)), [FunctionType(0, 1), FunctionType(0, 1)]) == 1

    # multiple RETFs
    assert _validate_function(0, bytes((OP_RJUMPI, 0x00, 0x03, OP_PREVRANDAO, OP_DUP1, OP_RETF, OP_ADDRESS, OP_DUP1, OP_RETF)), [FunctionType(1, 2)]) == 2

    # underflow
    with pytest.raises(ValidationException, match="non-empty stack on terminating instruction"):
        _validate_function(0, bytes((OP_RETF,)), [FunctionType(0, 1), FunctionType(0, 1)])
    with pytest.raises(ValidationException, match="non-empty stack on terminating instruction"):
        _validate_function(1, bytes((OP_RETF,)), [FunctionType(0, 1), FunctionType(0, 1)])
    with pytest.raises(ValidationException, match="non-empty stack on terminating instruction"):
        _validate_function(0, bytes((OP_RETF,)), [FunctionType(0, 1)])
    with pytest.raises(ValidationException, match="non-empty stack on terminating instruction"):
        _validate_function(1, bytes((OP_PREVRANDAO, OP_RETF)), [FunctionType(0, 0), FunctionType(0, 2)])
    with pytest.raises(ValidationException, match="non-empty stack on terminating instruction"):
        _validate_function(0, bytes((OP_RJUMPI, 0x00, 0x03, OP_PREVRANDAO, OP_DUP1, OP_RETF, OP_ADDRESS, OP_RETF)), [FunctionType(1, 2)])


def test_unreachable():
    # Max stack not changed by unreachable code
    assert _validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_STOP, OP_ADDRESS, OP_ADDRESS, OP_ADDRESS, OP_POP, OP_POP, OP_POP, OP_STOP))) == 1
    assert _validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_RETF, OP_ADDRESS, OP_ADDRESS, OP_ADDRESS, OP_POP, OP_POP, OP_POP, OP_STOP))) == 1
    assert _validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_RJUMP, 0x00, 0x06, OP_ADDRESS, OP_ADDRESS, OP_ADDRESS, OP_POP, OP_POP, OP_POP, OP_STOP))) == 1
    # Stack underflow in unreachable code
    assert _validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_STOP, OP_POP, OP_STOP))) == 1
    assert _validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_RETF, OP_POP, OP_STOP))) == 1
    assert _validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_RJUMP, 0x00, 0x01, OP_POP, OP_STOP))) == 1


def test_stack_overflow():
    assert _validate_function(0, bytes([OP_NUMBER] * 1022 + [OP_POP] * 1022 + [OP_STOP])) == 1022
    with pytest.raises(ValidationException, match="max stack above limit"):
        _validate_function(0, bytes([OP_NUMBER] * 1023 + [OP_POP] * 1023 + [OP_STOP]))


def _validate_1pass(code: bytes) -> int:
    a = -1
    try:
        a = validate_function_2pass(0, code)
    except ValidationException:
        pass

    b = -1
    try:
        b = validate_function_1pass(0, code)
    except ValidationException:
        pass

    assert b == a, "validation mismatch"
    return a


def test_1pass():
    assert _validate_1pass(bytes.fromhex("5cfffd")) == 0
    assert _validate_1pass(bytes.fromhex("5c0001")) == -1
    assert _validate_1pass(bytes.fromhex("605b00")) == 1
    assert _validate_1pass(bytes.fromhex("fb0100")) == -1
    assert _validate_1pass(bytes.fromhex("fc78")) == -1
    assert _validate_1pass(bytes.fromhex("59fc")) == -1
    assert _validate_1pass(bytes.fromhex("5900")) == 1
    assert _validate_1pass(bytes.fromhex("38")) == -1
    assert _validate_1pass(bytes.fromhex("5b00")) == 0


    assert _validate_1pass(bytes.fromhex("50")) == -1
    assert _validate_1pass(bytes.fromhex("00")) == 0
    assert _validate_1pass(bytes.fromhex("fb")) == -1

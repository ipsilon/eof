from eip5450 import validate_function, FunctionType
from eip5450_table import *


def test_empty():
    assert validate_function(0, bytes((OP_STOP,))) == 0


def test_stack_empty_at_exit():
    assert validate_function(0, bytes((OP_NUMBER, OP_STOP))) == -103
    assert validate_function(0, bytes((OP_NUMBER, OP_POP, OP_STOP))) == 1
    assert validate_function(1, bytes((OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(1, 0)]) == 1
    assert validate_function(1, bytes((OP_STOP,)), [FunctionType(0, 0), FunctionType(1, 0)]) == -103


def test_immediate_bytes():
    assert validate_function(0, bytes((OP_PUSH1, 0x01, OP_POP, OP_STOP))) == 1


def test_stack_underflow():
    assert validate_function(0, bytes((OP_POP, OP_STOP))) == -101


def test_jump_forward():
    assert validate_function(0, bytes((OP_RJUMP, 0x00, 0x00, OP_STOP))) == 0
    assert validate_function(0, bytes((OP_RJUMP, 0x00, 0x01, OP_NUMBER, OP_STOP))) == 0
    assert validate_function(0, bytes((OP_RJUMP, 0x00, 0x02, OP_NUMBER, OP_POP, OP_STOP))) == 0
    assert validate_function(0, bytes((OP_RJUMP, 0x00, 0x03, OP_ADD, OP_POP, OP_STOP, OP_PUSH1, 0x01, OP_PUSH1, 0x01, OP_RJUMP, 0xff, 0xf6, OP_STOP))) == 2


def test_jump_backwards():
    assert validate_function(0, bytes((OP_RJUMP, 0xff, 0xfd, OP_STOP))) == 0
    assert validate_function(0, bytes((OP_JUMPDEST, OP_RJUMP, 0xff, 0xfc, OP_STOP))) == 0
    assert validate_function(0, bytes((OP_NUMBER, OP_RJUMP, 0xff, 0xfc, OP_POP, OP_STOP))) == -102
    assert validate_function(0, bytes((OP_NUMBER, OP_POP, OP_RJUMP, 0xff, 0xfc, OP_STOP))) == -102
    assert validate_function(0, bytes((OP_NUMBER, OP_POP, OP_RJUMP, 0xff, 0xfd, OP_STOP))) == 1
    assert validate_function(0, bytes((OP_NUMBER, OP_POP, OP_JUMPDEST, OP_RJUMP, 0xff, 0xfc, OP_STOP))) == 1
    assert validate_function(0, bytes((OP_NUMBER, OP_POP, OP_NUMBER, OP_RJUMP, 0xff, 0xfb, OP_POP, OP_STOP))) == 1
    assert validate_function(0, bytes((OP_NUMBER, OP_POP, OP_NUMBER, OP_RJUMP, 0xff, 0xfc, OP_POP, OP_STOP))) == -102

def test_conditional_jump():
    # Each branch ending with STOP
    assert validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x02, OP_POP, OP_STOP, OP_POP, OP_STOP))) == 2
    # One branch ending with RJUMP
    assert validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x04, OP_POP, OP_RJUMP, 0x00, 0x01, OP_POP, OP_STOP))) == 2
    # Fallthrough
    assert validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x04, OP_DUP1, OP_DUP1, OP_POP, OP_POP, OP_POP, OP_STOP))) == 3
    # Offset 0
    assert validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x00, OP_POP, OP_STOP))) == 2    
    # Simple loop (RJUMP offset = -5)
    assert validate_function(0, bytes((OP_PUSH1, 0x01, OP_PUSH1, 0xff, OP_DUP2, OP_SUB, OP_DUP1, OP_RJUMPI, 0xff, 0xfa, OP_POP, OP_POP, OP_STOP))) == 3
    # One branch increasing max stack more stack than another
    assert validate_function(0, bytes((OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x07, OP_ADDRESS, OP_ADDRESS, OP_ADDRESS, OP_POP, OP_POP, OP_POP, OP_STOP, OP_ADDRESS, OP_POP, OP_STOP))) == 3
    assert validate_function(0, bytes((OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x03, OP_ADDRESS, OP_POP, OP_STOP, OP_ADDRESS, OP_ADDRESS, OP_ADDRESS, OP_POP, OP_POP, OP_POP, OP_STOP))) == 3

    # Missing stack argument
    assert validate_function(0, bytes((OP_RJUMPI, 0x00, 0x00, OP_STOP))) == -101
    # Stack underflow in one branch
    assert validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x02, OP_POP, OP_STOP, OP_SUB, OP_POP, OP_STOP))) == -101
    assert validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x02, OP_SUB, OP_STOP, OP_NOT, OP_POP, OP_STOP))) == -101
    # Stack not empty in the end of one branch
    assert validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x02, OP_POP, OP_STOP, OP_NOT, OP_STOP))) == -103
    assert validate_function(0, bytes((OP_PUSH1, 0xff, OP_PUSH1, 0x01, OP_RJUMPI, 0x00, 0x02, OP_NOT, OP_STOP, OP_POP, OP_STOP))) == -103

def test_callf():
    # 0 inputs, 0 outpus
    assert validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(0, 0), FunctionType(0, 0)]) == 0
    assert validate_function(0, bytes((OP_CALLF, 0x00, 0x02, OP_STOP)), [FunctionType(0, 0), FunctionType(1, 1), FunctionType(0, 0)]) == 0

    # more than 0 inputs
    assert validate_function(0, bytes((OP_ADDRESS, OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(0, 0), FunctionType(1, 0)]) == 1
    # forwarding an argument
    assert validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(1, 0), FunctionType(1, 0)]) == 1
    
    # more than 1 inputs
    assert validate_function(0, bytes((OP_ADDRESS, OP_DUP1, OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(0, 0), FunctionType(2, 0)]) == 2
    
    # more than 0 outputs
    assert validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(0, 1)]) == 1
    assert validate_function(0, bytes((OP_CALLF, 0x00, 0x02, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(0, 0), FunctionType(0, 1)]) == 1

    # more than 1 outputs
    assert validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_POP, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(0, 2)]) == 2

    # more than 0 inputs, more than 0 outputs
    assert validate_function(0, bytes((OP_ADDRESS, OP_ADDRESS, OP_CALLF, 0x00, 0x01, OP_POP, OP_POP, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(2, 3)]) == 3

    # recursion
    assert validate_function(0, bytes((OP_CALLF, 0x00, 0x00, OP_STOP)), [FunctionType(0, 0)]) == 0
    assert validate_function(0, bytes((OP_CALLF, 0x00, 0x00, OP_STOP)), [FunctionType(2, 0)]) == 2
    assert validate_function(0, bytes((OP_CALLF, 0x00, 0x00, OP_POP, OP_POP, OP_STOP)), [FunctionType(2, 2)]) == 2
    assert validate_function(1, bytes((OP_ADDRESS, OP_ADDRESS, OP_CALLF, 0x00, 0x01, OP_POP, OP_POP, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(2, 1)]) == 4

    # multiple CALLFs with different types
    assert validate_function(0, bytes((OP_PREVRANDAO, OP_CALLF, 0x00, 0x01, OP_DUP1, OP_DUP1, OP_CALLF, 0x00, 0x02, 
        OP_PREVRANDAO, OP_DUP1, OP_CALLF, 0x00, 0x03, OP_POP, OP_POP, OP_STOP)), [FunctionType(0, 0), FunctionType(1, 1), FunctionType(3, 0), FunctionType(2, 2)]) == 3

    # underflow
    assert validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(0, 0), FunctionType(1, 0)]) == -101
    assert validate_function(0, bytes((OP_ADDRESS, OP_CALLF, 0x00, 0x01, OP_STOP)), [FunctionType(0, 0), FunctionType(2, 0)]) == -101
    assert validate_function(0, bytes((OP_POP, OP_CALLF, 0x00, 0x00, OP_STOP)), [FunctionType(1, 0)]) == -101
    assert validate_function(0, bytes((OP_PREVRANDAO, OP_CALLF, 0x00, 0x01, OP_DUP1, OP_CALLF, 0x00, 0x02, OP_STOP)), 
        [FunctionType(0, 0), FunctionType(1, 1), FunctionType(3, 0)]) == -101

def test_retf():
    # 0 outpus
    assert validate_function(0, bytes((OP_RETF,)), [FunctionType(0, 0), FunctionType(0, 0)]) == 0
    assert validate_function(1, bytes((OP_RETF,)), [FunctionType(0, 0), FunctionType(0, 0)]) == 0
    assert validate_function(2, bytes((OP_RETF,)), [FunctionType(0, 0), FunctionType(1, 1), FunctionType(0, 0)]) == 0

    # more than 0 outputs
    assert validate_function(0, bytes((OP_PREVRANDAO, OP_RETF)), [FunctionType(0, 1), FunctionType(0, 1)]) == 1
    assert validate_function(1, bytes((OP_PREVRANDAO, OP_RETF)), [FunctionType(0, 1), FunctionType(0, 1)]) == 1

    # more than 1 outputs
    assert validate_function(1, bytes((OP_PREVRANDAO, OP_DUP1, OP_RETF)), [FunctionType(0, 0), FunctionType(0, 2)]) == 2

    # forwarding return value
    assert validate_function(0, bytes((OP_RETF,)), [FunctionType(1, 1)]) == 1
    assert validate_function(0, bytes((OP_CALLF, 0x00, 0x01, OP_RETF)), [FunctionType(0, 1), FunctionType(0, 1)]) == 1

    # multiple RETFs
    assert validate_function(0, bytes((OP_RJUMPI, 0x00, 0x03, OP_PREVRANDAO, OP_DUP1, OP_RETF, OP_ADDRESS, OP_DUP1, OP_RETF)), [FunctionType(1, 2)]) == 2

    # underflow
    assert validate_function(0, bytes((OP_RETF,)), [FunctionType(0, 1), FunctionType(0, 1)]) == -103
    assert validate_function(1, bytes((OP_RETF,)), [FunctionType(0, 1), FunctionType(0, 1)]) == -103
    assert validate_function(0, bytes((OP_RETF,)), [FunctionType(0, 1)]) == -103
    assert validate_function(1, bytes((OP_PREVRANDAO, OP_RETF)), [FunctionType(0, 0), FunctionType(0, 2)]) == -103
    assert validate_function(0, bytes((OP_RJUMPI, 0x00, 0x03, OP_PREVRANDAO, OP_DUP1, OP_RETF, OP_ADDRESS, OP_RETF)), [FunctionType(1, 2)]) == -103


def test_unreachable():
    # Max stack not changed by unreachable code
    assert validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_STOP, OP_ADDRESS, OP_ADDRESS, OP_ADDRESS, OP_POP, OP_POP, OP_POP, OP_STOP))) == 1
    assert validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_RETF, OP_ADDRESS, OP_ADDRESS, OP_ADDRESS, OP_POP, OP_POP, OP_POP, OP_STOP))) == 1
    assert validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_RJUMP, 0x00, 0x06, OP_ADDRESS, OP_ADDRESS, OP_ADDRESS, OP_POP, OP_POP, OP_POP, OP_STOP))) == 1
    # Stack underflow in unreachable code
    assert validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_STOP, OP_POP, OP_STOP))) == 1
    assert validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_RETF, OP_POP, OP_STOP))) == 1
    assert validate_function(0, bytes((OP_ADDRESS, OP_POP, OP_RJUMP, 0x00, 0x01, OP_POP, OP_STOP))) == 1


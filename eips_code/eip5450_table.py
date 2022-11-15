from dataclasses import dataclass


@dataclass
class InstrInfo:
    name: str
    immediate_size: int
    is_terminating: bool
    stack_height_required: int
    stack_height_change: int


OP_STOP = 0x00
OP_ADD = 0x01
OP_MUL = 0x02
OP_SUB = 0x03
OP_DIV = 0x04
OP_SDIV = 0x05
OP_MOD = 0x06
OP_SMOD = 0x07
OP_ADDMOD = 0x08
OP_MULMOD = 0x09
OP_EXP = 0x0a
OP_SIGNEXTEND = 0x0b

OP_LT = 0x10
OP_GT = 0x11
OP_SLT = 0x12
OP_SGT = 0x13
OP_EQ = 0x14
OP_ISZERO = 0x15
OP_AND = 0x16
OP_OR = 0x17
OP_XOR = 0x18
OP_NOT = 0x19
OP_BYTE = 0x1a
OP_SHL = 0x1b
OP_SHR = 0x1c
OP_SAR = 0x1d

OP_KECCAK256 = 0x20

OP_ADDRESS = 0x30
OP_BALANCE = 0x31
OP_ORIGIN = 0x32
OP_CALLER = 0x33
OP_CALLVALUE = 0x34
OP_CALLDATALOAD = 0x35
OP_CALLDATASIZE = 0x36
OP_CALLDATACOPY = 0x37
OP_CODESIZE = 0x38
OP_CODECOPY = 0x39
OP_GASPRICE = 0x3a
OP_EXTCODESIZE = 0x3b
OP_EXTCODECOPY = 0x3c
OP_RETURNDATASIZE = 0x3d
OP_RETURNDATACOPY = 0x3e
OP_EXTCODEHASH = 0x3f

OP_BLOCKHASH = 0x40
OP_COINBASE = 0x41
OP_TIMESTAMP = 0x42
OP_NUMBER = 0x43
OP_PREVRANDAO = 0x44
OP_GASLIMIT = 0x45
OP_CHAINID = 0x46
OP_SELFBALANCE = 0x47
OP_BASEFEE = 0x48

OP_POP = 0x50
OP_MLOAD = 0x51
OP_MSTORE = 0x52
OP_MSTORE8 = 0x53
OP_SLOAD = 0x54
OP_SSTORE = 0x55
OP_JUMP = 0x56
OP_JUMPI = 0x57
OP_PC = 0x58
OP_MSIZE = 0x59
OP_GAS = 0x5a
OP_JUMPDEST = 0x5b
OP_RJUMP = 0x5c
OP_RJUMPI = 0x5d

OP_PUSH0 = 0x5f
OP_PUSH1 = 0x60
OP_PUSH2 = 0x61
OP_PUSH3 = 0x62
OP_PUSH4 = 0x63
OP_PUSH5 = 0x64
OP_PUSH6 = 0x65
OP_PUSH7 = 0x66
OP_PUSH8 = 0x67
OP_PUSH9 = 0x68
OP_PUSH10 = 0x69
OP_PUSH11 = 0x6a
OP_PUSH12 = 0x6b
OP_PUSH13 = 0x6c
OP_PUSH14 = 0x6d
OP_PUSH15 = 0x6e
OP_PUSH16 = 0x6f
OP_PUSH17 = 0x70
OP_PUSH18 = 0x71
OP_PUSH19 = 0x72
OP_PUSH20 = 0x73
OP_PUSH21 = 0x74
OP_PUSH22 = 0x75
OP_PUSH23 = 0x76
OP_PUSH24 = 0x77
OP_PUSH25 = 0x78
OP_PUSH26 = 0x79
OP_PUSH27 = 0x7a
OP_PUSH28 = 0x7b
OP_PUSH29 = 0x7c
OP_PUSH30 = 0x7d
OP_PUSH31 = 0x7e
OP_PUSH32 = 0x7f
OP_DUP1 = 0x80
OP_DUP2 = 0x81
OP_DUP3 = 0x82
OP_DUP4 = 0x83
OP_DUP5 = 0x84
OP_DUP6 = 0x85
OP_DUP7 = 0x86
OP_DUP8 = 0x87
OP_DUP9 = 0x88
OP_DUP10 = 0x89
OP_DUP11 = 0x8a
OP_DUP12 = 0x8b
OP_DUP13 = 0x8c
OP_DUP14 = 0x8d
OP_DUP15 = 0x8e
OP_DUP16 = 0x8f
OP_SWAP1 = 0x90
OP_SWAP2 = 0x91
OP_SWAP3 = 0x92
OP_SWAP4 = 0x93
OP_SWAP5 = 0x94
OP_SWAP6 = 0x95
OP_SWAP7 = 0x96
OP_SWAP8 = 0x97
OP_SWAP9 = 0x98
OP_SWAP10 = 0x99
OP_SWAP11 = 0x9a
OP_SWAP12 = 0x9b
OP_SWAP13 = 0x9c
OP_SWAP14 = 0x9d
OP_SWAP15 = 0x9e
OP_SWAP16 = 0x9f
OP_LOG0 = 0xa0
OP_LOG1 = 0xa1
OP_LOG2 = 0xa2
OP_LOG3 = 0xa3
OP_LOG4 = 0xa4

OP_CALLF = 0xb0
OP_RETF = 0xb1

OP_CREATE = 0xf0
OP_CALL = 0xf1
OP_CALLCODE = 0xf2
OP_RETURN = 0xf3
OP_DELEGATECALL = 0xf4
OP_CREATE2 = 0xf5

OP_STATICCALL = 0xfa

OP_REVERT = 0xfd
OP_INVALID = 0xfe
OP_SELFDESTRUCT = 0xff

TABLE = 256 * [InstrInfo("undefined", 0, True, 0, 0)]

TABLE[OP_STOP] = InstrInfo("STOP", 0, True, 0, 0)
TABLE[OP_ADD] = InstrInfo("ADD", 0, False, 2, -1)
TABLE[OP_MUL] = InstrInfo("MUL", 0, False, 2, -1)
TABLE[OP_SUB] = InstrInfo("SUB", 0, False, 2, -1)
TABLE[OP_DIV] = InstrInfo("DIV", 0, False, 2, -1)
TABLE[OP_SDIV] = InstrInfo("SDIV", 0, False, 2, -1)
TABLE[OP_MOD] = InstrInfo("MOD", 0, False, 2, -1)
TABLE[OP_SMOD] = InstrInfo("SMOD", 0, False, 2, -1)
TABLE[OP_ADDMOD] = InstrInfo("ADDMOD", 0, False, 3, -2)
TABLE[OP_MULMOD] = InstrInfo("MULMOD", 0, False, 3, -2)
TABLE[OP_EXP] = InstrInfo("EXP", 0, False, 2, -1)
TABLE[OP_SIGNEXTEND] = InstrInfo("SIGNEXTEND", 0, False, 2, -1)

TABLE[OP_LT] = InstrInfo("LT", 0, False, 2, -1)
TABLE[OP_GT] = InstrInfo("GT", 0, False, 2, -1)
TABLE[OP_SLT] = InstrInfo("SLT", 0, False, 2, -1)
TABLE[OP_SGT] = InstrInfo("SGT", 0, False, 2, -1)
TABLE[OP_EQ] = InstrInfo("EQ", 0, False, 2, -1)
TABLE[OP_ISZERO] = InstrInfo("ISZERO", 0, False, 1, 0)
TABLE[OP_AND] = InstrInfo("AND", 0, False, 2, -1)
TABLE[OP_OR] = InstrInfo("OR", 0, False, 2, -1)
TABLE[OP_XOR] = InstrInfo("XOR", 0, False, 2, -1)
TABLE[OP_NOT] = InstrInfo("NOT", 0, False, 1, 0)
TABLE[OP_BYTE] = InstrInfo("BYTE", 0, False, 2, -1)
TABLE[OP_SHL] = InstrInfo("SHL", 0, False, 2, -1)
TABLE[OP_SHR] = InstrInfo("SHR", 0, False, 2, -1)
TABLE[OP_SAR] = InstrInfo("SAR", 0, False, 2, -1)

TABLE[OP_KECCAK256] = InstrInfo("KECCAK256", 0, False, 2, -1)

TABLE[OP_ADDRESS] = InstrInfo("ADDRESS", 0, False, 0, 1)
TABLE[OP_BALANCE] = InstrInfo("BALANCE", 0, False, 1, 0)
TABLE[OP_ORIGIN] = InstrInfo("ORIGIN", 0, False, 0, 1)
TABLE[OP_CALLER] = InstrInfo("CALLER", 0, False, 0, 1)
TABLE[OP_CALLVALUE] = InstrInfo("CALLVALUE", 0, False, 0, 1)
TABLE[OP_CALLDATALOAD] = InstrInfo("CALLDATALOAD", 0, False, 1, 0)
TABLE[OP_CALLDATASIZE] = InstrInfo("CALLDATASIZE", 0, False, 0, 1)
TABLE[OP_CALLDATACOPY] = InstrInfo("CALLDATACOPY", 0, False, 3, -3)
TABLE[OP_CODESIZE] = InstrInfo("CODESIZE", 0, False, 0, 1)
TABLE[OP_CODECOPY] = InstrInfo("CODECOPY", 0, False, 3, -3)
TABLE[OP_GASPRICE] = InstrInfo("GASPRICE", 0, False, 0, 1)
TABLE[OP_EXTCODESIZE] = InstrInfo("EXTCODESIZE", 0, False, 1, 0)
TABLE[OP_EXTCODECOPY] = InstrInfo("EXTCODECOPY", 0, False, 4, -4)
TABLE[OP_RETURNDATASIZE] = InstrInfo("RETURNDATASIZE", 0, False, 0, 1)
TABLE[OP_RETURNDATACOPY] = InstrInfo("RETURNDATACOPY", 0, False, 3, -3)
TABLE[OP_EXTCODEHASH] = InstrInfo("EXTCODEHASH", 0, False, 1, 0)

TABLE[OP_BLOCKHASH] = InstrInfo("BLOCKHASH", 0, False, 1, 0)
TABLE[OP_COINBASE] = InstrInfo("COINBASE", 0, False, 0, 1)
TABLE[OP_TIMESTAMP] = InstrInfo("TIMESTAMP", 0, False, 0, 1)
TABLE[OP_NUMBER] = InstrInfo("NUMBER", 0, False, 0, 1)
TABLE[OP_PREVRANDAO] = InstrInfo("PREVRANDAO", 0, False, 0, 1)
TABLE[OP_GASLIMIT] = InstrInfo("GASLIMIT", 0, False, 0, 1)
TABLE[OP_CHAINID] = InstrInfo("CHAINID", 0, False, 0, 1)
TABLE[OP_SELFBALANCE] = InstrInfo("SELFBALANCE", 0, False, 0, 1)
TABLE[OP_BASEFEE] = InstrInfo("BASEFEE", 0, False, 0, 1)

TABLE[OP_POP] = InstrInfo("POP", 0, False, 1, -1)
TABLE[OP_MLOAD] = InstrInfo("MLOAD", 0, False, 1, 0)
TABLE[OP_MSTORE] = InstrInfo("MSTORE", 0, False, 2, -2)
TABLE[OP_MSTORE8] = InstrInfo("MSTORE8", 0, False, 2, -2)
TABLE[OP_SLOAD] = InstrInfo("SLOAD", 0, False, 1, 0)
TABLE[OP_SSTORE] = InstrInfo("SSTORE", 0, False, 2, -2)
TABLE[OP_JUMP] = InstrInfo("JUMP", 0, False, 1, -1)
TABLE[OP_JUMPI] = InstrInfo("JUMPI", 0, False, 2, -2)
TABLE[OP_PC] = InstrInfo("PC", 0, False, 0, 1)
TABLE[OP_MSIZE] = InstrInfo("MSIZE", 0, False, 0, 1)
TABLE[OP_GAS] = InstrInfo("GAS", 0, False, 0, 1)
TABLE[OP_JUMPDEST] = InstrInfo("JUMPDEST", 0, False, 0, 0)
TABLE[OP_RJUMP] = InstrInfo("RJUMP", 2, False, 0, 0)
TABLE[OP_RJUMPI] = InstrInfo("RJUMPI", 2, False, 1, -1)

TABLE[OP_PUSH0] = InstrInfo("PUSH0", 0, False, 0, 1)

TABLE[OP_PUSH1] = InstrInfo("PUSH1", 1, False, 0, 1)
TABLE[OP_PUSH2] = InstrInfo("PUSH2", 2, False, 0, 1)
TABLE[OP_PUSH3] = InstrInfo("PUSH3", 3, False, 0, 1)
TABLE[OP_PUSH4] = InstrInfo("PUSH4", 4, False, 0, 1)
TABLE[OP_PUSH5] = InstrInfo("PUSH5", 5, False, 0, 1)
TABLE[OP_PUSH6] = InstrInfo("PUSH6", 6, False, 0, 1)
TABLE[OP_PUSH7] = InstrInfo("PUSH7", 7, False, 0, 1)
TABLE[OP_PUSH8] = InstrInfo("PUSH8", 8, False, 0, 1)
TABLE[OP_PUSH9] = InstrInfo("PUSH9", 9, False, 0, 1)
TABLE[OP_PUSH10] = InstrInfo("PUSH10", 10, False, 0, 1)
TABLE[OP_PUSH11] = InstrInfo("PUSH11", 11, False, 0, 1)
TABLE[OP_PUSH12] = InstrInfo("PUSH12", 12, False, 0, 1)
TABLE[OP_PUSH13] = InstrInfo("PUSH13", 13, False, 0, 1)
TABLE[OP_PUSH14] = InstrInfo("PUSH14", 14, False, 0, 1)
TABLE[OP_PUSH15] = InstrInfo("PUSH15", 15, False, 0, 1)
TABLE[OP_PUSH16] = InstrInfo("PUSH16", 16, False, 0, 1)
TABLE[OP_PUSH17] = InstrInfo("PUSH17", 17, False, 0, 1)
TABLE[OP_PUSH18] = InstrInfo("PUSH18", 18, False, 0, 1)
TABLE[OP_PUSH19] = InstrInfo("PUSH19", 19, False, 0, 1)
TABLE[OP_PUSH20] = InstrInfo("PUSH20", 20, False, 0, 1)
TABLE[OP_PUSH21] = InstrInfo("PUSH21", 21, False, 0, 1)
TABLE[OP_PUSH22] = InstrInfo("PUSH22", 22, False, 0, 1)
TABLE[OP_PUSH23] = InstrInfo("PUSH23", 23, False, 0, 1)
TABLE[OP_PUSH24] = InstrInfo("PUSH24", 24, False, 0, 1)
TABLE[OP_PUSH25] = InstrInfo("PUSH25", 25, False, 0, 1)
TABLE[OP_PUSH26] = InstrInfo("PUSH26", 26, False, 0, 1)
TABLE[OP_PUSH27] = InstrInfo("PUSH27", 27, False, 0, 1)
TABLE[OP_PUSH28] = InstrInfo("PUSH28", 28, False, 0, 1)
TABLE[OP_PUSH29] = InstrInfo("PUSH29", 29, False, 0, 1)
TABLE[OP_PUSH30] = InstrInfo("PUSH30", 30, False, 0, 1)
TABLE[OP_PUSH31] = InstrInfo("PUSH31", 31, False, 0, 1)
TABLE[OP_PUSH32] = InstrInfo("PUSH32", 32, False, 0, 1)

TABLE[OP_DUP1] = InstrInfo("DUP1", 0, False, 1, 1)
TABLE[OP_DUP2] = InstrInfo("DUP2", 0, False, 2, 1)
TABLE[OP_DUP3] = InstrInfo("DUP3", 0, False, 3, 1)
TABLE[OP_DUP4] = InstrInfo("DUP4", 0, False, 4, 1)
TABLE[OP_DUP5] = InstrInfo("DUP5", 0, False, 5, 1)
TABLE[OP_DUP6] = InstrInfo("DUP6", 0, False, 6, 1)
TABLE[OP_DUP7] = InstrInfo("DUP7", 0, False, 7, 1)
TABLE[OP_DUP8] = InstrInfo("DUP8", 0, False, 8, 1)
TABLE[OP_DUP9] = InstrInfo("DUP9", 0, False, 9, 1)
TABLE[OP_DUP10] = InstrInfo("DUP10", 0, False, 10, 1)
TABLE[OP_DUP11] = InstrInfo("DUP11", 0, False, 11, 1)
TABLE[OP_DUP12] = InstrInfo("DUP12", 0, False, 12, 1)
TABLE[OP_DUP13] = InstrInfo("DUP13", 0, False, 13, 1)
TABLE[OP_DUP14] = InstrInfo("DUP14", 0, False, 14, 1)
TABLE[OP_DUP15] = InstrInfo("DUP15", 0, False, 15, 1)
TABLE[OP_DUP16] = InstrInfo("DUP16", 0, False, 16, 1)

TABLE[OP_SWAP1] = InstrInfo("SWAP1", 0, False, 2, 0)
TABLE[OP_SWAP2] = InstrInfo("SWAP2", 0, False, 3, 0)
TABLE[OP_SWAP3] = InstrInfo("SWAP3", 0, False, 4, 0)
TABLE[OP_SWAP4] = InstrInfo("SWAP4", 0, False, 5, 0)
TABLE[OP_SWAP5] = InstrInfo("SWAP5", 0, False, 6, 0)
TABLE[OP_SWAP6] = InstrInfo("SWAP6", 0, False, 7, 0)
TABLE[OP_SWAP7] = InstrInfo("SWAP7", 0, False, 8, 0)
TABLE[OP_SWAP8] = InstrInfo("SWAP8", 0, False, 9, 0)
TABLE[OP_SWAP9] = InstrInfo("SWAP9", 0, False, 10, 0)
TABLE[OP_SWAP10] = InstrInfo("SWAP10", 0, False, 11, 0)
TABLE[OP_SWAP11] = InstrInfo("SWAP11", 0, False, 12, 0)
TABLE[OP_SWAP12] = InstrInfo("SWAP12", 0, False, 13, 0)
TABLE[OP_SWAP13] = InstrInfo("SWAP13", 0, False, 14, 0)
TABLE[OP_SWAP14] = InstrInfo("SWAP14", 0, False, 15, 0)
TABLE[OP_SWAP15] = InstrInfo("SWAP15", 0, False, 16, 0)
TABLE[OP_SWAP16] = InstrInfo("SWAP16", 0, False, 17, 0)

TABLE[OP_LOG0] = InstrInfo("LOG0", 0, False, 2, -2)
TABLE[OP_LOG1] = InstrInfo("LOG1", 0, False, 3, -3)
TABLE[OP_LOG2] = InstrInfo("LOG2", 0, False, 4, -4)
TABLE[OP_LOG3] = InstrInfo("LOG3", 0, False, 5, -5)
TABLE[OP_LOG4] = InstrInfo("LOG4", 0, False, 6, -6)

TABLE[OP_CREATE] = InstrInfo("CREATE", 0, False, 3, -2)
TABLE[OP_CALL] = InstrInfo("CALL", 0, False, 7, -6)
TABLE[OP_CALLCODE] = InstrInfo("CALLCODE", 0, False, 7, -6)
TABLE[OP_RETURN] = InstrInfo("RETURN", 0, True, 2, -2)
TABLE[OP_DELEGATECALL] = InstrInfo("DELEGATECALL", 0, False, 6, -5)
TABLE[OP_CREATE2] = InstrInfo("CREATE2", 0, False, 4, -3)
TABLE[OP_STATICCALL] = InstrInfo("STATICCALL", 0, False, 6, -5)
TABLE[OP_CALLF] = InstrInfo("CALLF", 2, False, 0, 0)
TABLE[OP_RETF] = InstrInfo("RETF", 0, True, 0, 0)
TABLE[OP_REVERT] = InstrInfo("REVERT", 0, True, 2, -2)
TABLE[OP_INVALID] = InstrInfo("INVALID", 0, True, 0, 0)
TABLE[OP_SELFDESTRUCT] = InstrInfo("SELFDESTRUCT", 0, True, 1, -1)

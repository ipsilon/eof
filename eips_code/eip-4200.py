# The below are ranges as specified in the Yellow Paper.
# Note: range(s, e) excludes e, hence the +1
valid_opcodes = [
    *range(0x00, 0x0b + 1),
    *range(0x10, 0x1d + 1),
    0x20,
    *range(0x30, 0x3f + 1),
    *range(0x40, 0x47 + 1),
    *range(0x50, 0x5d + 1),
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
    # RJUMP and RJUMPI
    elif opcode == 0x5c or opcode == 0x5d:
        immediate_sizes.append(2)
    else:
        immediate_sizes.append(0)


# Fails with assertion on invalid code
def validate_code(code: bytes):
    # Note that EOF1 already asserts this with the code section requirements
    assert(len(code) > 0)

    opcode = 0
    pos = 0
    rjumpdests = set()
    immediates = set()
    while pos < len(code):
        # Ensure the opcode is valid
        opcode = code[pos]
        pos += 1
        assert(opcode in valid_opcodes)

        if opcode == 0x5c or opcode == 0x5d:
            assert(pos + 2 <= len(code))
            offset = int.from_bytes(code[pos:pos+2], byteorder = "big", signed = True)

            rjumpdest = pos + immediate_sizes[opcode] + offset 
            assert(rjumpdest >= 0 and rjumpdest < len(code))

            rjumpdests.add(rjumpdest)

        # Save immediate value positions
        immediates.update(range(pos, pos + immediate_sizes[opcode]))
        # Skip immediates
        pos += immediate_sizes[opcode]

    # Ensure last opcode's immediate doesn't go over code end
    assert(pos == len(code))

    # opcode is the *last opcode*
    assert(opcode in terminating_opcodes)

    # Ensure relative jump destinations don't target immediates
    assert(rjumpdests.isdisjoint(immediates))


def test_validate_code(code: bytes) -> bool:
    try:
        validate_code(code)
        return True
    except:
        return False

def hex(code: bytes) -> str:
    return ''.join(format(x, '02x') for x in code)


# Some valid opcodes
assert test_validate_code(b'\x30\x00') == True
assert test_validate_code(b'\x50\x00') == True
assert test_validate_code(b'\xfe\x00') == True
assert test_validate_code(b'\xff\x00') == True

# PUSHes with valid immediates
assert test_validate_code(b'\x60\x00\x00') == True
assert test_validate_code(b'\x61' + b'\x00' * 2 + b'\x00') == True
assert test_validate_code(b'\x62' + b'\x00' * 3 + b'\x00') == True
assert test_validate_code(b'\x63' + b'\x00' * 4 + b'\x00') == True
assert test_validate_code(b'\x64' + b'\x00' * 5 + b'\x00') == True
assert test_validate_code(b'\x65' + b'\x00' * 6 + b'\x00') == True
assert test_validate_code(b'\x66' + b'\x00' * 7 + b'\x00') == True
assert test_validate_code(b'\x67' + b'\x00' * 8 + b'\x00') == True
assert test_validate_code(b'\x68' + b'\x00' * 9 + b'\x00') == True
assert test_validate_code(b'\x69' + b'\x00' * 10 + b'\x00') == True
assert test_validate_code(b'\x6a' + b'\x00' * 11 + b'\x00') == True
assert test_validate_code(b'\x6b' + b'\x00' * 12 + b'\x00') == True
assert test_validate_code(b'\x6c' + b'\x00' * 13 + b'\x00') == True
assert test_validate_code(b'\x6d' + b'\x00' * 14 + b'\x00') == True
assert test_validate_code(b'\x6e' + b'\x00' * 15 + b'\x00') == True
assert test_validate_code(b'\x6f' + b'\x00' * 16 + b'\x00') == True
assert test_validate_code(b'\x70' + b'\x00' * 17 + b'\x00') == True
assert test_validate_code(b'\x71' + b'\x00' * 18 + b'\x00') == True
assert test_validate_code(b'\x72' + b'\x00' * 19 + b'\x00') == True
assert test_validate_code(b'\x73' + b'\x00' * 20 + b'\x00') == True
assert test_validate_code(b'\x74' + b'\x00' * 21 + b'\x00') == True
assert test_validate_code(b'\x75' + b'\x00' * 22 + b'\x00') == True
assert test_validate_code(b'\x76' + b'\x00' * 23 + b'\x00') == True
assert test_validate_code(b'\x77' + b'\x00' * 24 + b'\x00') == True
assert test_validate_code(b'\x78' + b'\x00' * 25 + b'\x00') == True
assert test_validate_code(b'\x79' + b'\x00' * 26 + b'\x00') == True
assert test_validate_code(b'\x7a' + b'\x00' * 27 + b'\x00') == True
assert test_validate_code(b'\x7b' + b'\x00' * 28 + b'\x00') == True
assert test_validate_code(b'\x7c' + b'\x00' * 29 + b'\x00') == True
assert test_validate_code(b'\x7d' + b'\x00' * 30 + b'\x00') == True
assert test_validate_code(b'\x7e' + b'\x00' * 31 + b'\x00') == True
assert test_validate_code(b'\x7f' + b'\x00' * 32 + b'\x00') == True

# RJUMP with valid immediates
# offset = 0
assert test_validate_code(b'\x5c\x00\x00\x00') == True
# offset = 1
assert test_validate_code(b'\x5c\x00\x01\x00\x00') == True
# offset = 4
assert test_validate_code(b'\x5c\x00\x01\x00\x00\x00\x00\x00') == True
# offset = 256
assert test_validate_code(b'\x5c\x01\x00' + b'\x00' * 256 + b'\x00') == True
# offset = 32767
assert test_validate_code(b'\x5c\x7f\xff' + b'\x00' * 32767 + b'\x00') == True
# offset = -3
assert test_validate_code(b'\x5c\xff\xfd\x00\x00') == True
# offset = -4
assert test_validate_code(b'\x00\x5c\xff\xfc\x00') == True
# offset = -256
assert test_validate_code(b'\x00' * 253 + b'\x5c\xff\x00\x00') == True
# offset = -32768
assert test_validate_code(b'\x00' * 32765 + b'\x5c\x80\x01\x00') == True
# RJUMPI with valid immediates
# offset = 0
assert test_validate_code(b'\x60\x01\x5d\x00\x00\x00') == True
# offset = 1
assert test_validate_code(b'\x60\x01\x5d\x00\x01\x00\x00') == True
# offset = 4
assert test_validate_code(b'\x60\x01\x5d\x00\x01\x00\x00\x00\x00\x00') == True
# offset = 256
assert test_validate_code(b'\x60\x01\x5d\x01\x00' + b'\x00' * 256 + b'\x00') == True
# offset = 32767
assert test_validate_code(b'\x60\x01\x5d\x7f\xff' + b'\x00' * 32767 + b'\x00') == True
# offset = -3
assert test_validate_code(b'\x60\x01\x5d\xff\xfd\x00\x00') == True
# offset = -5
assert test_validate_code(b'\x60\x01\x5d\xff\xfb\x00') == True
# offset = -256
assert test_validate_code(b'\x00' * 252 + b'\x60\x01\x5d\xff\x00\x00') == True
# offset = -32768
assert test_validate_code(b'\x00' * 32763 + b'\x60\x01\x5d\x80\x01\x00') == True
# RJUMP without PUSH before - still valid
assert test_validate_code(b'\x5d\x00\x00\x00') == True


# Valid code terminators
assert test_validate_code(b'\x00') == True
assert test_validate_code(b'\xf3') == True
assert test_validate_code(b'\xfd') == True
assert test_validate_code(b'\xfe') == True


# Empty code
assert test_validate_code(b'') == False
# Valid opcode, but invalid as terminator
assert test_validate_code(b'\x5b') == False
# Invalid opcodes
assert test_validate_code(b'\x0c\x00') == False
assert test_validate_code(b'\x0d\x00') == False
assert test_validate_code(b'\x0e\x00') == False
assert test_validate_code(b'\x0f\x00') == False

assert test_validate_code(b'\x1e\x00') == False
assert test_validate_code(b'\x1f\x00') == False

assert test_validate_code(b'\x21\x00') == False
assert test_validate_code(b'\x22\x00') == False
assert test_validate_code(b'\x23\x00') == False
assert test_validate_code(b'\x24\x00') == False
assert test_validate_code(b'\x25\x00') == False
assert test_validate_code(b'\x26\x00') == False
assert test_validate_code(b'\x27\x00') == False
assert test_validate_code(b'\x28\x00') == False
assert test_validate_code(b'\x29\x00') == False
assert test_validate_code(b'\x2a\x00') == False
assert test_validate_code(b'\x2b\x00') == False
assert test_validate_code(b'\x2c\x00') == False
assert test_validate_code(b'\x2d\x00') == False
assert test_validate_code(b'\x2e\x00') == False
assert test_validate_code(b'\x2f\x00') == False

assert test_validate_code(b'\x49\x00') == False
assert test_validate_code(b'\x4a\x00') == False
assert test_validate_code(b'\x4b\x00') == False
assert test_validate_code(b'\x4c\x00') == False
assert test_validate_code(b'\x4d\x00') == False
assert test_validate_code(b'\x4e\x00') == False
assert test_validate_code(b'\x4f\x00') == False

assert test_validate_code(b'\x5e\x00') == False
assert test_validate_code(b'\x5f\x00') == False

assert test_validate_code(b'\xa5\x00') == False
assert test_validate_code(b'\xa6\x00') == False
assert test_validate_code(b'\xa7\x00') == False
assert test_validate_code(b'\xa8\x00') == False
assert test_validate_code(b'\xa9\x00') == False
assert test_validate_code(b'\xaa\x00') == False
assert test_validate_code(b'\xab\x00') == False
assert test_validate_code(b'\xac\x00') == False
assert test_validate_code(b'\xad\x00') == False
assert test_validate_code(b'\xae\x00') == False
assert test_validate_code(b'\xaf\x00') == False

assert test_validate_code(b'\xb0\x00') == False
assert test_validate_code(b'\xb1\x00') == False
assert test_validate_code(b'\xb2\x00') == False
assert test_validate_code(b'\xb3\x00') == False
assert test_validate_code(b'\xb4\x00') == False
assert test_validate_code(b'\xb5\x00') == False
assert test_validate_code(b'\xb6\x00') == False
assert test_validate_code(b'\xb7\x00') == False
assert test_validate_code(b'\xb8\x00') == False
assert test_validate_code(b'\xb9\x00') == False
assert test_validate_code(b'\xba\x00') == False
assert test_validate_code(b'\xbb\x00') == False
assert test_validate_code(b'\xbc\x00') == False
assert test_validate_code(b'\xbd\x00') == False
assert test_validate_code(b'\xbe\x00') == False
assert test_validate_code(b'\xbf\x00') == False

assert test_validate_code(b'\xc0\x00') == False
assert test_validate_code(b'\xc1\x00') == False
assert test_validate_code(b'\xc2\x00') == False
assert test_validate_code(b'\xc3\x00') == False
assert test_validate_code(b'\xc4\x00') == False
assert test_validate_code(b'\xc5\x00') == False
assert test_validate_code(b'\xc6\x00') == False
assert test_validate_code(b'\xc7\x00') == False
assert test_validate_code(b'\xc8\x00') == False
assert test_validate_code(b'\xc9\x00') == False
assert test_validate_code(b'\xca\x00') == False
assert test_validate_code(b'\xcb\x00') == False
assert test_validate_code(b'\xcc\x00') == False
assert test_validate_code(b'\xcd\x00') == False
assert test_validate_code(b'\xce\x00') == False
assert test_validate_code(b'\xcf\x00') == False

assert test_validate_code(b'\xd0\x00') == False
assert test_validate_code(b'\xd1\x00') == False
assert test_validate_code(b'\xd2\x00') == False
assert test_validate_code(b'\xd3\x00') == False
assert test_validate_code(b'\xd4\x00') == False
assert test_validate_code(b'\xd5\x00') == False
assert test_validate_code(b'\xd6\x00') == False
assert test_validate_code(b'\xd7\x00') == False
assert test_validate_code(b'\xd8\x00') == False
assert test_validate_code(b'\xd9\x00') == False
assert test_validate_code(b'\xda\x00') == False
assert test_validate_code(b'\xdb\x00') == False
assert test_validate_code(b'\xdc\x00') == False
assert test_validate_code(b'\xdd\x00') == False
assert test_validate_code(b'\xde\x00') == False
assert test_validate_code(b'\xdf\x00') == False

assert test_validate_code(b'\xe0\x00') == False
assert test_validate_code(b'\xe1\x00') == False
assert test_validate_code(b'\xe2\x00') == False
assert test_validate_code(b'\xe3\x00') == False
assert test_validate_code(b'\xe4\x00') == False
assert test_validate_code(b'\xe5\x00') == False
assert test_validate_code(b'\xe6\x00') == False
assert test_validate_code(b'\xe7\x00') == False
assert test_validate_code(b'\xe8\x00') == False
assert test_validate_code(b'\xe9\x00') == False
assert test_validate_code(b'\xea\x00') == False
assert test_validate_code(b'\xeb\x00') == False
assert test_validate_code(b'\xec\x00') == False
assert test_validate_code(b'\xed\x00') == False
assert test_validate_code(b'\xee\x00') == False
assert test_validate_code(b'\xef\x00') == False

assert test_validate_code(b'\xf6\x00') == False
assert test_validate_code(b'\xf7\x00') == False
assert test_validate_code(b'\xf8\x00') == False
assert test_validate_code(b'\xf9\x00') == False
assert test_validate_code(b'\xfb\x00') == False
assert test_validate_code(b'\xfc\x00') == False

# PUSHes with truncated immediates
assert test_validate_code(b'\x60\x00') == False
assert test_validate_code(b'\x61' + b'\x00' * 1 + b'\x00') == False
assert test_validate_code(b'\x62' + b'\x00' * 2 + b'\x00') == False
assert test_validate_code(b'\x63' + b'\x00' * 3 + b'\x00') == False
assert test_validate_code(b'\x64' + b'\x00' * 4 + b'\x00') == False
assert test_validate_code(b'\x65' + b'\x00' * 5 + b'\x00') == False
assert test_validate_code(b'\x66' + b'\x00' * 6 + b'\x00') == False
assert test_validate_code(b'\x67' + b'\x00' * 7 + b'\x00') == False
assert test_validate_code(b'\x68' + b'\x00' * 8 + b'\x00') == False
assert test_validate_code(b'\x69' + b'\x00' * 9 + b'\x00') == False
assert test_validate_code(b'\x6a' + b'\x00' * 10 + b'\x00') == False
assert test_validate_code(b'\x6b' + b'\x00' * 11 + b'\x00') == False
assert test_validate_code(b'\x6c' + b'\x00' * 12 + b'\x00') == False
assert test_validate_code(b'\x6d' + b'\x00' * 13 + b'\x00') == False
assert test_validate_code(b'\x6e' + b'\x00' * 14 + b'\x00') == False
assert test_validate_code(b'\x6f' + b'\x00' * 15 + b'\x00') == False
assert test_validate_code(b'\x70' + b'\x00' * 16 + b'\x00') == False
assert test_validate_code(b'\x71' + b'\x00' * 17 + b'\x00') == False
assert test_validate_code(b'\x72' + b'\x00' * 18 + b'\x00') == False
assert test_validate_code(b'\x73' + b'\x00' * 19 + b'\x00') == False
assert test_validate_code(b'\x74' + b'\x00' * 20 + b'\x00') == False
assert test_validate_code(b'\x75' + b'\x00' * 21 + b'\x00') == False
assert test_validate_code(b'\x76' + b'\x00' * 22 + b'\x00') == False
assert test_validate_code(b'\x77' + b'\x00' * 23 + b'\x00') == False
assert test_validate_code(b'\x78' + b'\x00' * 24 + b'\x00') == False
assert test_validate_code(b'\x79' + b'\x00' * 25 + b'\x00') == False
assert test_validate_code(b'\x7a' + b'\x00' * 26 + b'\x00') == False
assert test_validate_code(b'\x7b' + b'\x00' * 27 + b'\x00') == False
assert test_validate_code(b'\x7c' + b'\x00' * 28 + b'\x00') == False
assert test_validate_code(b'\x7d' + b'\x00' * 29 + b'\x00') == False
assert test_validate_code(b'\x7e' + b'\x00' * 30 + b'\x00') == False
assert test_validate_code(b'\x7f' + b'\x00' * 31 + b'\x00') == False

# RJUMP with truncated immmediate
assert test_validate_code(b'\x5c') == False
assert test_validate_code(b'\x5c\x00') == False
assert test_validate_code(b'\x5c\x00\x00') == False
# RJUMPI with truncated immmediate
assert test_validate_code(b'\x60\x01\x5d') == False
assert test_validate_code(b'\x60\x01\x5d\x00') == False
assert test_validate_code(b'\x60\x01\x5d\x00\x00') == False

# RJUMP destination out of bounds
# offset = 1
assert test_validate_code(b'\x5c\x00\x01\x00') == False
# offset = -4
assert test_validate_code(b'\x5c\xff\xfc\x00') == False
# RJUMPI destination out of bounds
# offset = 1
assert test_validate_code(b'\x60\x01\x5d\x00\x01\x00') == False
# offset = -6
assert test_validate_code(b'\x60\x01\x5d\xff\xfa\x00') == False

# RJUMP / RJUMPI into PUSH immediate
for n in range(1, 33):
    for offset in range(1, n + 1):
        code = [0x5c, 0x00, offset] # RJUMP offset
        code += [0x60 + n - 1] # PUSHn
        code += [0x00] * n     # push data
        code += [0x00]         # STOP

        assert test_validate_code(code) == False, "code expected to be invalid: " + hex(code)

        code = [0x60, 0x01, 0x5d, 0x00, offset] # PUSH1 1 RJUMI offset
        code += [0x60 + n - 1] # PUSHn
        code += [0x00] * n     # push data
        code += [0x00]         # STOP

        assert test_validate_code(code) == False, "code expected to be invalid: " +  hex(code)

# RJUMP into RJUMP immediate
assert test_validate_code(b'\x5c\x00\x01\x5c\x00\x01\x00') == False
assert test_validate_code(b'\x5c\x00\x02\x5c\x00\x01\x00') == False
# RJUMPI into RJUMP immediate
assert test_validate_code(b'\x60\x01\x5d\x00\x01\x5c\x00\x01\x00') == False
assert test_validate_code(b'\x60\x01\x5d\x00\x02\x5c\x00\x01\x00') == False
# RJUMP into RJUMPI immediate
assert test_validate_code(b'\x5c\x00\x03\x60\x01\x5d\x00\x01\x00') == False
assert test_validate_code(b'\x5c\x00\x04\x60\x01\x5d\x00\x01\x00') == False
# RJUMPI into RJUMPI immediate
assert test_validate_code(b'\x60\x01\x5d\x00\x03\x60\x01\x5d\x00\x01\x00') == False
assert test_validate_code(b'\x60\x01\x5d\x00\x04\x60\x01\x5d\x00\x01\x00') == False

# 0x5c byte which could be interpreted a RJUMP, but it's not because it's in PUSH data
assert test_validate_code(b'\x60\x5c\x00\x10\x00') == True
assert test_validate_code(b'\x61\x00\x5c\x00\x10\x00') == True
# 0x5d byte which could be interpreted a RJUMPI, but it's not because it's in PUSH data
assert test_validate_code(b'\x60\x5d\x00\x10\x00') == True
assert test_validate_code(b'\x61\x00\x5d\x00\x10\x00') == True

# 0x60 byte which could be interpreted as PUSH, but it's not because it's in RJUMP data
# offset = -160
assert test_validate_code(b'0x00' * 160 + b'\x5c\xff\x60\x00') == True
# 0x60 byte which could be interpreted as PUSH, but it's not because it's in RJUMPI data
# offset = -160
assert test_validate_code(b'0x00' * 160 + b'\x5d\xff\x60\x00') == True

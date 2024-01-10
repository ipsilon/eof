def encode_unsigned(value: int) -> bytes:
    assert value >= 0

    if value == 0:
        return b"\x00"

    ret = bytearray()
    while value > 0:
        char = value & 0x7F
        value >>= 7

        ret.append(char)

    # set the continuation bits
    for i, char in enumerate(ret):
        if i == 0:
            continue
        ret[i] |= 0x80

    # flip to big endian
    ret.reverse()

    return bytes(ret)

def decode_unsigned(value: bytes) -> int:
    ret = 0
    for char in (value):
        ret <<= 7
        ret |= char & 0x7F
        if char & 0x80 == 0:  # check continuation byte
            break
    else:
        raise ValueError(value)  # TODO: use validation error

    return ret

def encode_signed(value: int) -> bytes:
    bits = value.bit_length()
    bits += 7 - (bits % 7)

    # https://gist.github.com/mfuerstenau/ba870a29e16536fdbaba
    zigzag = (value >> bits - 1) ^ (value << 1)

    return encode_unsigned(zigzag)

def decode_signed(value: bytes) -> int:
    int_val = decode_unsigned(value)

    # zig zag decoding
    # https://gist.github.com/mfuerstenau/ba870a29e16536fdbaba
    return (int_val >> 1) ^ -(int_val & 1)

def test_encode_decode():
    import time
    t0 = time.time()
    for i in range(2**21):
        assert decode_unsigned(encode_unsigned(i)) == i, i
        assert decode_signed(encode_signed(i)) == i, i
        assert decode_signed(encode_signed(-i)) == -i, -i
    t1 = time.time()
    elapsed = t1 - t0
    per_item = elapsed / i
    print(f"test_encode_decode took: {elapsed}s ({per_item}s per item)")

def test_variable_length():
    import time
    import math
    t0 = time.time()
    for i in range(2**21):
        if i == 0:
            assert len(encode_unsigned(i)) == 1
            continue
        assert len(encode_unsigned(i)) == math.ceil(i.bit_length() / 7), i
        assert len(encode_signed(i)) == math.ceil((i.bit_length() + 1) / 7), i
        assert len(encode_signed(-i)) == math.ceil(((i - 1).bit_length() + 1) / 7), -i

    t1 = time.time()
    elapsed = t1 - t0
    per_item = elapsed / i
    print(f"test_variable_length took: {elapsed}s ({per_item}s per item)")

def time_to_bytes_from_bytes():
    import time
    import math
    t0 = time.time()
    for i in range(2**21):
        n_bytes = i.bit_length() // 8 + 1
        assert int.from_bytes(i.to_bytes(n_bytes, "big"), "big") == i, i

    t1 = time.time()
    elapsed = t1 - t0
    per_item = elapsed / i
    print(f"test_timer took: {elapsed}s ({per_item}s per item)")

def time_to_bytes():
    import time
    import math
    t0 = time.time()
    for i in range(2**21):
        n_bytes = i.bit_length() // 8 + 1
        assert len(i.to_bytes(n_bytes, "big")) == n_bytes

    t1 = time.time()
    elapsed = t1 - t0
    per_item = elapsed / i
    print(f"test_timer took: {elapsed}s ({per_item}s per item)")

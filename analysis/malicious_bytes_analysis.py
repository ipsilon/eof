PUSH1 = 0x60
PUSH32 = 0x7f
JUMPDEST = 0x5b


def get_offsets_of_malicious_bytes(code):
    malicious_bytes_offsets = []
    L = len(code)
    i = 0
    while i < L:
        op = code[i]
        i += 1
        if PUSH1 <= op <= PUSH32:
            p = i - 1
            i += op - PUSH1 + 1
            while (p := code.find(JUMPDEST, p + 1, i)) != -1:
                malicious_bytes_offsets.append(p)

    return malicious_bytes_offsets


def test_get_offsets_of_malicious_bytes():
    assert get_offsets_of_malicious_bytes(b'') == []
    assert get_offsets_of_malicious_bytes(bytes.fromhex("605b")) == [1]
    assert get_offsets_of_malicious_bytes(bytes.fromhex("61005b")) == [2]
    assert get_offsets_of_malicious_bytes(bytes.fromhex("615b5b")) == [1, 2]
    assert get_offsets_of_malicious_bytes(bytes.fromhex("FE7f5b5b0000005b005b")) == [2, 3, 7, 9]
    assert get_offsets_of_malicious_bytes(bytes.fromhex("6100001161005b11615b00")) == [6, 9]


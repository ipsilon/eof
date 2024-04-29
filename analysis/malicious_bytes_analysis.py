from dataclasses import dataclass
from typing import List

PUSH1 = 0x60
PUSH32 = 0x7f
JUMPDEST = 0x5b
CHUNK_LEN = 32


@dataclass
class Chunk:
    first_instruction_offset: int
    first_jumpdest_offset: int = CHUNK_LEN
    contains_invalid_jumpdest: bool = False


def get_chunks(code):
    chunks: List[Chunk] = []
    pushdata_remaining = 0
    for i, op in enumerate(code):
        offset = i % CHUNK_LEN
        if offset == 0:
            chunks.append(Chunk(first_instruction_offset=pushdata_remaining))

        ch = chunks[len(chunks) - 1]

        if pushdata_remaining > 0:
            if op == JUMPDEST:
                ch.contains_invalid_jumpdest = True
            pushdata_remaining -= 1
        else:
            if PUSH1 <= op <= PUSH32:
                pushdata_remaining = op - PUSH1 + 1
            elif op == JUMPDEST:
                ch.first_jumpdest_offset = min(ch.first_jumpdest_offset, offset)

    return chunks


def test_first_instruction_offset():
    def _(s):
        return [ch.first_instruction_offset for ch in get_chunks(bytes.fromhex(s))]

    assert _('') == []
    assert _('00') == [0]
    assert _('60dd') == [0]
    assert _('00' * 31 + '60dd') == [0, 1]
    assert _('00' * 31 + '61dddd00') == [0, 2]
    assert _('00' * 30 + '61dddd00') == [0, 1]
    assert _('00' * 32 + '61dddd00') == [0, 0]
    assert _('00' * 31 + '7fdd') == [0, 32]


def test_contains_invalid_jumpdest():
    def _(s):
        return [ch.contains_invalid_jumpdest for ch in get_chunks(bytes.fromhex(s))]

    assert _('') == []
    assert _('00') == [False]
    assert _('605b') == [True]
    assert _('00' * 32 + '63dddd5bdd') == [False, True]
    assert _('00' * 31 + '60' + '605b') == [False, False]


def test_first_jumpdest_offset():
    def _(s):
        return [ch.first_jumpdest_offset for ch in get_chunks(bytes.fromhex(s))]

    assert _('') == []
    assert _('00') == [32]
    assert _('5b') == [0]
    assert _('005b') == [1]
    assert _('615b5b5b') == [3]
    assert _('00' * 31 + '5b') == [31]
    assert _('00' * 32 + '5b') == [32, 0]
    assert _('00' * 32 + '005b') == [32, 1]
    assert _('00' * 32 + '605b') == [32, 32]
    assert _('7f' + '5b' * 31 + '605b') == [32, 1]


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

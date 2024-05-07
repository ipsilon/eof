import json
from dataclasses import dataclass, field
from typing import List

PUSH1 = 0x60
PUSH32 = 0x7f
JUMPDEST = 0x5b
CHUNK_LEN = 32


@dataclass
class Chunk:
    first_instruction_offset: int
    jumpdests: List[int] = field(default_factory=list)
    contains_invalid_jumpdest: bool = False


@dataclass
class CodeAnalysis:
    num_push_bytes = 0
    num_jumpdests = 0
    num_invalid_jumpdests = 0
    chunks: List[Chunk] = field(default_factory=list)


def analyse_code(code) -> CodeAnalysis:
    analysis = CodeAnalysis()
    chunks = analysis.chunks
    pushdata_remaining = 0
    for i, op in enumerate(code):
        offset = i % CHUNK_LEN
        if offset == 0:
            chunks.append(Chunk(first_instruction_offset=pushdata_remaining))

        ch = chunks[len(chunks) - 1]

        if pushdata_remaining > 0:
            analysis.num_push_bytes += 1
            if op == JUMPDEST:
                analysis.num_invalid_jumpdests += 1
                ch.contains_invalid_jumpdest = True
            pushdata_remaining -= 1
        else:
            if PUSH1 <= op <= PUSH32:
                pushdata_remaining = op - PUSH1 + 1
            elif op == JUMPDEST:
                analysis.num_jumpdests += 1
                ch.jumpdests.append(offset)

    return analysis


def test_first_instruction_offset():
    def _(s):
        return [ch.first_instruction_offset for ch in analyse_code(bytes.fromhex(s)).chunks]

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
        return [ch.contains_invalid_jumpdest for ch in analyse_code(bytes.fromhex(s)).chunks]

    assert _('') == []
    assert _('00') == [False]
    assert _('605b') == [True]
    assert _('00' * 32 + '63dddd5bdd') == [False, True]
    assert _('00' * 31 + '60' + '605b') == [False, False]


def test_first_jumpdest_offset():
    def _(s):
        return [ch.jumpdests for ch in analyse_code(bytes.fromhex(s)).chunks]

    assert _('') == []
    assert _('00') == [[]]
    assert _('5b') == [[0]]
    assert _('005b') == [[1]]
    assert _('005b005b00') == [[1, 3]]
    assert _('615b5b5b') == [[3]]
    assert _('00' * 31 + '5b') == [[31]]
    assert _('00' * 32 + '5b') == [[], [0]]
    assert _('00' * 32 + '005b') == [[], [1]]
    assert _('00' * 32 + '605b') == [[], []]
    assert _('00' * 32 + '605b5b5b') == [[], [2, 3]]
    assert _('7f' + '5b' * 31 + '605b') == [[], [1]]
    assert _('7f' + '5b' * 31 + '605b605b60605b') == [[], [1, 6]]


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


def analyse_top_bytecodes():
    with open('top_bytecodes.json') as f:
        data = json.load(f)
    print(len(data))

    total_l = 0
    total_d = 0
    total_j = 0
    total_v = 0

    for row in data:
        code = bytes.fromhex(row["code"][2:])
        analysis = analyse_code(code)
        l = len(code)
        d = analysis.num_push_bytes
        j = analysis.num_jumpdests
        v = analysis.num_invalid_jumpdests
        print(f"{row['example_address']}, {l}, {(l + 31) // 32}:")
        print(
            f"{d} ({d / l:.3}) {j} ({j / l:.3}) {v} ({v / l:.3})")
        for i, ch in enumerate(analysis.chunks):
            if ch.contains_invalid_jumpdest:
                print(f"  {i:4}, {ch.first_instruction_offset:4}, {ch.jumpdests}")

        total_l += l
        total_d += d
        total_j += j
        total_v += v

    print(f"total: {total_l} {total_d} ({total_d/total_l:.3}) {total_j} ({total_j/total_l:.3}) {total_v} ({total_v/total_l:.3}, {total_v/total_d:.3})")


if __name__ == '__main__':
    analyse_top_bytecodes()

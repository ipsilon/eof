import csv
import json
from collections import defaultdict
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


@dataclass
class Operation:
    skip_only: bool
    chunk_delta: int
    fio: int


def transform_to_operation(invalid_jumpdests: list[Chunk]) -> list[Operation]:
    operations = []
    last_chunk_no = 0

    for i, ch in enumerate(invalid_jumpdests):
        if not ch.contains_invalid_jumpdest:
            continue  # skip chunks without invalid jumpdests

        # Chunk delta compared to last encoded number.
        chunk_delta = i - last_chunk_no

        # Generate skips if needed.
        while chunk_delta > 15:
            d = min(chunk_delta, 1023)
            operations.append(Operation(True, d, 0))
            chunk_delta -= d

        last_chunk_no = i

        assert (chunk_delta <= 15)
        assert (0 <= ch.first_instruction_offset <= 32)
        operations.append(Operation(False, chunk_delta, ch.first_instruction_offset))

    return operations


def perc(x, t):
    if x == 0:
        return "0"
    return f"{x * 100 / t:.2f}%"


def analyse_top_bytecodes():
    with open('top_bytecodes.json') as f:
        data = json.load(f)

    w = [['example address', 'earliest block', 'latest block', 'gas used', 'code length',
          'code chunks', 'push bytes', 'jumpdests', 'invalid jumpdests', 'scheme1 (1,10,4+6)'], []]

    earliest_block = 1_000_000_000
    latest_block = 0
    total_gas = 0
    total_l = 0
    total_d = 0
    total_j = 0
    total_v = 0

    total_encoding_len = 0
    encoding_dist = defaultdict(int)
    fio_dist = [0] * 33
    fio_dist_adj = [0] * 33
    for row in data:
        code = bytes.fromhex(row["code"][2:])
        analysis = analyse_code(code)
        l = len(code)
        num_code_chunks = (l + 31) // 32
        d = analysis.num_push_bytes
        j = analysis.num_jumpdests
        v = analysis.num_invalid_jumpdests

        print(f"{row['example_address']}, {l}, {num_code_chunks}:")
        print(
            f"{d} ({d / l:.3}) {j} ({j / l:.3}) {v} ({v / l:.3})")
        last_i = 0
        for i, ch in enumerate(analysis.chunks):
            if ch.contains_invalid_jumpdest:
                fio_dist[ch.first_instruction_offset] += 1
                fio_dist_adj[ch.first_instruction_offset if len(ch.jumpdests) > 0 else 32] += 1
                print(f"  {i:4}, {i - last_i:4}, {ch.first_instruction_offset:4}, {ch.jumpdests}")
                last_i = i

        ops = transform_to_operation(analysis.chunks)
        encoding_bits = len(ops) * 11
        encoding_len = (encoding_bits + 7) // 8
        total_encoding_len += encoding_len
        encoding_dist[encoding_len] += 1
        print(f"encoding: {encoding_bits}, {encoding_len}, {(encoding_len + 31) // 32}")
        # for op in ops:
        #     print(f"{op}")

        w.append(
            [row['example_address'], row['earliest_block'], row['latest_block'], row['gas_used'], l,
             num_code_chunks, perc(d, l), perc(j, l), perc(v, l), encoding_len])

        earliest_block = min(earliest_block, row['earliest_block'])
        latest_block = max(latest_block, row['latest_block'])
        total_gas += row['gas_used']
        total_l += l
        total_d += d
        total_j += j
        total_v += v

    print(
        f"total: {total_l} {total_d} ({total_d / total_l:.3}) {total_j} ({total_j / total_l:.3}) {total_v} ({total_v / total_l:.3}, {total_v / total_d:.3})")

    print("\nfio distribution:")
    for x, v in enumerate(fio_dist):
        print(f"{x:4}: {v}")
    print("\nfio adjusted distribution:")
    for x, v in enumerate(fio_dist_adj):
        print(f"{x:4}: {v}")
    print(f"\nencoding length distribution: {total_encoding_len}")
    for k, v in sorted(encoding_dist.items()):
        print(f"{k}: {v}")

    w[1] = ['total', earliest_block, latest_block, total_gas, total_l, (total_l + 31) // 32,
            perc(total_d, total_l), perc(total_j, total_l), perc(total_v, total_l),
            total_encoding_len]

    with open('code_analysis.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in w:
            writer.writerow(row)


if __name__ == '__main__':
    analyse_top_bytecodes()

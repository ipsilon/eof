import csv
import json
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
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
    num_push1_zeros = 0
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
                if op == PUSH1 and code[i + 1] == 0:
                    analysis.num_push1_zeros += 1
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


class Scheme:
    VALUE_MAX = 32
    VALUE_WIDTH = VALUE_MAX.bit_length()
    VALUE_MOD = VALUE_MAX + 1

    def __init__(self, name: str, width: int):
        self.name = name
        self.WIDTH = width

        payload_max = 2 ** (width - 1) - 1

        self.SKIP_ONLY = 1 << (self.WIDTH - 1)
        self.VALUE_SKIP_MAX = (payload_max - self.VALUE_MAX) // self.VALUE_MOD
        self.SKIP_BIAS = self.VALUE_SKIP_MAX + 1

    def encode_entry(self, delta: int, value: int) -> list[int]:
        assert 0 <= value <= self.VALUE_MAX
        skip_only_max = self.SKIP_ONLY - 1
        ops = []

        # Generate skips if needed.
        while delta > self.VALUE_SKIP_MAX:
            d = min(delta - self.SKIP_BIAS, skip_only_max)
            assert 0 <= d <= skip_only_max
            ops.append(self.SKIP_ONLY | d)
            delta -= d + self.SKIP_BIAS

        assert 0 <= delta <= self.VALUE_SKIP_MAX
        encoded = delta * self.VALUE_MOD + value
        assert encoded.bit_length() <= self.WIDTH
        ops.append(encoded)
        return ops

    def encode(self, chunks: dict[int, int]) -> tuple[list[int], int]:
        ops = []
        last_chunk_index = 0
        for i, fio in chunks.items():
            delta = i - last_chunk_index
            ops += self.encode_entry(delta, fio)
            last_chunk_index = i

        return ops, self.WIDTH * len(ops)

    def decode(self, ops: list[int]) -> dict[int, int]:
        m = dict()
        i = 0
        for op in ops:
            if op & self.SKIP_ONLY:
                delta = (op ^ self.SKIP_ONLY) + self.SKIP_BIAS
                value = None
            else:
                delta = op // self.VALUE_MOD
                value = op % self.VALUE_MOD
            i += delta
            print(f"{delta:+4}")
            if value is not None:
                m[i] = value
                print(f"{i:4}: {value}")
        return m


def test_scheme_consecutive():
    sch = Scheme("", 10)
    assert sch.WIDTH == 10
    assert sch.VALUE_SKIP_MAX == 14

    chunks = {0: 1, 1: 2, 2: 3}
    ops, _ = sch.encode(chunks)
    assert ops[0] == 0 * sch.VALUE_MOD + 1
    assert ops[1] == 1 * sch.VALUE_MOD + 2
    assert ops[2] == 1 * sch.VALUE_MOD + 3

    assert sch.decode(ops) == chunks


def test_scheme_skip_one():
    sch = Scheme("", 8)
    assert sch.VALUE_SKIP_MAX == 2

    chunks = {0: 1, 2: 3}
    ops, _ = sch.encode(chunks)
    assert ops[0] == 0 * sch.VALUE_MOD + 1
    assert ops[1] == 2 * sch.VALUE_MOD + 3

    assert sch.decode(ops) == chunks


def test_scheme_skip_first():
    sch = Scheme("", 8)

    chunks = {1: 2, 2: 3}
    ops, _ = sch.encode(chunks)
    assert ops[0] == 1 * sch.VALUE_MOD + 2
    assert ops[1] == 1 * sch.VALUE_MOD + 3

    assert sch.decode(ops) == chunks


def test_scheme_sparse_values():
    sch = Scheme("", 8)
    gap = [Chunk(0, [], False)]

    chunks = {0: 1, 2: 2, 4: 3}
    ops, _ = sch.encode(chunks)
    assert ops[0] == 0 * sch.VALUE_MOD + 1
    assert ops[1] == 2 * sch.VALUE_MOD + 2
    assert ops[2] == 2 * sch.VALUE_MOD + 3

    assert sch.decode(ops) == chunks


def test_scheme_skip_entry_0():
    sch = Scheme("", 8)

    chunks = {0: 1, 130: 3}
    ops, _ = sch.encode(chunks)
    assert ops[0] == 0 * sch.VALUE_MOD + 1
    assert ops[1] == sch.SKIP_ONLY + 127
    assert ops[2] == 0 * sch.VALUE_MOD + 3

    assert sch.decode(ops) == chunks


def test_scheme_skip_entry_2():
    sch = Scheme("", 8)
    uc = [Chunk(0, [], False)]
    chunks = {0: 1, 132: 3}
    ops, _ = sch.encode(chunks)
    assert ops[0] == 0 * sch.VALUE_MOD + 1
    assert ops[1] == sch.SKIP_ONLY + 127
    assert ops[2] == 2 * sch.VALUE_MOD + 3

    assert sch.decode(ops) == chunks


def test_scheme_skip_entry_minimal():
    sch = Scheme("", 8)

    chunks = {3: 1}
    ops, _ = sch.encode(chunks)
    assert ops[0] == sch.SKIP_ONLY + 0
    assert ops[1] == 0 * sch.VALUE_MOD + 1

    assert sch.decode(ops) == chunks


def test_scheme_double_skip_entry():
    sch = Scheme("", 8)

    chunks = {0: 1, 262: 3}
    ops, _ = sch.encode(chunks)
    assert ops[0] == 0 * sch.VALUE_MOD + 1
    assert ops[1] == sch.SKIP_ONLY + 130 - sch.SKIP_BIAS
    assert ops[2] == sch.SKIP_ONLY + 130 - sch.SKIP_BIAS
    assert ops[3] == 2 * sch.VALUE_MOD + 3

    assert sch.decode(ops) == chunks


def test_scheme_skip_entry_first_0():
    sch = Scheme("", 8)

    chunks = {130: 3}
    ops, _ = sch.encode(chunks)
    assert ops[0] == sch.SKIP_ONLY + 127
    assert ops[1] == 0 * sch.VALUE_MOD + 3

    assert sch.decode(ops) == chunks


def test_scheme_skip_entry_first_1():
    sch = Scheme("", 8)

    chunks = {131: 3}
    ops, _ = sch.encode(chunks)
    assert ops[0] == sch.SKIP_ONLY + 127
    assert ops[1] == 1 * sch.VALUE_MOD + 3

    assert sch.decode(ops) == chunks


def test_scheme_skip_entry_first_2():
    sch = Scheme("", 8)

    chunks = {132: 3}
    ops, _ = sch.encode(chunks)
    assert ops[0] == sch.SKIP_ONLY + 127
    assert ops[1] == 2 * sch.VALUE_MOD + 3

    assert sch.decode(ops) == chunks


def test_scheme_double_skip_entry_first():
    sch = Scheme("", 8)

    chunks = {262: 3}
    ops, _ = sch.encode(chunks)
    assert ops[0] == sch.SKIP_ONLY + 130 - sch.SKIP_BIAS
    assert ops[1] == sch.SKIP_ONLY + 130 - sch.SKIP_BIAS
    assert ops[2] == 2 * sch.VALUE_MOD + 3

    assert sch.decode(ops) == chunks


def analyze_encoding(scheme: Scheme, chunks: list[Chunk]) -> int:
    invalid_jumpdests = {}
    for i, ch in enumerate(chunks):
        if ch.contains_invalid_jumpdest:
            invalid_jumpdests[i] = ch.first_instruction_offset

    operations, length = scheme.encode(invalid_jumpdests)
    m = scheme.decode(operations)
    assert m == invalid_jumpdests
    return length


def perc(x, t):
    if x == 0:
        return "0"
    return f"{x * 100 / t:.2f}%"


SCHEMES = [
    Scheme("scheme f11", 11),
    Scheme("scheme f10", 10),
    Scheme("scheme f9", 9),
    Scheme("scheme f8", 8),
]


def analyse_top_bytecodes(dataset_file: Path, result_file: Path):
    with open(dataset_file) as f:
        data = json.load(f)

    w = [['example address', 'earliest block', 'latest block', 'gas used',
          'code length', 'code chunks', 'push bytes', 'PUSH1 zeros', 'jumpdests',
          'invalid jumpdests']
         + [s.name for s in SCHEMES], []]

    earliest_block = 1_000_000_000
    latest_block = 0
    total_gas = 0
    total_l = 0
    total_d = 0
    total_z = 0
    total_j = 0
    total_v = 0

    total_encoding_len = [0] * len(SCHEMES)
    encoding_dist = [defaultdict(int)] * len(SCHEMES)
    fio_dist = [0] * 33
    fio_dist_adj = [0] * 33
    for row in data:
        code = bytes.fromhex(row["code"][2:])
        analysis = analyse_code(code)
        l = len(code)
        num_code_chunks = (l + 31) // 32
        d = analysis.num_push_bytes
        z = analysis.num_push1_zeros
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

        w.append(
            [row['example_address'], row['earliest_block'], row['latest_block'], row['gas_used'], l,
             num_code_chunks, perc(d, l), perc(z, l), perc(j, l), perc(v, l)])

        for i, sch in enumerate(SCHEMES):
            encoding_bits = analyze_encoding(sch, analysis.chunks)
            encoding_len = (encoding_bits + 7) // 8
            total_encoding_len[i] += encoding_len
            encoding_dist[i][encoding_len] += 1
            print(f"encoding: {encoding_bits}, {encoding_len}, {(encoding_len + 31) // 32}")
            w[-1].append(encoding_len)

        earliest_block = min(earliest_block, row['earliest_block'])
        latest_block = max(latest_block, row['latest_block'])
        total_gas += row['gas_used']
        total_l += l
        total_d += d
        total_z += z
        total_j += j
        total_v += v
        # break

    print(
        f"total: {total_l} {total_d} ({total_d / total_l:.3}) {total_j} ({total_j / total_l:.3}) {total_v} ({total_v / total_l:.3}, {total_v / total_d:.3})")

    # print("\nfio distribution:")
    # for x, v in enumerate(fio_dist):
    #     print(f"{x:4}: {v}")
    # print("\nfio adjusted distribution:")
    # for x, v in enumerate(fio_dist_adj):
    #     print(f"{x:4}: {v}")
    print(f"\nencoding length distribution: {total_encoding_len}")
    # for k, v in sorted(encoding_dist.items()):
    #     print(f"{k}: {v}")

    w[1] = ['total', earliest_block, latest_block, total_gas, total_l, (total_l + 31) // 32,
            perc(total_d, total_l), perc(total_z, total_l), perc(total_j, total_l),
            perc(total_v, total_l)] + total_encoding_len

    with open(result_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in w:
            writer.writerow(row)


if __name__ == '__main__':
    assert len(sys.argv) >= 2, "missing argument: dataset file"

    dataset_file = Path(sys.argv[1])
    result_file = dataset_file.with_stem(dataset_file.stem + "_analysis").with_suffix(".csv")

    analyse_top_bytecodes(dataset_file, result_file)

# This implements "Scheme 1".

from dataclasses import dataclass

MAX_CHUNK_VALUE_DELTA = 32
MAX_CHUNK_SKIP_DELTA = 1024 # 2^10-1

@dataclass
class InvalidJumpdest:
    pos: int
    fio: int # First instruction offset

@dataclass
class Operation:
    skip_only: bool
    chunk_delta: int
    fio: int

def transform_to_operation(jumpdests: list[InvalidJumpdest]) -> list[Operation]:
    operations = []
    last_chunk_no = 0

    for entry in jumpdests:
        print(entry)
    
        # Chunk number of current entry.
        chunk_no = entry.pos // 32

        assert(entry.pos - (chunk_no * 32) + entry.fio <= 32)

        # Chunk delta compared to last encoded number.
        chunk_delta = chunk_no - last_chunk_no
        print("Chunk", last_chunk_no,  chunk_no, chunk_delta)

        # Generate skips if needed.
        while chunk_delta > 31:
            # Too large chunks can only be skipped.
            while chunk_delta > 1023:
                operations.append(Operation(True, 1023, 0))
                chunk_delta -= 1023

            operations.append(Operation(True, 31, 0))
            chunk_delta -= 31

        last_chunk_no = chunk_no

        assert(chunk_delta <= 31)
        assert(entry.fio <= 31)
        operations.append(Operation(False, chunk_delta, entry.fio))

    return operations

def compress_invalid_jumpdest_list(jumpdests: list[InvalidJumpdest] = []) -> bytes:
    print("Invalid jumpdests", jumpdests)

    # Transform to operation list.
    operations = transform_to_operation(jumpdests)
    print("Operations", operations)
    
    # Encode operation.
    # We collect statistics instead
    total_bits = 0
    for entry in operations:
        if entry.skip_only:
            total_bits += 1 + 10
        else:
            total_bits += 1 + 4 + 6
    print("Total header size", total_bits, (total_bits + 7) // 8)
    
    # TODO actually encode it
    return bytes()

compress_invalid_jumpdest_list([InvalidJumpdest(0, 0), InvalidJumpdest(0, 2), InvalidJumpdest(31, 1), InvalidJumpdest(32, 31), InvalidJumpdest(128, 1)])

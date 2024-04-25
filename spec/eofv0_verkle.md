# EOFv0 for packaging legacy code in Verkle Trees

The design draft that proposes the use of EOF
for storing code in Verkle Trees.
An alternative to the existing method of executing
31-byte code chunks accompanied by 1 byte of metadata.

## Goal

Simplified legacy code execution in the Verkle Tree implementation.

Better "code-to-data" ratio.

Provide the result of the jumpdest analysis of a deployed code as the EOF section.
During code execution the jumpdest analysis is already available
and the answer to the question "is this jump target valid?" can be looked up
in the section. This allows using 32-byte Verkle Tree code chunks
(instead of 31-byte of code + 1 byte of metadata).

## Specification

### Container

1. Re-use the EOF container format defined by [EIP-3540](https://eips.ethereum.org/EIPS/eip-3540).
2. Set the EOF version to 0. I.e. the packaged legacy code will be referenced as EOFv0.
3. The EOFv0 consists of the header and two sections:
    - *jumpdest*
    - *code*
4. The header must contain information about the sizes of these sections.
   For that the EIP-3540 header or a simplified one can be used.
5. The legacy code is placed in the *code* section without modifications.
6. The *jumpdest* section contains the set of all valid jump destinations matching the positions
   of all `JUMPDEST` instructions in the *code*.
   The exact encoding of this section is specified separately.

### Changes to execution semantics

1. Execution starts at the first byte of the *code* section, and `PC` is set to 0.
2. Execution stops if `PC` goes outside the code section bounds (in case of EOFv0 this is also the
   end of the container).
3. `PC` returns the current position within the *code*.
4. The instructions which *read* code must refer to the *code* section only. 
   The modification keeps the behavior of these instructions unchanged.
   These instructions are invalid in EOFv1.
   The instructions are:
    - `CODECOPY` (copies a part of the *code* section),
    - `CODESIZE` (returns the size of the *code* section),
    - `EXTCODECOPY`,
    - `EXTCODESIZE`,
    - `EXTCODEHASH`.
5. To execute a `JUMP` or `JUMPI` instruction the jump target position must exist
   in the *jumpdest* set. The *jumpdest* guarantees that the target instruction is `JUMPDEST`.

### Changes to contract creation semantics

1. Initcode execution is performed without changes. I.e. initcode remains an ephemeral code
   without EOF wrapping. However, because the EOF containers are not visible to any EVM program,
   implementations may decide to wrap initcodes with EOFv0 and execute it the same way as
   EOFv0 deployed codes.
2. The initcode size limit and cost remains defined by [EIP-3860](https://eips.ethereum.org/EIPS/eip-3860).
3. The initcode still returns a plain deploy code.
   The plain code size limit and cost is defined by [EIP-170](https://eips.ethereum.org/EIPS/eip-170).
4. If the plain code is not empty, it must be wrapped with EOFv0 before put in the state:
    - perform jumpdest analysis of the plain code,
    - encode the jumpdest analysis result as the *jumpdest* section,
    - put the plain code in the *code* section,
    - create EOFv0 container with the *jumpdest* and *code* sections.
5. The code deployment cost is calculated from the total EOFv0 size.
   This is a breaking change so the impact must be analysed.
6. During Verkle Tree migration perform the above EOFv0 wrapping of all deployed code.

### Jumpdest section encoding

#### Bitmap

A valid `JUMPDEST` is represented as `1` in a byte-aligned bitset.
The tailing zero bytes must be trimmed.
Therefore, the size of the bitmap is at most `ceil(len(code) / 8)` giving ~12% size overhead
(comparing with plain code size).
Such encoding doesn't require pre-processing and provides random access.

Originally, the EIP-3690 proposes to use delta encoding for the elements of the *jumpdest* section.
This should be efficient for an average contract but behaves badly in the worst case
(every instruction in the code is a `JUMPDEST`).
The delta encoding has also another disadvantage for Verkle Tree code chunking:
whole (?) section must be loaded and preprocessed to check a single jump target validity.

### Metadata encoding (8-bit numbers)

Follow the original Verkle Tree idea to provide the single byte of metadata with the
"number of leading pushdata bytes in a chunk".
However, instead of including this in the chunk itself,
place the byte in order in the *jumpdest* section.

This provides the following benefits over the original Verkle Tree design:

1. The code executes by full 32-byte chunks.
2. The *metadata* size overhead slightly smaller: 3.1% (`1/32`) instead of 3.2% (`1/31`).
3. The *metadata* lookup is only needed for executing jumps
   (not needed when following through to the next chunk).

### Super-dense metadata encoding (6-bit numbers)

The same as above except encode the values as 6-bit numbers
(minimum number of bits needed for encoding `32`).
Such encoding lowers the size overhead from 3.1% to 2.3%.

### Encode only invalid pushdata (dense encoding)

Alternate option is instead of encoding all valid `JUMPDEST` locations, to only encode invalid ones.

This is beneficial if our assumption is correct that most contracts only contain a limited number
of offending cases. Our initial analysis suggests this is the case, e.g. Uniswap router has 9 cases,
one of the Arbitrum validator contracts has 6 cases.

Since Solidity contracts have a trailing metadata, which contains a Keccak-256 (32-byte) hash of the
source, there is a 12% probability ($1 - (255/256)^{32}$) that at least one of the bytes of the hash
will contain the `0x5b` value, which gives our minimum probability of having at least one invalid `JUMPDEST`.

Let's create a map of `invalid_jumpdests[chunk_no] = position_in_chunk`. We can densely encode this
map using techniques similar to *run-length encoding* to skip distances and delta-encode offsets.

In *scheme 1*, for each entry in `invalid_jumpdests`:
- 1-bit mode (`skip`, `value`)
- For skip-mode:
  - 10-bit delta-encoding of `chunk_no`
- For value-mode:
  - 4-bit delta-encoding of `chunk_no`
  - 6-bit `position_in_chunk`

Worst case encoding where each chunk contains an invalid `JUMPDEST`:
```
total_chunk_count = 24576 / 32 = 768
total_chunk_count * (1 + 4 + 6) / 8 = 1056 # bytes for the header
number_of_verkle_leafs = total_chunk_count / 32 = 33
```

*Scheme 2* differs slightly:
- 1-bit mode (`skip`, `value`)
- For skip-mode:
  - 10-bit delta-encoding of `chunk_no`
- For value-mode:
  - 6-bit `position_in_chunk`

Worst case encoding:
```
total_chunk_count = 24576 / 32 = 768
total_chunk_count * (1 + 6) / 8 = 672 # bytes for the header
number_of_verkle_leafs = total_chunk_count / 32 = 21
```

The decision between *scheme 1* and *scheme 2*, as well as the best encoding sizes, can be determined
through analysing existing code.

#### Header location

It is possible to place above as part of the "EOFv0" header, but given the upper bound of number of chunks occupied is low (33 vs 21),
it is also possible to make this part of the Verkle account header.

This second option allows for the simplification of the `code_size` value, as it does not need to change.

#### Runtime after Verkle

During runtime execution two checks must be done in this order:
1) Check if the destination is on the invalid list, and abort if so.
2) Check if the value in the chunk is an actual `JUMPDEST`, and abort if not.

It is possible to reconstruct sparse account code prior to execution with all the submitted chunks of the transaction
and perform `JUMPDEST`-validation to build up a relevant *valid `JUMPDEST` locations* map instead.

#### Analysis

We have analyzed two contracts, Arbitrum validator and Uniswap router.

Arbitrum (2147-bytes long):
```
(chunk offset, chunk number, pushdata offset)
malicious push byte: 85 2 21
malicious push byte: 95 2 31
malicious push byte: 116 3 20
malicious push byte: 135 4 7
malicious push byte: 216 6 24
malicious push byte: 1334 41 22
```

Encoding with *scheme 1*:
```
[skip, 2]
[value, 0, 21]
[value, 0, 31]
[value, 1, 20]
[value, 1, 7]
[value, 2, 24]
[skip, 35, 22]
```

Encoding size: `2 skips (2 * 11 bits) + 5 values (5 * 11 bits)` = 10-bytes header (0.465%)

Encoding with *scheme 2*:
```
[skip, 2]
[value, 21]
[value, 31]
[skip, 1]
[value, 20]
[skip, 1]
[value, 7]
[skip, 2]
[value, 24]
[skip, 35]
[value, 22]
```

Encoding size: `5 skips (5 * 11 bits) + 6 values (6 * 7 bits)` = 13-bytes header (0.605%)

Uniswap router contract (17958 bytes):

```
(chunk offset, chunk number, pushdata offset)
malicious push byte: 1646 51 14
malicious push byte: 1989 62 5
malicious push byte: 4239 132 15
malicious push byte: 4533 141 21
malicious push byte: 7043 220 3
malicious push byte: 8036 251 4
malicious push byte: 8604 268 28
malicious push byte: 12345 385 25
malicious push byte: 15761 492 17
```

Encoding using *scheme 1*:
```
[skip, 51]
[value, 0, 14]
[value, 11, 5]
[skip, 70]
[value, 0, 15]
[value, 9, 21]
[skip, 79]
[value, 0, 3]
[skip, 31]
[value, 0, 4]
[skip, 17]
[value, 0, 28]
[skip, 117]
[value, 0, 25]
[skip, 107]
[value, 0, 17]
```

Encoding size: `7 skips (7 * 11 bits) + 9 values (9 * 11 bits)` = 22-bytes header (0.122%)

## Backwards Compatibility

EOF-packaged code execution if fully compatible with the legacy code execution.
This is achieved by prepending the legacy code with EOF header and the section containing
jumpdest metadata. The contents of the code section is identical to the lagacy code.

Moreover, the wrapping process is bidirectional: wrapping can be created from the legacy code
and legacy code extracted from the wrapping without any information loss.
Implementations may consider keeping the legacy code in the database without modifications
and only construct the EOF wrapping when loading the code from the database.

It also can be noted that information in the *jumpdest* section is redundant to the `JUMPDEST`
instructions. However, we **cannot** remove these instructions from the code because
this potentially breaks:

- *dynamic* jumps (where we will not be able to adjust their jump targets),
- code introspection with `CODECOPY` and `EXTCODECOPY`.

## Extensions

### Detect unreachable code

The bitmap encoding has a potential of omitting contract's tailing data from the *jumpdest* section
provided there are no `0x5b` bytes in the data.

We can extend this capability by trying to detect unreachable code
(e.g. contract's metadata, data or inicodes and deploy codes for `CREATE` instructions).
For this we require a heuristic that does not generate any false positives.

One interesting example is a "data" contract staring with a terminating instruction
(e.g. `STOP`, `INVALID` or any unassigned opcode).

There are new risks this method introduces.

1. Treating unassigned opcodes as terminating instructions prevents them
   from being assigned to a new instruction.
2. The heuristic will be considered by compilers optimizing for code size.

### Prove jump targets are valid

#### Prove all "static jumps"

By "static jump" we consider a jump instruction directly preceded by a `PUSH` instruction.

In the solidity generated code all `JUMPI` instructions and 85% of `JUMP` instructions are "static".
(these numbers must be verified on bigger sample of contracts).

We can easily validate all static jumps and mark a contracts with "all static jumps valid"
at deploy time. Then at runtime static jumps can be executed without accessing jumpdest section.

#### Prove all jumps

If we can prove that all jump targets in the code are valid,
then there is no need for the *jumpdest* section.

Erigon project has a
[prototype analysis tool](https://github.com/ledgerwatch/erigon/blob/devel/cmd/hack/flow/flow.go#L488)
which is able to prove all jump validity for 95+% of contracts.


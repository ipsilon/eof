# EOFv0 for packaging legacy code in Verkle Trees

The design draft that proposes the use of EOF
for storing code in Verkle Trees.
An alternative to the existing method of executing
31-byte code chunks accompanied by 1 byte of metadata.

## Goal

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
4. The instructions which *read* code must refer to the *code* section only. This is significantly
   different from what the original EIP-3540 proposed, however this difference is not relevant
   in the latest EOFv1 revision where these instructions are invalid.
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
2. The initcode size limit remains defined by [EIP-3860](https://eips.ethereum.org/EIPS/eip-3860).
3. The initcode still returns a plain deploy code.
   The plain code size limit is defined by [EIP-170](https://eips.ethereum.org/EIPS/eip-170).
4. The plain code is not empty it must be wrapped with EOFv0 before put in the state:
    - perform jumpdest analysis of the plain code,
    - encode the jumpdest analysis result as the *jumpdest* section,
    - put the plain code in the *code* section,
    - create EOFv0 container with the *jumpdest* and *code* sections.
5. The code deployment cost is calculated from the total EOFv0 size.
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
2. The *metadata* size overhead slightly smaller `1/32` instead of `1/31`.
3. The *metadata* lookup is only needed for executing jumps
   (not needed when following through to the next chunk).

### Super-dense metadata encoding (6-bit numbers)

The same as above except encode the values as 6-bit numbers
(minimum number of bits needed for encoding `32`).
Such encoding lowers the size overhead from 3.1% to 2.3%.

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

### Prove all jump targets are valid

If we can prove that all jump targets in the code are valid,
then there is no need for the *jumpdest* section.

In the solidity generated code all `JUMPI` instructions are "static"
(preceded by a `PUSH` instruction).
Only some `JUMP` instructions are not "static" because they are used to implement
returns from functions.

Erigon project has a
[prototype analysis tool](https://github.com/ledgerwatch/erigon/blob/devel/cmd/hack/flow/flow.go#L488)
which is able to prove all jump validity for 95+% of contracts.


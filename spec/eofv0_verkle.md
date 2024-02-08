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

## Specification Draft

1. Put the code in the single *code* EOF section.
2. Use the EOF container format proposed by [EIP-3540](https://eips.ethereum.org/EIPS/eip-3540) with
   version 0 and following modifications to "Changes to execution semantics":
    1. `CODECOPY`/`CODESIZE`/`EXTCODECOPY`/`EXTCODESIZE`/`EXTCODEHASH` operates on the *code*
       section only.
    2. `JUMP`/`JUMPI`/`PC` relates code positions to the *code* section only.
3. Perform the jumpdest analysis of the code at deploy time (during contract creation).
4. Store the result of the jumpdest analysis in the *jumpdest* EOF section as proposed
   by [EIP-3690](https://eips.ethereum.org/EIPS/eip-3690),
   but the jumpdests encoding changed to bitmap.
5. The packaging process is done for every deployed code during Verkle Tree migration
   and also for every contract creation later
   (i.e. becomes the part of the consensus forever).

##  Backwards Compatibility

EOF-packaged code execution if fully compatible with the legacy code execution.
This is achieved by prepending the legacy code with EOF header and the section containing
jumpdest metadata. The contents of the code section is identical to the lagacy code.

Moreover, the wrapping process is bidirectional: wrapping can be created from the legacy code
and legacy code extracted from the wrapping without any information loss.
Implementations may consider keeping the legacy code in the database without modifications
and only construct the EOF wrapping when loading the code from the database.

It also can be noted that information in the *jumpdest* section is redundant to the `JUMPDEST`
instructions. However, we cannot remove these instructions from the code because
this would break at least *dynamic* jumps (where we will not be able to adjust their jump targets).

## Rationale

### Jumpdests encoding

Originally, the EIP-3690 proposes to use delta encoding for the elements of the *jumpdest* section.
This should be efficient for an average contract but behaves badly in the worst case
(every instruction in the code is a `JUMPDEST`).
The delta encoding has also another disadvantage for Verkle Tree code chunking:
whole (?) section must be loaded and preprocessed to check a jump target validity.

We propose to use a bitmap to encode jumpdests.
Such encoding does not need pre-processing and provides random access.
This gives constant 12.5% size overhead, but does not have the two mentioned disadvantages.

## Extensions

### Data section

Let's try to identify a segment of code at the end of the code where a contract stores data.
We require a heuristic that does not generate any false positives.
This arrangement ensures that the instructions inspecting the code
work without modifications on the continuous *code*+*data* area

Having a *data* section makes the *code* section and therefore the *jumpdest* section smaller.

Example heuristic:

1. Decode instructions.
2. Traverse instructions in reverse order.
3. If during traversal a terminating instruction (`STOP`, `INVALID`, etc)
   or the code beginning is encountered,
   then the *data* section starts just after the current position.
   End here.
4. If during traversal a `JUMPDEST` instruction is encountered,
   then there is no *data* section.
   End here.

### Prove all jump targets are valid

If we can prove that all jump targets in the code are valid,
then there is no need for the *jumpdest* section.

In the solidity generated code all `JUMPI` instructions are "static"
(preceded by a `PUSH` instruction).
Only some `JUMP` instructions are not "static" because they are used to implement
returns from functions.

Erigon project had an analysis tool which was able to prove all jump validity
for 90+% of contracts.

### Super-dense metadata encoding (6-bit numbers)

Follow the original Verkle Tree idea to provide the metadata of
"number of leading pushdata bytes in a chunk". However, instead of including
this metadata as a single byte in the chunk itself, place the value as a 6-bit
encoded number in the *metadata* EOF section. This provides the following benefits:

1. The code executes by full 32-byte chunks.
2. The *metadata* overhead is smaller (2.3% instead of 3.2%).
3. The *metadata* lookup is only needed for jumps
   (not needed when following through to the next chunk).

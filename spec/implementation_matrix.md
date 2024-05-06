# Readiness matrix

|              |    3540 |      3670 | 4200 | 4750 | 5450 | 6206 | 7480 | 7069 | 7620     | 663   |
|--------------|---------|-----------|------|------|------|------|------|------|----------|-------|
| **Megaspec** | :+1:    | :+1:      | :+1: | :+1: | :+1: | :+1: | :+1: | :+1: | :+1:     | :+1:  |
| **EIP**      | :+1:    | :+1:      | :+1: | :+1: | :+1: | :+1: | :+1: | :+1: | :+1:     | :+1:  |
| **testing**  | :+1:    | :+1:      | :+1: | :+1: | :+1: | 🚧   | 🚧   | :+1: | :+1:     |  🚧   |
| besu         | :+1:    | :+1:      | :+1: | :+1: | :+1: | :+1: | :+1: | :+1: | :+1:     | :+1:  |
| erigon       |         |           |      |      |      |      |      |      |          |       |
| ethereumjs   |         |           |      |      |      |      |      |      |          |       |
| evmone       | :+1:    | :+1:      | :+1: | :+1: | :+1: | :+1: | :+1: | :+1: | 🚧       | :+1:  |
| geth         | 🚧      | 🚧         | 🚧   | 🚧   | 🚧    | 🚧   | 🚧   | 🚧    | 🚧       | 🚧    |
| nethermind   |         |           |      |      |      |      |      |      |          |       |
| revm         | :+1:    |  :+1:     | :+1: | :+1: |  🚧  | :+1: | :+1: |  🚧  |  🚧      | :+1:  |
| solidity     | 🚧      | N/A       | 🚧   | 🚧   | N/A  |      |      |      |          |       |
| vyper        |         |           |      |      |      |      |      |      |          |       |

# Specs

## Megaspec

[**Megaspec**](./eof.md) is ready and main source of truth.

- Alternative version without an irregular state change is discussed: https://github.com/ipsilon/eof/pull/78

## EIP updates in progress 🚧

EIP contents are being updated to match up with the **Megaspec**:

- **EIP-7620** - ethereum/EIPs#8358 (mostly clarifications)
- **EIP-7620** - irregular state change discussion pending, to be filed after https://github.com/ipsilon/eof/pull/78 concludes

# Implementations

## Besu

Currently EOF is in a branch [mega-eof](https://github.com/hyperledger/besu/tree/mega-eof)

# Column Descriptions

* EIP-3540 - EOF Container
  * Validation
    * https://github.com/ethereum/tests/tree/develop/EOFTests/EIP3540
    * https://github.com/ethereum/tests/tree/develop/EOFTests/ori
  * Execution - https://github.com/ethereum/tests/tree/develop/EIPTests/StateTests/stEOF/stEIP3540
  * Legacy->EOF `EXTCODE*` state tests generated from evmone unit tests - https://github.com/ipsilon/tests/tree/eof-create3-evmone-generated/EIPTests/StateTests/stEOF/extcode

* EIP-3670 - Code Validation
  * Validation - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP3670
  * Validation tests generated from evmone unit tests - https://github.com/ethereum/tests/tree/develop/EOFTests/efValidation
    * these cover validation rules from all EIPs

* EIP-4200 - Static Relative Jumps
  * Validation - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP4200
  * Execution - https://github.com/ethereum/tests/tree/develop/EIPTests/StateTests/stEOF/stEIP4200

* EIP-4750 - Functions
  * Validation - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP4750
  * Execution - https://github.com/ethereum/tests/tree/develop/EIPTests/StateTests/stEOF/stEIP4750

* EIP-5450 - Stack Validation
  * Validation - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP5450
  * Execution - https://github.com/ethereum/tests/tree/develop/EIPTests/StateTests/stEOF/stEIP5450
  * Validation tests generated from evmone unit tests - https://github.com/ethereum/tests/tree/develop/EOFTests/efStack

* EIP-6206 - JUMPF and non-returning functions

* EIP-7480 - Data section access
  * Execution - https://github.com/ethereum/execution-spec-tests/pull/518

* EIP-7069 - Revamped CALL instructions
  * `EXT*CALL` state tests generated from evmone unit tests - https://github.com/ipsilon/tests/tree/eof-create3-evmone-generated/EIPTests/StateTests/stEOF/eof_calls

* EIP-7620 - EOF Create Instructions
  * Creation state tests generated from evmone unit tests - https://github.com/ipsilon/tests/tree/eof-create3-evmone-generated/EIPTests/StateTests/stEOF/stCreate

* EIP-663 - SWAPN/DUPN/EXCHANGE
  * Execution - https://github.com/ethereum/execution-spec-tests/pull/502

## geth

Current work-in-progress implementation resides at: https://github.com/ethereum/go-ethereum/pull/29518

## Solidity

Last implementation resides at https://github.com/ethereum/solidity/pull/13825.  This is based on the December 2022 version of EOF.

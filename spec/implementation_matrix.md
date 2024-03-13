# Readiness matrix

|              |    3540 |      3670 | 4200 | 4750 | 5450 | 6206 | 7480 | 7069 | 7620     | 663   |
|--------------|---------|-----------|------|------|------|------|------|------|----------|-------|
| **Megaspec** | :+1:    | :+1:      | :+1: | :+1: | :+1: | :+1: | :+1: | :+1: | :+1:     |  :+1: |
| **EIP**      | 🚧      | :+1:      | :+1: | 🚧   | 🚧   | :+1: | :+1:  | 🚧  | :+1:     |  :+1: |
| **testing**  | :x:     | :x:       |      |      |      |      |      |      |          |       |
| besu         | :+1:    | :+1:      | :+1: | :+1: | :+1: | :+1: | :+1: | :+1: | 🚧        | :+1:  |
| erigon       |         |           |      |      |      |      |      |      |          |       |
| ethereumjs   |         |           |      |      |      |      |      |      |          |       |
| evmone       | :+1:    | :+1:      | :+1: | :+1: | :+1: | :+1: | :+1: | 🚧   | 🚧       | 🚧    |
| geth         |         |           |      |      |      |      |      |      |          |       |
| nethermind   |         |           |      |      |      |      |      |      |          |       |
| revm         | 🚧      |           | :+1: | :+1: |      | :+1: | :+1: |      |  🚧      | :+1:  |
| solidity     |         |           |      |      |      |      |      |      |          |       |
| vyper        |         |           |      |      |      |      |      |      |          |       |

# Specs

## Megaspec

[**Megaspec**](./eof.md) is ready and main source of truth.

## EIP updates in progress 🚧

EIP contents are being updated to match up with the **Megaspec**:

- **EIP-3540** - ethereum/EIPs#8152
- **EIP-7069** - ethereum/EIPs#8287

# Implementations

## Besu

Currently EOF is in a branch [mega-eof](https://github.com/hyperledger/besu/tree/mega-eof)


# Column Descriptions

* EIP-3540 - EOF Container
  * Validation
    * https://github.com/ethereum/tests/tree/develop/EOFTests/EIP3540
    * https://github.com/ethereum/tests/tree/develop/EOFTests/ori
  * Execution - https://github.com/ethereum/tests/tree/develop/EIPTests/StateTests/stEOF/stEIP3540

* EIP-3670 - Code Validation
  * Validation - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP3670
  * Validation tests generated from evmone unit tests - https://github.com/ipsilon/tests/tree/evmone-eof-validation-tests/EOFTests/eof_validation
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
  * Validation tests generated from evmone unit tests - https://github.com/ipsilon/tests/tree/evmone-eof-validation-tests/EOFTests/eof_validation/stack

* EIP-6206 - JUMPF and non-returning functions

* EIP-7480 - Data section access

* EIP-7069 - Revamped CALL instructions

* EIP-7620 - EOF Create Instructions
  * Creation state tests generated from evmone unit tests - https://github.com/ipsilon/tests/tree/eof-create3-evmone-generated/EIPTests/StateTests/stEOF/stCreate

* EIP-663 - SWAPN/DUPN/EXCHANGE

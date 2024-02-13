# Readiness matrix

|              |    3540 |      3670 | 4200 | 4750 | 5450 | 6206 | 7480 | 7069 | 7620     | 663   |
|--------------|---------|-----------|------|------|------|------|------|------|----------|-------|
| **Megaspec** | :+1:    | :+1:      | :+1: | :+1: | :+1: | :+1: | :+1: | :+1: | :+1:     |  :+1: |
| **EIP**      | 🚧      | stale     | stale| stale| stale| :+1: | :+1:  | :+1:| :+1      | 🚧    |
| **testing**  | :x:     | :x:       |      |      |      |      |      |      |          |       |
| besu         | 477/758 | 1262/1374 | :+1: | :+1: | :+1: |      |      |      |          |       |
| erigon       |         |           |      |      |      |      |      |      |          |       |
| ethereumjs   |         |           |      |      |      |      |      |      |          |       |
| evmone       | :+1:    | :+1:      | :+1: | :+1: | 🚧   | :+1: | :+1: | 🚧   | 🚧       | 🚧    |
| geth         |         |           |      |      |      |      |      |      |          |       |
| nethermind   |         |           |      |      |      |      |      |      |          |       |
| reth         |         |           |      |      |      |      |      |      |          |       |
| solidity     |         |           |      |      |      |      |      |      |          |       |
| vyper        |         |           |      |      |      |      |      |      |          |       |

# Specs

## Megaspec

[**Megaspec**](./eof.md) is ready and main source of truth.

## EIP updates in progress

EIP contents are being updated to match up with the **Megaspec**:

- ethereum/EIPs#7819
- ethereum/EIPs#8152

# Implementations

## Besu

Currently EOF is in a branch [mega-eof](https://github.com/hyperledger/besu/tree/mega-eof)


# Column Descriptions

* EIP-3540 - EOF Container
  * Execution Validation (758 tests) - https://github.com/ethereum/tests/tree/develop/EIPTests/StateTests/stEOF/stEIP3540

* EIP-3670 - Code Validation
  * Execution Validation (1374 tests) - https://github.com/ethereum/tests/tree/develop/EIPTests/StateTests/stEOF/stEIP3540

* EIP-4200 - Static Relative Jumps
  * Container Validation (54 tests) - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP4200
  * Execution Validation (27 tests) - https://github.com/ethereum/tests/tree/develop/EIPTests/StateTests/stEOF/stEIP4200

* EIP-4750 - Functions
  * Container Validation (29 tests) - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP4750
  * Execution Validation (4 tests) - https://github.com/ethereum/tests/tree/develop/EIPTests/StateTests/stEOF/stEIP4750

* EIP-5450 - Stack Validation
  * Container Validation (202 tests) - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP5450
  * Execution Validation (2 tests) - https://github.com/ethereum/tests/tree/develop/EIPTests/StateTests/stEOF/stEIP5450

* EIP-6206 - JUMPF and non-returning functions

* EIP-7480 - Data section access

* EIP-7069 - Revamped CALL instructions

* EIP-TBD - EOF Create Instructions

* EIP-663 - SWAPN/DUPN/EXCHANGE

# Readiness matrix

|                     | [3540] | [3670] | [4200] | [4750] | [5450] | [6206] | [7480] | [7069] | [7620] | [7698] | [663] |
|---------------------|--------|--------|-------|-------|--------|-------|-------|--------|-------|--------|-------|
| **Megaspec**        | :+1:   | :+1:   | :+1:  | :+1:  | :+1:   | :+1:  | :+1:  | :+1:   | :+1:  | :+1:   | :+1:  |
| **EIP**             | :+1:   | :+1:   | :+1:  | :+1:  | :+1:   | :+1:  | :+1:  | :+1:   | :+1:  | :+1:   | :+1:  |
| **testing**         | :+1:   | :+1:   | :+1:  | :+1:  | :+1:   | 🚧    | 🚧    | :+1:   | :+1:  |        |  🚧   |
| besu                | :+1:   | :+1:   | :+1:  | :+1:  | :+1:   | :+1:  | :+1:  | :+1:   | :+1:  |        | :+1:  |
| erigon              |        |        |       |       |        |       |       |        |       |        |       |
| erigon++ (silkworm) | :+1:   | :+1:   | :+1:  | :+1:  | :+1:   | :+1:  | :+1:  | :+1:   | :+1:  | 🚧     | :+1:  |
| ethereumjs          | stale  | stale  | stale | stale | stale  |       |       |        |       |        |       |
| evmone              | :+1:   | :+1:   | :+1:  | :+1:  | :+1:   | :+1:  | :+1:  | :+1:   | :+1:  | 🚧     | :+1:  |
| geth                | 🚧     | 🚧     | 🚧    | 🚧    | 🚧     | 🚧    | 🚧    | 🚧     | 🚧    |        | 🚧     |
| nethermind          | 🚧     | 🚧     | 🚧    | 🚧    | 🚧     | 🚧    | 🚧    | 🚧     | 🚧    |        | 🚧     |
| revm                | :+1:   | :+1:   | :+1:  | :+1:  | 🚧     | :+1:  | :+1:  | 🚧     | 🚧    |        | :+1:  |
| [solidity POC]      | :+1:     | N/A    | 🚧    | :+1:  | N/A    |   :+1:  |   :+1:  | :+1:   | :+1:  | :+1:     |       |
| vyper               | stale  | N/A    | stale | stale | N/A    |       |       |        |       |        |       |

[solidity POC]: https://github.com/ipsilon/solidity/tree/eof-functions-rebased/libsolidity
[3540]: https://eips.ethereum.org/EIPS/eip-3540
[3670]: https://eips.ethereum.org/EIPS/eip-3670
[4200]: https://eips.ethereum.org/EIPS/eip-4200
[4750]: https://eips.ethereum.org/EIPS/eip-4750
[5450]: https://eips.ethereum.org/EIPS/eip-5450
[6206]: https://eips.ethereum.org/EIPS/eip-6206
[7480]: https://eips.ethereum.org/EIPS/eip-7480 
[7069]: https://eips.ethereum.org/EIPS/eip-7069 
[7620]: https://eips.ethereum.org/EIPS/eip-7620 
[7698]: https://eips.ethereum.org/EIPS/eip-7698 
[663]: https://eips.ethereum.org/EIPS/eip-663

# Specs

## Megaspec

[**Megaspec**](./eof.md) is ready and main source of truth.

Pending updates addressing recent feedback:

- **A tweak to the EOF validation of creation opcodes** - https://github.com/ipsilon/eof/pull/86

## EIP updates in progress

EIP contents are being updated to match up with the **Megaspec**:

- **EIP-7620** - ethereum/EIPs#8522 (Remove TXCREATE, InitcodeTransaction and the Creator Contract)

# Implementations

## Besu

Currently EOF is in a branch [mega-eof](https://github.com/hyperledger/besu/tree/mega-eof).

## erigon++

[Erigon++ is a version of Erigon using Silkworm as the execution engine.](https://erigon.tech/erigonpp/) Since Silkworm uses evmone, it receives the feature from upstream.

## ethereumjs

Ethereumjs in 2022 has merged the initial EOF EIPs into mainline, and then worked on the late 2022 version in [PR#2453](https://github.com/ethereumjs/ethereumjs-monorepo/pull/2453). This code can be considered stale.

## geth

Current work-in-progress implementation resides at: https://github.com/ethereum/go-ethereum/pull/29518

## Nethermind

Nethermind currently has EOF support in the branch [feature/evm/eof](https://github.com/NethermindEth/nethermind/commits/feature/evm/eof/)  ([PR#6896](https://github.com/NethermindEth/nethermind/pull/6896)).

## Solidity

Last implementation resides at https://github.com/ethereum/solidity/pull/13825.  This is based on the December 2022 version of EOF.

## Vyper

There is a contributor submitted PR from mid 2023 implementing some of EOF: https://github.com/vyperlang/vyper/pull/3457

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

* EIP-7698 - EOF - Creation transaction

* EIP-663 - SWAPN/DUPN/EXCHANGE
  * Execution - https://github.com/ethereum/execution-spec-tests/pull/502

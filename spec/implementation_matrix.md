# Readiness matrix

|                       | [3540] | [3670] | [4200]  | [4750] | [5450] | [6206] | [7480] | [7069] | [7620] | [7698] | [663] |
|-----------------------|--------|--------|---------|--------|--------|--------|--------|--------|--------|--------|-------|
| [**Megaspec**]        | 👍     | 👍     | 👍      | 👍     | 👍     | 👍     | 👍     | 👍     | 👍     | 👍     | 👍    |
| **EIP**               | 👍     | 👍     | 👍      | 👍     | 👍     | 👍     | 👍     | 👍     | 👍     | 👍     | 👍    |
| **testing**           | 👍     | 👍     | 👍      | 👍     | 👍     | 👍     | 🚧     | 🚧     | 🚧     |        | 👍    |
| [besu]                | 👍     | 👍     | 👍      | 👍     | 👍     | 👍     | 👍     | 👍     | 👍     | 👍      | 👍   |
| erigon                | 🚧     | 🚧     | 🚧      | 🚧     | 🚧     | 🚧     | 🚧     |        |        |        | 🚧    |
| [ethereumjs]          | 🚧     | 🚧     | 🚧      | 🚧     | 🚧     | 🚧     | 🚧     | 🚧     | 🚧     | 🚧     | 🚧    |
| [evmone]              | 👍     | 👍     | 👍      | 👍     | 👍     | 👍     | 👍     | 👍     | 👍     | 👍     | 👍    |
| [geth]                | 🚧     | 🚧     | 🚧      | 🚧     | 🚧     | 🚧     | 🚧     | 🚧     | 🚧     |        | 🚧    |
| [nethermind]          | 👍     | 👍     | 👍      | 👍     | 👍     | 👍     | 👍     | 👍     | 👍     | 👍      | 👍   |
| revm                  | 👍     | 👍     | 👍      | 👍     | 👍     | 👍     | 👍     | 👍     | 👍     | 👍     | 👍    |
| [solidity POC]        | 👍     | N/A    | 👍      | 👍     | N/A    | 👍     | 👍     | 👍     | 👍     | 👍     |       |
| [vyper]               | 🚧     | N/A    | 🚧      | 🚧     | N/A    |        |        |        |        |        |       |
| [EELS]                | 👍     | 👍     | 👍      | 👍     | 👍     | 👍     | 👍     | 👍     | 👍     | 👍      | 👍   |

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

[**Megaspec**]: https://github.com/ipsilon/eof/blob/main/spec/eof.md
[besu]: https://github.com/hyperledger/besu/tree/mega-eof
[ethereumjs]: https://github.com/ethereumjs/ethereumjs-monorepo/pull/3440
[evmone]: https://github.com/ethereum/evmone
[geth]: https://github.com/ethereum/go-ethereum/pull/29518
[nethermind]: https://github.com/NethermindEth/nethermind/commits/feature/evm/eof
[solidity POC]: https://github.com/ipsilon/solidity/tree/eof-functions-rebased/libsolidity
[vyper]: https://github.com/vyperlang/vyper/pull/3457
[EELS]: https://github.com/ethereum/execution-specs/pull/972

## Testing readiness matrix

|                                                      | [besu] |  erigon  | [ethereumjs] | [evmone] | [geth] | [nethermind] |  revm  | [EELS] |
|------------------------------------------------------|--------|----------|--------------|----------|--------|--------------|--------|--------|
| \[\*\] [EEST] `eip7692@v1.1.0` - `state_tests`       | ✅     | ✅       |              | ✅       |        | ✅            | ✅     | ✅     |
| \[\*\] [EEST] `eip7692@v1.1.0` - `eof_tests`         | ✅     | ✅       |              | ✅       |        | ✅            | ✅     | ✅     |
| [EEST] `eip7692@v2.0.0` - `state_tests`              |        |          |              |          |        |              |        |        |
| [EEST] `eip7692@v2.0.0` - `eof_tests`                |        |          |              |          |        |              |        |        |
| [tests] `v14.1` - `EIPTests/StateTests/stEOF`        | ✅     |          |              | ✅       |        |              | ✅     | ✅     |
| [tests] `v14.1` - `EOFTests`                         | ✅     |          |              | ✅       |        |              | ✅     | ✅     |
| \[\*\] [`evmone` exported] `v0.12.0` - `state_tests` | ✅     |          |              | ✅       |        |              | ✅     | ✅     |
| \[\*\] [`evmone` exported] `v0.12.0` - `eof_tests`   | ✅     |          |              | ✅       |        |              | ✅     | ✅     |
| [`evmone` exported] `v0.13.0` - `state_tests`        | ❓     |          |              | ✅       |        |              | ✅     | ✅     |
| [`evmone` exported] `v0.13.0` - `eof_tests`          | ❓     |          |              | ✅       |        |              | ✅     | ✅     |

[EEST]: https://github.com/ethereum/execution-spec-tests/releases/
[tests]: https://github.com/ethereum/tests/releases/
[`evmone` exported]: https://github.com/ethereum/evmone/releases/ 

\[\*\] **NOTE:** old version, will be dropped once clients report back with recent version passing.

# Specs

## Megaspec

[**Megaspec**](./eof.md) is ready and main source of truth.

## EIPs

Are aligned with the Megaspec, Meta EOF EIP at https://eips.ethereum.org/EIPS/eip-7692.

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

## EELS
There is a draft PR with some of the EIPs implemented. The other EIPs are in progress and will be built on top: https://github.com/ethereum/execution-specs/pull/972

# Column Descriptions

* EIP-3540 - EOF Container
  * Validation
    * https://github.com/ethereum/tests/tree/develop/EOFTests/EIP3540
    * https://github.com/ethereum/tests/tree/develop/EOFTests/ori
  * https://github.com/ethereum/execution-spec-tests/tree/main/tests/osaka/eip7692_eof_v1/eip3540_eof_v1

* EIP-3670 - Code Validation
  * Validation - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP3670
  * Validation tests generated from evmone unit tests - https://github.com/ethereum/tests/tree/develop/EOFTests/efValidation
    * these cover validation rules from all EIPs

* EIP-4200 - Static Relative Jumps
  * Validation - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP4200
  * https://github.com/ethereum/execution-spec-tests/tree/main/tests/osaka/eip7692_eof_v1/eip4200_relative_jumps

* EIP-4750 - Functions
  * Validation - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP4750
  * https://github.com/ethereum/execution-spec-tests/tree/main/tests/osaka/eip7692_eof_v1/eip4750_functions

* EIP-5450 - Stack Validation
  * Validation - https://github.com/ethereum/tests/tree/develop/EOFTests/EIP5450
  * Validation tests generated from evmone unit tests - https://github.com/ethereum/tests/tree/develop/EOFTests/efStack
  * https://github.com/ethereum/execution-spec-tests/tree/main/tests/osaka/eip7692_eof_v1/eip5450_stack

* EIP-6206 - JUMPF and non-returning functions
  * https://github.com/ethereum/execution-spec-tests/tree/main/tests/osaka/eip7692_eof_v1/eip6206_jumpf

* EIP-7480 - Data section access
  * https://github.com/ethereum/execution-spec-tests/tree/main/tests/osaka/eip7692_eof_v1/eip7480_data_section

* EIP-7069 - Revamped CALL instructions
  * https://github.com/ethereum/execution-spec-tests/tree/main/tests/osaka/eip7692_eof_v1/eip7069_extcall

* EIP-7620 - EOF Create Instructions
  * https://github.com/ethereum/execution-spec-tests/tree/main/tests/osaka/eip7692_eof_v1/eip7620_eof_create

* EIP-7698 - EOF - Creation transaction
  * https://github.com/ethereum/execution-spec-tests/tree/main/tests/osaka/eip7692_eof_v1/eip7698_eof_creation_tx

* EIP-663 - SWAPN/DUPN/EXCHANGE
  * https://github.com/ethereum/execution-spec-tests/tree/main/tests/osaka/eip7692_eof_v1/eip663_dupn_swapn_exchange

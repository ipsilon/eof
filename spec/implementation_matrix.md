# Readiness matrix

|                | [eof-devnet-0]           | [eof-devnet-1]       | eof-devnet-2 |
|----------------|--------------------------|----------------------|--------------|
| Megaspec       | ✅ [Megaspec v0.1.1]     | ✅ [Megaspec main]   | 🚧           |
| **EIP**        | ✅ [EIP-7692 `8580af`]   | ✅ [EIP-7692]        | 🚧           |
| **testing**    | ✅ [EEST eip7692@v2.3.0] | ✅ [EEST v4.3.0]     | 🚧           |
| [besu]         | ✅                       | ✅                   |              |
| [erigon]       | ✅                       |                      |              |
| [ethereumjs]   | ✅                       |                      |              |
| [evmone]       | ✅                       | ✅                   |              |
| [geth]         | ✅                       | ✅                   |              |
| [nethermind]   | ✅                       |                      |              |
| [revm]         | ✅                       |                      |              |
| [EELS]         | ✅                       |                      |              |
| [solidity]     | ✅                       |                      |              |
| [vyper]        |                          |                      |              |

**NOTE**: Compiling to EOF with [solidity] requires one to use the `--experimental-eof-version 1` flag, more details [here](https://soliditylang.org/blog/2025/03/12/solidity-0.8.29-release-announcement/)

[eof-devnet-0]: https://notes.ethereum.org/@ethpandaops/eof-devnet-0
[eof-devnet-1]: https://notes.ethereum.org/@ethpandaops/eof-devnet-1

[Megaspec v0.1.1]: https://github.com/ipsilon/eof/blob/v0.1.1/spec/eof.md
[Megaspec main]: https://github.com/ipsilon/eof/blob/main/spec/eof.md

[EIP-7692 `8580af`]: https://github.com/ethereum/EIPs/blob/8580af761332f72cdb8b90232d31e85c70f87423/EIPS/eip-7692.md
[EIP-7692]: https://eips.ethereum.org/EIPS/eip-7692

[EEST eip7692@v2.3.0]: https://github.com/ethereum/execution-spec-tests/releases/tag/eip7692%40v2.3.0
[EEST v4.3.0]: https://github.com/ethereum/execution-spec-tests/releases/tag/v4.3.0

[besu]: https://github.com/hyperledger/besu
[ethereumjs]: https://github.com/ethereumjs/ethereumjs-monorepo
[evmone]: https://github.com/ethereum/evmone
[geth]: https://github.com/shemnon/go-ethereum/tree/osaka-mega-eof
[nethermind]: https://github.com/NethermindEth/nethermind/commits/feature/evm/eof
[solidity]: https://github.com/ethereum/solidity
[vyper]: https://github.com/vyperlang/vyper/pull/3457
[EELS]: https://github.com/ethereum/execution-specs/tree/eips/osaka/eip-7692
[revm]: https://github.com/bluealloy/revm
[erigon]: https://github.com/erigontech/erigon

## Testing readiness matrix

|                                                      | [besu] |  [erigon]| [ethereumjs] | [evmone] | [geth] | [nethermind] |  [revm]  | [EELS] |
|------------------------------------------------------|--------|----------|--------------|----------|--------|--------------|----------|--------|
| [EEST] `v4.3.0` - `state_tests`                      | ✅     |          |              | ✅       | ✅     |              |          |        |
| [EEST] `v4.3.0` - `blockchain_tests`                 | ✅     |          |              | ✅       | ✅     |              |          |        |
| [EEST] `v4.3.0` - `eof_tests`                        | ✅     |          |              | ✅       | ✅     |              |          |        |
| [EEST] `eip7692@v2.3.0` - `state_tests`              | ✅     | ✅       |              | ✅       |        | ✅           | ✅       | ✅     |
| [EEST] `eip7692@v2.3.0` - `blockchain_tests`         | ✅     | ✅       |              | ✅       |        | ✅           |          | ✅     |
| [EEST] `eip7692@v2.3.0` - `eof_tests`                | ✅     | ✅       |              | ✅       |        | ✅           | ✅       | ✅     |
| \[\*\] [EEST] `eip7692@v2.2.0` - `state_tests`       |        | ✅       | ✅           | ✅       | ✅     | ✅           |          | ✅     |
| \[\*\] [EEST] `eip7692@v2.2.0` - `blockchain_tests`  |        | ✅       | ✅           | ✅       | ✅     | ✅           |          | ✅     |
| \[\*\] [EEST] `eip7692@v2.2.0` - `eof_tests`         |        | ✅       | ✅           | ✅       | ✅     | ✅           |          | ✅     |
| \[\*\] [tests] `v14.1` - `EIPTests/StateTests/stEOF` | ✅     |          |              | ✅       |        |              | ✅       | ✅     |
| [tests] `v14.1` - `EOFTests`                         | ✅     |          |              | ✅       |        |              | ✅       | ✅     |
| [`evmone` exported] `v0.13.0` - `state_tests`        | ❓     |          |              | ✅       |        |              | ✅       | ✅     |
| [`evmone` exported] `v0.13.0` - `eof_tests`          | ❓     |          |              | ✅       |        |              | ✅       | ✅     |

[EEST]: https://github.com/ethereum/execution-spec-tests/releases/
[tests]: https://github.com/ethereum/tests/releases/
[`evmone` exported]: https://github.com/ethereum/evmone/releases/ 

\[\*\] **NOTE:** old version, will be dropped once clients report back with recent version passing.
**NOTE:** [EEST eip7692@v2.3.0] release follows [eof-devnet-0] spec
**NOTE:** [EEST v4.3.0] release follows [eof-devnet-1] spec


# Specs

## Megaspec

[**Megaspec**](./eof.md) is ready and main source of truth.

## EIPs

Are aligned with the Megaspec, Meta EOF EIP at https://eips.ethereum.org/EIPS/eip-7692.

# Implementation forks & branches

## erigon++

[Erigon++ is a version of Erigon using Silkworm as the execution engine.](https://erigon.tech/erigonpp/) Since Silkworm uses evmone, it receives the feature from upstream.

## geth

Current work-in-progress implementation resides in a fork at: https://github.com/shemnon/go-ethereum/tree/osaka-mega-eof

## Nethermind

Nethermind currently has EOF support in the branch [feature/evm/eof](https://github.com/NethermindEth/nethermind/commits/feature/evm/eof/)  ([PR#8176](https://github.com/NethermindEth/nethermind/pull/8176)).

## Solidity

Current work-in-progress implementation split into PRs at: https://github.com/ethereum/solidity/pulls?q=is%3Aopen+is%3Apr+label%3AEOF

## Vyper

There is a contributor submitted PR from mid 2023 implementing some of EOF: https://github.com/vyperlang/vyper/pull/3457

## EELS

The WIP implementation of EOF on EELS can be found here: https://github.com/ethereum/execution-specs/tree/eips/osaka/eip-7692

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

# Designs for future upgrade of EOFv1

**This document gathers the designs which were excluded from the [Mega EOF spec](./eof.md), i.e. will not be a part of the first EOF release. They are planned to be introduced in a future upgrade.**

# `TXCREATE` and `InitcodeTransaction`

## Transaction Types

Introduce new transaction type `InitcodeTransaction` which extends EIP-1559 (type 2) transaction by adding a new field `initcodes: List[ByteList[MAX_INITCODE_SIZE], MAX_INITCODE_COUNT]`.

The `initcodes` can only be accessed via the `TXCREATE` instruction (see below), therefore `InitcodeTransactions` are intended to be sent to contracts including `TXCREATE` in their execution.

Under transaction validation rules `initcodes` are not validated for conforming to the EOF specification. They are only validated when accessed via `TXCREATE`. This avoids potential DoS attacks of the mempool. If during the execution of an `InitcodeTransaction` no `TXCREATE` instruction is called, such transaction is still valid.

`initcodes` data is similar to calldata for two reasons:
1) It must be fully transmitted in the transaction.
2) It is accessible to the EVM, but it can't be fully loaded into EVM memory.

For these reasons, define cost of each of the `initcodes` items same as calldata (16 gas for non-zero bytes, 4 for zero bytes -- see EIP-2028). The intrinsic gas of an `InitcodeTransaction` is extended by the sum of all those items' costs.

EIP-3860 and EIP-170 still apply, i.e. `MAX_CODE_SIZE` as 24576, `MAX_INITCODE_SIZE` as `2 * MAX_CODE_SIZE`. Define `MAX_INITCODE_COUNT` as 256.

`InitcodeTransaction` is invalid if either:
- there are more than `MAX_INITCODE_COUNT` entries in `initcodes`
- `initcodes` is an empty array
- length of any entry in `initcodes` exceeds `MAX_INITCODE_SIZE`
- any entry in `initcodes` has zero length
- the `to` is `nil`

#### RLP and signature

Given the definitions from [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718) the `TransactionPayload` for an `InitcodeTransaction` is the RLP serialization of:

```
[chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, to, value, data, access_list, initcodes, y_parity, r, s]
```

`TransactionType` is `INITCODE_TX_TYPE` (`0x04`) and the signature values `y_parity`, `r`, and `s` are calculated by constructing a secp256k1 signature over the following digest:

```
keccak256(INITCODE_TX_TYPE || rlp([chain_id, nonce, max_priority_fee_per_gas, max_fee_per_gas, gas_limit, to, value, data, access_list, initcodes]))
```

The [EIP-2718](https://eips.ethereum.org/EIPS/eip-2718) `ReceiptPayload` for this transaction is `rlp([status, cumulative_transaction_gas_used, logs_bloom, logs])`.

### New Behavior

- `TXCREATE (0xed)` instruction
    - Works the same as `EOFCREATE` except:
        - does not have `initcontainer_index` immediate
        - pops one more value from the stack (first argument): `tx_initcode_hash`
        - loads the initcode EOF container from the transaction `initcodes` array which hashes to `tx_initcode_hash`
            - fails (returns 0 on the stack) if such initcode does not exist in the transaction, or if called from a transaction of `TransactionType` other than `INITCODE_TX_TYPE`
                - caller's nonce is not updated and gas for initcode execution is not consumed. Only `TXCREATE` constant gas was consumed
            - let `initcontainer_size` be the length of that EOF container in bytes
        - in addition to hashing charge as in `EOFCREATE`, deducts `2 * ((initcontainer_size + 31) // 32)` gas (EIP-3860 charge)
        - just before executing the initcode container:
            - **validates the initcode container and all its subcontainers recursively**
            - validation includes checking that the container is an "initcode" container as defined in the validation section, that is, it does not contain `RETURN` or `STOP`
            - in addition to this, checks if the initcode container has its `len(data_section)` equal to `data_size`, i.e. data section content is exactly as the size declared in the header (see [Data section lifecycle](#data-section-lifecycle))
            - fails (returns 0 on the stack) if any of those was invalid
                - caller’s nonce is not updated and gas for initcode execution is not consumed. Only `TXCREATE` constant, EIP-3860 gas and hashing gas were consumed

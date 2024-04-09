# "Mega EOF Endgame" Specification (EOFv1)

![EOF logo](./assets/eof_logo.png)

## Preface

**This document describes all the changes which we previously dicussed titles as EOF 1.1 and EOF 2.0. Those changes do not have an EIP yet.**

This unified specification should be used as a guide to understand the various changes the EVM Object Format is proposing. The individual EIPs ~~still remain the official specification and should confusion arise those are to be consulted~~ are not fully updated yet, and this document serves as a main source of truth at the moment. See appendix for the original list of EIPs.

While EOF is extensible, in this document we discuss the first version, EOFv1.

## Container

EVM bytecode is traditionally an unstructured sequence of instructions. EOF introduces the concept of a container, which brings structure to byte code. The container consists of a header and then several sections.

```
container := header, body
header := 
    magic, version, 
    kind_types, types_size, 
    kind_code, num_code_sections, code_size+,
    [kind_container, num_container_sections, container_size+,]
    kind_data, data_size,
    terminator
body := types_section, code_section+, container_section*, data_section
types_section := (inputs, outputs, max_stack_height)+
```

_note: `,` is a concatenation operator, `+` should be interpreted as "one or more" of the preceding item, and `*` should be interpreted as "zero or more" of the preceding item._

#### Header

| name              | length   | value  | description |
|-------------------|----------|---------------|-------------|
| magic             | 2 bytes  | 0xEF00        | EOF prefix  |
| version           | 1 byte   | 0x01          | EOF version |
| kind_types        | 1 byte   | 0x01          | kind marker for types size section |
| types_size        | 2 bytes  | 0x0004-0xFFFF | 16-bit unsigned big-endian integer denoting the length of the type section content |
| kind_code         | 1 byte   | 0x02          | kind marker for code size section |
| num_code_sections | 2 bytes  | 0x0001-0xFFFF | 16-bit unsigned big-endian integer denoting the number of the code sections |
| code_size         | 2 bytes  | 0x0001-0xFFFF | 16-bit unsigned big-endian integer denoting the length of the code section content |
| kind_container    | 1 byte   | 0x03          | kind marker for container size section |
| num_container_sections | 2 bytes  | 0x0001-0x00FF | 16-bit unsigned big-endian integer denoting the number of the container sections |
| container_size    | 2 bytes  | 0x0001-0xFFFF | 16-bit unsigned big-endian integer denoting the length of the container section content |
| kind_data         | 1 byte   | 0x04          | kind marker for data size section |
| data_size         | 2 bytes  | 0x0000-0xFFFF | 16-bit unsigned big-endian integer denoting the length of the data section content (for not yet deployed containers this can be more than the actual content, see [Data Section Lifecycle](#data-section-lifecycle))|
| terminator        | 1 byte   | 0x00          | marks the end of the header |

#### Body

| name          | length   | value  | description |
|---------------|----------|---------------|-------------|
| types_section | variable | n/a           | stores code section metadata |
| inputs        | 1 byte | 0x00-0x7F       | number of stack elements the code section consumes |
| outputs       | 1 byte | 0x00-0x80       | number of stack elements the code section returns or 0x80 for non-returning functions |
| max_stack_height | 2 bytes | 0x0000-0x03FF | maximum number of elements ever placed onto the stack by the code section |
| code_section  | variable | n/a           | arbitrary sequence of bytes |
| container_section | variable | n/a       | arbitrary sequence of bytes |
| data_section  | variable | n/a           | arbitrary sequence of bytes |

### Data Section Lifecycle

**For an EOF container which has not yet been deployed**, the `data_section` is only a portion of the final `data_section` after deployment.
Let's define it as `pre_deploy_data_section` and as `pre_deploy_data_size` the `data_size` declared in that container's header.
`pre_deploy_data_size >= len(pre_deploy_data_section)`, which anticipates more data to be appended to the `pre_deploy_data_section` during the process of deploying.

```
pre_deploy_data_section
|                                       |
 \___________pre_deploy_data_size______/
```

**For a deployed EOF container**, the final `data_section` becomes:

```
pre_deploy_data_section | static_aux_data | dynamic_aux_data
|                         |             |                  |
|                          \___________aux_data___________/
|                                       |                  |
 \___________pre_deploy_data_size______/                   |
|                                                          |
 \________________________data_size_______________________/
```

where:
- `aux_data` is the data which is appended to `pre_deploy_data_section` on `RETURNCONTRACT` instruction [see New Behavior](#new-behavior).
- `static_aux_data` is a subrange of `aux_data`, which size is known before `RETURNCONTRACT` and equals `pre_deploy_data_size - len(pre_deploy_data_section)`.
- `dynamic_aux_data` is the remainder of `aux_data`.

`data_size` in the deployed container header is also updated to be equal `len(data_section)`.

Summarizing, there are `pre_deploy_data_size` bytes in the final data section which are guaranteed to exist before the EOF container is deployed and `len(dynamic_aux_data)` bytes which are known to exist only after.
This impacts the validation and behavior of data-section-accessing instructions: `DATALOAD`, `DATALOADN`, and `DATACOPY`, see [Code Validation](#code-validation).

### Container Validation

The following validity constraints are placed on the container format:

- minimum valid header size is `15` bytes
- `version` must be `0x01`
- `types_size` is divisible by `4`
- the number of code sections must be equal to `types_size / 4`
- the number of code sections must not exceed 1024
- `code_size` may not be 0
- the number of container sections must not exceed 256
- `container_size` may not be 0, but container sections are optional
- the total size of a deployed container without container sections must be `13 + 2*num_code_sections + types_size + code_size[0] + ... + code_size[num_code_sections-1] + data_size`
- the total size of a deployed container with at least one container section must be `16 + 2*num_code_sections + types_size + code_size[0] + ... + code_size[num_code_sections-1] + data_size + 2*num_container_sections + container_size[0] + ... + container_size[num_container_sections-1]`
- the total size of not yet deployed container might be up to `data_size` lower than the above values due to how the data section is rewritten and resized during deployment (see [Data Section Lifecycle](#data-section-lifecycle))

## Transaction Types

Introduce new transaction type `InitcodeTransaction` which extends EIP-1559 (type 2) transaction by adding a new field `initcodes: List[ByteList[MAX_INITCODE_SIZE], MAX_INITCODE_COUNT]`.

The `initcodes` can only be accessed via the `TXCREATE` instruction (see below), therefore `InitcodeTransactions` are intended to be sent to contracts including `TXCREATE` in their execution.

We introduce a standardised Creator Contract (i.e. written in EVM, but existing at a known address, such as precompiles), which eliminates the need to have create transactions with empty `to`. Deployment of the Creator Contract will require an irregular state change at EOF activation block. Note that such introduction of the Creator Contract is needed, because only EOF contracts can create EOF contracts. See the appendix below for Creator Contract code.

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

## Execution Semantics

Code executing within an EOF environment will behave differently than legacy code. We can break these differences down into i) changes to existing behavior and ii) introduction of new behavior.

### Modified Behavior

- Execution starts at the first byte of code section 0, and `pc` is set to 0.
- `pc` is scoped to the executing code section
- The instructions `CALL`, `CALLCODE`, `DELEGATECALL`, `STATICCALL`, `SELFDESTRUCT`, `JUMP`, `JUMPI`, `PC`, `CREATE`, `CREATE2`, `CODESIZE`, `CODECOPY`, `EXTCODESIZE`, `EXTCODECOPY`, `EXTCODEHASH`, `GAS` are deprecated and rejected by validation in EOF contracts. They are only available in legacy contracts.
- If the target account of `EXTCODECOPY` is an EOF contract, then it will copy up to 2 bytes from `EF00`, as if that would be the code.
- If the target account of `EXTCODEHASH` is an EOF contract, then it will return `0x9dbf3648db8210552e9c4f75c6a1c3057c0ca432043bd648be15fe7be05646f5` (the hash of `EF00`, as if that would be the code).
- If the target account of `EXTCODESIZE` is an EOF contract, then it will return 2.
- The instruction `JUMPDEST` is renamed to `NOP` and remains charging 1 gas without any effect.
    - Note: jumpdest-analysis is not performed anymore.
- EOF contract may not deploy legacy code (it is naturally rejected on the code validation stage)
- Legacy creation transactions (any tranactions with empty `to`) are invalid in case `data` contains EOF code (starts with `EF00` magic)
- If instructions `CREATE` and `CREATE2` have EOF code as initcode (starting with `EF00` magic)
    - deployment fails (returns 0 on the stack)
    - caller's nonce is not updated and gas for initcode execution is not consumed

**NOTE** Legacy contract and legacy creation transactions may not deploy EOF code, that is behavior from [EIP-3541](https://eips.ethereum.org/EIPS/eip-3541) is not modified.

### New Behavior

The following instructions are introduced in EOF code:

- `RJUMP (0xe0)` instruction
    - deduct 2 gas
    - read int16 operand `offset`, set `pc = offset + pc + 3`
- `RJUMPI (0xe1)` instruction
    - deduct 4 gas
    - pop one value, `condition` from stack
    - set `pc += 3`
    - if `condition != 0`, read int16 operand `offset` and set `pc += offset`
- `RJUMPV (0xe2)` instruction
    - deduct 4 gas
    - read uint8 operand `max_index`
    - pop one value, `case` from stack
    - set `pc += 2`
    - if `case > max_index` (out-of-bounds case), fall through and set `pc += (max_index + 1) * 2`
    - otherwise interpret 2 byte operand at `pc + case * 2` as int16, call it `offset`, and set `pc += (max_index + 1) * 2 + offset`
- introduce new vm context variables
    - `current_code_idx` which stores the actively executing code section index
    - new `return_stack` which stores the pairs `(code_section, pc)`.
        - when instantiating a vm context, push an initial value to the *return stack* of `(0,0)`
- `CALLF (0xe3)` instruction
    - deduct 5 gas
    - read uint16 operand `idx`
    - if `1024 < len(stack) + types[idx].max_stack_height - types[idx].inputs`, execution results in an exceptional halt
    - if `1024 <= len(return_stack)`, execution results in an exceptional halt
    - push new element to `return_stack` `(current_code_idx, pc+3)`
    - update `current_code_idx` to `idx` and set `pc` to 0
- `RETF (0xe4)` instruction
    - deduct 3 gas
    - pops `val` from `return_stack` and sets `current_code_idx` to `val.code_section` and `pc` to `val.pc`
- `JUMPF (0xe5)` instruction
    - deduct 5 gas
    - read uint16 operand `idx`
    - if `1024 < len(stack) + types[idx].max_stack_height - types[idx].inputs`, execution results in an exceptional halt
    - set `current_code_idx` to `idx`
    - set `pc = 0`
- `EOFCREATE (0xec)` instruction
    - deduct `32000` gas
    - read uint8 operand `initcontainer_index`
    - pops `value`, `salt`, `input_offset`, `input_size` from the stack
    - peform (and charge for) memory expansion using `[input_offset, input_size]`
    - load initcode EOF subcontainer at `initcontainer_index` in the container from which `EOFCREATE` is executed
    - deduct `6 * ((initcontainer_size + 31) // 32)` gas (hashing charge)
    - check call depth limit and whether caller balance is enough to transfer `value`
        - in case of failure returns 0 on the stack, caller's nonce is not updated and gas for initcode execution is not consumed.
    - copy memory starting at `input_offset` of `input_size` length into the call data
    - execute the container in "initcode-mode" and deduct gas for execution
        - increment `sender` account's nonce
        - calculate `new_address` as `keccak256(0xff || sender || salt || keccak256(initcontainer))[12:]`
        - an unsuccesful execution of initcode results in pushing `0` onto the stack
            - can populate returndata if execution `REVERT`ed
        - a successful execution ends with initcode executing `RETURNCONTRACT{deploy_container_index}(aux_data_offset, aux_data_size)` instruction (see below). After that:
            - load deploy EOF subcontainer at `deploy_container_index` in the container from which `RETURNCONTRACT` is executed
            - concatenate data section with `(aux_data_offset, aux_data_offset + aux_data_size)` memory segment and update data size in the header
            - if updated deploy container size exceeds `MAX_CODE_SIZE` instruction exceptionally aborts
            - set `state[new_address].code` to the updated deploy container
            - push `new_address` onto the stack
        - `RETURN` and `STOP` are not allowed in "initcode-mode" (abort execution)
        - "initcode-mode" _is not transitive_ - it is only active for the frame executing the initcontainer. If another (non-create) call is made from this frame, it _is not_ executed in "initcode-mode".
    - deduct `200 * deployed_code_size` gas
- `TXCREATE (0xed)` instruction
    - Works the same as `EOFCREATE` except:
        - does not have `initcontainer_index` immediate
        - pops one more value from the stack (first argument): `tx_initcode_hash`
        - loads the initcode EOF container from the transaction `initcodes` array which hashes to `tx_initcode_hash`
            - fails (returns 0 on the stack) if such initcode does not exist in the transaction, or if called from a transaction of `TransactionType` other than `INITCODE_TX_TYPE`
                - caller's nonce is not updated and gas for initcode execution is not consumed. Only `TXCREATE` constant gas was consumed
        - in addition to hashing charge as in `EOFCREATE`, deducts `2 * ((initcontainer_size + 31) // 32)` gas (EIP-3860 charge)
        - just before executing the initcode container:
            - **validates the initcode container and all its subcontainers recursively**
            - in addition to this, checks if the initcode container has its `len(data_section)` equal to `data_size`, i.e. data section content is exactly as the size declared in the header (see [Data section lifecycle](#data-section-lifecycle))
            - fails (returns 0 on the stack) if any of those was invalid
                - caller’s nonce is not updated and gas for initcode execution is not consumed. Only `TXCREATE` constant, EIP-3860 gas and hashing gas were consumed
- `RETURNCONTRACT (0xee)` instruction
    - loads `uint8` immediate `deploy_container_index`
    - pops two values from the stack: `aux_data_offset`, `aux_data_size` referring to memory section that will be appended to deployed container's data
    - cost 0 gas + possible memory expansion for aux data
    - ends initcode frame execution and returns control to `EOFCREATE` or `TXCREATE` caller frame where `deploy_container_index` and `aux_data` are used to construct deployed contract (see above)
    - instruction exceptionally aborts if after the appending, data section size would overflow the maximum data section size or underflow (i.e. be less than data section size declared in the header)
    - instruction exceptionally aborts if invoked not in "initcode-mode"
- `DATALOAD (0xd0)` instruction
    - deduct 4 gas
    - pop one value, `offset`, from the stack
    - read `[offset, offset+32]` from the data section of the active container and push the value to the stack
    - pad with 0s if reading out of data bounds
- `DATALOADN (0xd1)` instruction
    - deduct 3 gas
    - like `DATALOAD`, but takes the offset as a 16-bit immediate value and not from the stack
- `DATASIZE (0xd2)` instruction
    - deduct 2 gas
    - push the size of the data section of the active container to the stack
- `DATACOPY (0xd3)` instruction
    - deduct 3 gas
    - pops `mem_offset`, `offset`, `size` from the stack
    - perform memory expansion to `mem_offset + size` and deduct memory expansion cost
    - deduct `3 * ((size + 31) // 32)` gas for copying
    - read `[offset, offset+size]` from the data section of the active container and write it to memory starting at offset `mem_offset`
    - pad with 0s if reading out of data bounds
- `DUPN (0xe6)` instruction
    - deduct 3 gas
    - read uint8 operand `imm`
    - `n = imm + 1`
    - `n`‘th (1-based) stack item is duplicated at the top of the stack
    - Stack validation: `stack_height >= n`
- `SWAPN (0xe7)` instruction
    - deduct 3 gas
    - read uint8 operand `imm`
    - `n = imm + 1`
    - `n + 1`th stack item is swapped with the top stack item (1-based).
    - Stack validation: `stack_height >= n + 1`
- `EXCHANGE (0xe8)` instruction
    - deduct 3 gas
    - read uint8 operand `imm`
    - `n = imm >> 4 + 1`, `m = imm & 0x0F + 1`
    - `n + 1`th stack item is swapped with `n + m + 1`th stack item (1-based).
    - Stack validation: `stack_height >= n + m + 1`
- `RETURNDATALOAD (0xf7)` instruction
    - deduct 3 gas
    - pop `offset` from the stack
    - if `offset + 32 > len(returndata buffer)`, execution results in an exceptional halt
    - push 1 item onto the stack, the 32-byte word read from the returndata buffer starting at `offset`
- `EXTCALL (0xf8)`, `EXTDELEGATECALL (0xf9)`, `EXTSTATICCALL (0xfb)`
    - Replacement of `CALL`, `DELEGATECALL` and `STATICCALL` instructions, as specced out in [EIP-7069](https://eips.ethereum.org/EIPS/eip-7069), except the runtime operand stack check. In particular:
    - The `gas_limit` input is removed.
    - The `output_offset` and `output_size` is removed.
    - The `gas_limit` will be set to `(gas_left / 64) * 63` (as if the caller used `gas()` in place of `gas_limit`).
    - `EXTDELEGATECALL` to a legacy contract is disallowed, and it returns `1` (same as when the callee frame `reverts`) to signal failure. Only initial gas cost of `EXTDELEGATECALL` is consumed (similarly to the call depth check) and the target address still becomes warm. We allow legacy to EOF path for existing proxy contracts to be able to use EOF upgrades.

    **NOTE**: The replacement instructions `EXT*CALL` continue being treated as **undefined** in legacy code.

## Code Validation

- no unassigned instructions used
- instructions with immediate operands must not be truncated at the end of a code section
- `RJUMP` / `RJUMPI` / `RJUMPV` operands must not point to an immediate operand and may not point outside of code bounds
- `CALLF` and `JUMPF` operand may not exceed `num_code_sections`
- `CALLF` operand must not point to to a section with `0x80` as outputs (non-returning)
- `JUMPF` operand must point to a code section with equal or fewer number of outputs as the section in which it resides, or to a section with `0x80` as outputs (non-returning)
- no section may have more than 127 inputs or outputs
- section type has `0x80` as outputs value, and is non-returning, if and only if this section contains neither `RETF` instructions nor `JUMPF` into returning (`outputs <= 0x7f`) sections.
    - in particular, section having only `JUMPF`s to non-returning sections is non-returning itself.
- the first code section must have a type signature `(0, 0x80, max_stack_height)` (0 inputs non-returning function)
- `EOFCREATE` `initcontainer_index` must be less than `num_container_sections`
- `EOFCREATE` the subcontainer pointed to by `initcontainer_index` must have its `len(data_section)` equal `data_size`, i.e. data section content is exactly as the size declared in the header (see [Data section lifecycle](#data-section-lifecycle))
- `RETURNCONTRACT` `deploy_container_index` must be less than `num_container_sections`
- `DATALOADN`'s `immediate + 32` must be within `pre_deploy_data_size` (see [Data Section Lifecycle](#data-section-lifecycle))
     - the part of the data section which exceeds these bounds (the `dynamic_aux_data` portion) needs to be accessed using `DATALOAD` or `DATACOPY`
- no unreachable sections are allowed, i.e. every section is referenced by at least one non-recursive `CALLF` or `JUMPF`, and section 0 is implicitly reachable.

## Stack Validation

- Code basic blocks must be ordered in a way that every block is reachable either by a forward jump or sequential flow of instructions. In other words, there is no basic block reachable only by a backward jump.
- Validation procedure does not require actual operand stack implementation, but only to keep track of its height.
- The computational and space complexity is O(len(code)). Each instruction is visited exactly once.
- `stack_height_...` below refers to the number of stack values accessible by this function, i.e. it does not take into account values of caller functions’ frames (but does include this function’s inputs).
- For each instruction in the code the operand stack height bounds are recorded as `stack_height_min` and `stack_height_max`. Instructions are scanned in a single linear pass over the code.
- During scanning:
  - first instruction has `stack_height_min = stack_height_max = types[current_section_index].inputs`;
  - for each instruction reached from a forwards jump or sequential flow from previous instruction, update the target bounds so that they contain source bounds, i.e. `target_stack_min = min(target_stack_min, source_stack_min + change)` and `target_stack_max = max(target_stack_max, source_stack_max + change)`. `change` is the stack height change of the source instruction OPCODE or `outputs - inputs` in case of `CALLF`;
  - for each instruction reached from a backwards jump, check if target bounds are same as source bounds, i.e. `target_stack_min == source_stack_min + change` and `target_stack_max == source_stack_max + change`.
- No instruction may access more operand stack items than `stack_height_min`
- Terminating instructions: `STOP`, `INVALID`, `RETURN`, `REVERT`, `RETURNCONTRACT`, `RETF`, `JUMPF`.
- During `CALLF`, the following must hold: `stack_height_min >= types[target_section_index].inputs`
- During `CALLF` and `JUMPF`, the following must hold: `stack_height_max + types[target_section_index].max_stack_height - types[target_section_index].inputs <= 1024`
- Stack validation of `JUMPF` depends on "non-returning" status of target section
    - `JUMPF` into returning section (can be only from returning section): `stack_height_min == stack_height_max == type[current_section_index].outputs + type[target_section_index].inputs - type[target_section_index].outputs`
    - `JUMPF` into non-returning section: `stack_height_min >= types[target_section_index].inputs`
- During `RETF`, the following must hold: `stack_height_max == stack_height_min == types[current_code_index].outputs`
- During terminating instructions `STOP`, `INVALID`, `RETURN`, `REVERT`, `RETURNCONTRACT` operand stack may contain extra items below ones required by the instruction
- the last instruction may be a terminating instruction or `RJUMP`
- no instruction may be unreachable
- maximum data stack of a function must not exceed 1023
- `types[current_code_index].max_stack_height` must match the maximum stack height observed during validation
- Find full spec of the previous _more restrictive_ algorithm at https://eips.ethereum.org/EIPS/eip-5450#operand-stack-validation

## Examples

Annotated examples of EOF formatted containers demonstrating several key features of EOF can be found in [this test file within the `evmone` project repository](https://github.com/ethereum/evmone/blob/eof-examples/test/unittests/eof_example_test.cpp).

## Appendix: Creator Contract

```solidity
{
/// Takes [index][salt][init_data] as input,
/// creates contract and returns the address or failure otherwise

/// init_data.length can be 0, but the first 2 words are mandatory
let size := calldatasize()
if lt(size, 64) { revert(0, 0) }

let tx_initcode_index := calldataload(0)
let salt := calldataload(32)

let init_data_size := sub(size, 64)
calldatacopy(0, 64, init_data_size)

let ret := txcreate(tx_initcode_index, callvalue(), salt, 0, init_data_size)
if iszero(ret) { revert(0, 0) }

mstore(0, ret)
return(0, 32)

// Helper to compile this with existing Solidity (with --strict-assembly mode)
function txcreate(a, b, c, d, e) -> f {
    f := verbatim_5i_1o(hex"ed", a, b, c, d, e)
}
    
}
```

## Appendix: Original EIPs

These are the individual EIPs which evolved into this spec.

Specifications contained within are **out-of-date**, use only for reference and to look up motivation!

- 📃[EIP-3540](https://eips.ethereum.org/EIPS/eip-3540): EOF - EVM Object Format v1 [_history_](https://github.com/ethereum/EIPs/commits/master/EIPS/eip-3540.md)
- 📃[EIP-3670](https://eips.ethereum.org/EIPS/eip-3670): EOF - Code Validation [_history_](https://github.com/ethereum/EIPs/commits/master/EIPS/eip-3670.md)
- 📃[EIP-4200](https://eips.ethereum.org/EIPS/eip-4200): EOF - Static relative jumps [_history_](https://github.com/ethereum/EIPs/commits/master/EIPS/eip-4200.md)
- 📃[EIP-4750](https://eips.ethereum.org/EIPS/eip-4750): EOF - Functions [_history_](https://github.com/ethereum/EIPs/commits/master/EIPS/eip-4750.md)
- 📃[EIP-5450](https://eips.ethereum.org/EIPS/eip-5450): EOF - Stack Validation [_history_](https://github.com/ethereum/EIPs/commits/master/EIPS/eip-5450.md)
- 📃[EIP-6206](https://eips.ethereum.org/EIPS/eip-6206): EOF - JUMPF instruction [_history_](https://github.com/ethereum/EIPs/commits/master/EIPS/eip-6026.md)
- 📃[EIP-7480](https://eips.ethereum.org/EIPS/eip-7480): EOF - Data section access instructions [_history_](https://github.com/ethereum/EIPs/commits/master/EIPS/eip-7480.md)
- 📃[EIP-663](https://eips.ethereum.org/EIPS/eip-663): Unlimited SWAP and DUP instructions [_history_](https://github.com/ethereum/EIPs/commits/master/EIPS/eip-663.md)
- 📃[EIP-7069](https://eips.ethereum.org/EIPS/eip-7069): Revamped CALL instructions (*does not require EOF*) [_history_](https://github.com/ethereum/EIPs/commits/master/EIPS/eip-7069.md)
- 📃[EIP-7620](https://eips.ethereum.org/EIPS/eip-7620): EOF - Contract Creation Instructions [_history_](https://github.com/ethereum/EIPs/commits/master/EIPS/eip-7620.md)


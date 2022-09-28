
## Full container bytecode

```
ef0001 030006 01003b 010017 01001d 00 000001010101 60043560003560e01c63c766526781145d001c63c6c2ea1781145d00065050600080fd50fb000260005260206000f350fb000160005260206000f3 600181115d0004506001fc60018103fb000181029050fc 600281115d0004506001fc60028103fb000260018203fb0002019050fc
```

Without spaces:
```
ef000103000601003b01001701001d0000000101010160043560003560e01c63c766526781145d001c63c6c2ea1781145d00065050600080fd50fb000260005260206000f350fb000160005260206000f3600181115d0004506001fc60018103fb000181029050fc600281115d0004506001fc60028103fb000260018203fb0002019050fc
```

## Dispatch function

### Pseudocode

```
function main()
{
    let i := shr(calldataload(4))
    let sig := shr(calldataload(0), 224)
    if (eq(sig, 0xc7665267)) // fac(uint256)
    {
      mstore(0, fac(i))
      return(0, 32)
    }
    else if (eq(sig, 0xc6c2ea17)) // fib(uint256)
    {
      mstore(0, fib(i))
      return(0, 32)
    }
    else
    {
      revert(0, 0)
    }
}
```

### Assembly

```
push1 4
calldataload
push1 0
calldataload
push1 0xe0
shr
push4 0xc7665267
dup2
eq
rjumpi if1_true

//if1_false:
push4 0xc6c2ea17
dup2
eq
rjumpi if2_true

//if2_false:
pop
pop
push1 0
dup1
revert

//if2_true:
pop
callf fib
push1 0
mstore
push1 32
push1 0
return

//if1_true:
pop
callb fac
push1 0
mstore
push1 32
push1 0
return
```

### Section bytecode

```
60043560003560e01c63c766526781145d001c 63c6c2ea1781145d0006 5050600080fd 50fb000260005260206000f3 50fb000160005260206000f3
```


## Factorial function

### Pseudocode

```
function fac(i)
{
    if gt(i, 1)
    {
        retf(mul(i, fac(sub(i, 1))))
    }
    else
    {
        retf(1)
    }
}
```

### Assembly

```
push1 1
dup2
gt
rjumpi if_true

//if_false:
pop
push1 1
retf

//if_true:
push1 1
dup2
sub
callf fac
dup2
mul
swap1
pop
retf
```

### Section bytecode

```
600181115d0004 506001fc 60018103fb000181029050fc
```


## Fibonacci function

### Pseudocode

```
function fib(i)
{
    if gt(i, 2)
    {
        retf(add(fib(sub(i, 1)), fib(sub(i, 2))))
    }
    else
    {
        retf(1)
    }
}
```

### Assembly

```
push1 2
dup2
gt
rjumpi if_true

//if_false:
pop
push1 1
retf

//if_true:
push1 2
dup2
sub
callf fib
push1 1
dup3
sub
callf fib
add
swap1
pop
retf
```

### Section bytecode

```
600281115d0004 506001fc 60028103fb000260018203fb0002019050fc
```

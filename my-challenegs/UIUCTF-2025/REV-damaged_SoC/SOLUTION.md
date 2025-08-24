# Damaged SoC

This challenge shipped with a custom hardware implementation of MIPS64 litten endian ISA in System Verilog. The main point is use `syscall` as branch instruction to smash the control flow.

## Solution

* Identify the architecture with filename in `infra.zip`.
* Notice the flag length is 39 and placed in 0x8.
* Notice the first 8 bytes are interrupt handler function address in `data_mem.sv` hardware implementation.
* Notice start address is hard-coded `0x100` in hardware implementation.
* Notice `syscall` normally act as branch(jump offset). Then can either write script to replace those with branch or write IDA custom decompile module.

Then rest of parts are reversing some random `xor` and shifting to recover the correct "signature".

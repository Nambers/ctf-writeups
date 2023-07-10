# vmwhere 1
## Description
Usage: ./chal program
## Attachment
chal - a custom VM  
program - bytecode  
## Solution
I rewrote the main logic of VM into python(with help from ChatGPT), then use the `IndexError` as a flag to brute force the entire flag.  
```python
def CONCAT11(param_1: int, param_2: int):
    return int(hex(param_1).removeprefix("0x") + hex(param_2).removeprefix("0x"), 16)

def execute_program(param_1: bytes, param_2: int, inp: bytes):
    # print("size", hex(param_2))
    pbVar5 = bytearray(0x1000)
    local_20 = 0
    local_18 = 0
    
    while True:
        
        if local_20 < 0 or local_20 >= param_2:
            print(f"Program terminated unexpectedly. Last instruction: 0x{local_20:04x}")
            return 1
        
        pbVar1 = local_20 + 1
        opcode = param_1[local_20]
        # print(hex(opcode))
        # print(pbVar5.decode())
        if opcode == 0:
            return 0
        elif opcode == 1:
            pbVar5[local_18-2] = pbVar5[local_18-2] + pbVar5[local_18-1]
            local_18 = local_18 - 1
            local_20 = pbVar1
        elif opcode == 2:
            pbVar5[local_18-2] = pbVar5[local_18-2] - pbVar5[local_18-1]
            local_18 = local_18 -1
            local_20 = pbVar1
        elif opcode == 3:
            pbVar5[local_18-2] = pbVar5[local_18-2] & pbVar5[local_18-1]
            local_18 = local_18 -1
            local_20 = pbVar1
        elif opcode == 4:
            pbVar5[local_18-2] = pbVar5[local_18-2] | pbVar5[local_18-1]
            local_18 = local_18 - 1
            local_20 = pbVar1
        elif opcode == 5:
            pbVar5[local_18-2] = pbVar5[local_18-2] ^ pbVar5[local_18-1]
            local_18 = local_18 - 1
            local_20 = pbVar1
        elif opcode == 6:
            pbVar5[local_18-2] = pbVar5[local_18-2] << (pbVar5[local_18-1] & 0x1f)
            local_18 = local_18 - 1
            local_20 = pbVar1
        elif opcode == 7:
            pbVar5[local_18-2] = (pbVar5[local_18-2] & 0xff) >> (pbVar5[local_18-1] & 0x1f)
            local_18 = local_18 - 1
            local_20 = pbVar1
        elif opcode == 8:
            iVar4 = inp[0]
            inp = inp[1:]
            pbVar5[local_18] = iVar4 & 0xff
            local_18 = local_18 + 1
            local_20 = pbVar1
        elif opcode == 9:
            local_18 = local_18 - 1
            # print(chr(pbVar5[local_18]), end="")
            local_20 = pbVar1
        elif opcode == 10:
            pbVar5[local_18] = param_1[pbVar1]
            local_18 = local_18 + 1
            local_20 = local_20 + 2
        elif opcode == 0xb:
            if pbVar5[local_18-1] < 0:
                pbVar1 = (pbVar1 + CONCAT11(param_1[pbVar1], param_1[local_20 + 2])) & 0xffff
            local_20 = pbVar1
            local_20 = local_20 + 2
        elif opcode == 0xc:
            if pbVar5[local_18-1] == 0:
                pbVar1 = (pbVar1 + CONCAT11(param_1[pbVar1], param_1[local_20 + 2])) & 0xffff
            local_20 = pbVar1
            local_20 = local_20 + 2
        elif opcode == 0xd:
            local_20 = (pbVar1 + CONCAT11(param_1[pbVar1], param_1[local_20 + 2]) + 2) & 0xffff
        elif opcode == 0xe:
            local_18 = local_18 - 1
            local_20 = pbVar1
        elif opcode == 0xf:
            pbVar5[local_18] = pbVar5[local_18-1]
            local_18 = local_18 + 1
            local_20 = pbVar1
        elif opcode == 0x10:
            local_20 = local_20 + 2
            bVar2 = param_1[pbVar1]
            if local_18 < bVar2:
                print(f"Stack underflow in reverse at 0x{local_20:04x}")
            
            for local_24 in range(bVar2 >> 1):
                bVar3 = pbVar5[local_18 + ((local_24 - bVar2) & 0xff)]
                pbVar5[local_18 + ((~local_24) & 0xff)] = pbVar5[local_18 + local_24]
                pbVar5[local_18 + local_24] = bVar3
        elif opcode == 0x28:
            # fix me
            print("!!Hit FIX ME!")
            local_20 = pbVar1
            # raise Exception()
        else:
            print(f"Unknown opcode: 0x{opcode:02x} at 0x{local_20:04x}")
            return 1
        
        if local_18 < 0:
            break
        
        if 0x1000 < local_18:
            print(f"Stack overflow at 0x{local_20:04x}")
            return 1
    
    print(f"Stack underflow at 0x{local_20:04x}")
    return 1

import string

if __name__ == "__main__":
    with open("program", "rb") as f:
        program = f.read()
    inp = b"uiuctf"
    while True:
        succ = False
        for a in string.printable + "}":
            if inp[-1] == b"}":
                print(inp.decode())
                exit()
            try:
                execute_program(program, len(program), inp + a.encode())
            except IndexError as e:
                inp = inp + a.encode()
                print(inp.decode())
                succ = True
                break
        # print(inp.decode())
        if not succ:
            raise Exception()
```
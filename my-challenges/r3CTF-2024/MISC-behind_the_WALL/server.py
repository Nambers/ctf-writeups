#!/usr/bin/env python3.12
# run on python:3.12-slim docker image
import gc
import opcode

callback_codes = bytes.fromhex(input("Enter the code in hex: "))
callback_consts = input("Enter the const separated by comma: ").strip().removeprefix('(').removesuffix(')').split(",")
callback_names = input("Enter the names separated by comma: ").strip().removeprefix('(').removesuffix(')').split(",")
callback_stack_size = int(input("Enter the stack size: "))

# check callback
# constants must be number or None
callback_consts = tuple(c if len(c) == 1 and c >= 'a' and c <= 'z'else None if c == "None" else int(c) for c in callback_consts if c != "")
if len(callback_consts) > 20:
    print("too many constants")
    exit(1)

banned_letters = "dsfhjmoquvwxyz()[]{}<>@,;=_"
callback_names = tuple(a for a in callback_names if a != "")
for n in callback_names:
    if not isinstance(n, str) or any(a in n.lower() for a in banned_letters):
        print("banned letter in name")
        exit(1)
if len(callback_names) > 10:
    print("too many names")
    exit(1)

banned_ops = [opcode.opmap["IMPORT_NAME"], opcode.opmap["IMPORT_FROM"], opcode.opmap["BINARY_OP"]]
load_gl0bal_count = 0

for i in range(0, len(callback_codes), 2):
    a,b = callback_codes[i:i+2]
    if a == opcode.opmap["LOAD_CONST"] and b >= len(callback_consts):
        print("OOB is prohibited")
        exit(1)
    elif a == opcode.opmap["LOAD_GLOBAL"]:
        load_gl0bal_count += 1
    elif a in banned_ops:
        print("contains op that is prohibited")
        exit(1)
    
if load_gl0bal_count > 6:
    print("too many load global")
    exit(1)
if len(callback_codes) > 1000:
    print("too many ocodes")
    exit(1)

if callback_stack_size < 0 or callback_stack_size > 25:
    print("stack size is too large")
    exit(1)

def callback(re):
    pass


callback.__code__ = callback.__code__.replace(co_code=callback_codes, co_consts=callback_consts, co_names=callback_names, co_stacksize=callback_stack_size)


class _FlagGen:
    def __init__(self):
        self._flag = "r3ctf{y37_4n07h3r_5hy_fl46...}"


result = False


def gRc(): # stand for getResultChecker XD
    flag = _FlagGen()

    def checker():
        # TODO: do some check
        result = hash(flag._flag) == 0xdeadc0de
        # don't leak the flag :)
        gc.collect()
    print("checker generated")
    return checker

gRc()()

callback(result)

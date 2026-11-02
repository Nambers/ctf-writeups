#!python3.12
# run on python 3.12.4
import sys
import os
import json

assert sys.version.startswith("3.12.4")

test_code = input("Enter the function in json: ")
sys.stdin.close()

if len(test_code) > 2540:
    exit(1)
test_code: json = json.loads(test_code)
del json

test_code["co_consts"] = tuple(tuple(a) if isinstance(
    a, list) else a for a in test_code["co_consts"])
test_code["co_names"] = tuple(tuple(a) if isinstance(
    a, list) else a for a in test_code["co_names"])
test_code["co_varnames"] = tuple(tuple(a) if isinstance(
    a, list) else a for a in test_code["co_varnames"])


def check_ele(ele, inner=False):
    if ele is None:
        pass
    elif isinstance(ele, int):
        # some random magic numbers w/o any meaning
        if ele not in range(-0xd000, 0x50000):
            exit(1)
    elif isinstance(ele, str):
        if any((ord(a) not in (list(range(ord('0'), ord('9') + 1)) + list(range(ord('a'), ord('z') + 1)) + list(range(ord('A'), ord('Z') + 1)) + [95])) for a in ele):
            exit(1)
        elif len(ele) > 242:
            exit(1)
    elif isinstance(ele, tuple):
        if inner:
            exit(1)
        for a in ele:
            check_ele(a, True)
    else:
        exit(1)


for ele in test_code["co_consts"] + test_code["co_names"]:
    check_ele(ele)

del check_ele


def test(): pass


test.__code__ = test.__code__.replace(co_code=bytes.fromhex(test_code["co_code"]),
                                      co_consts=test_code["co_consts"],
                                      co_names=test_code["co_names"],
                                      co_stacksize=test_code["co_stacksize"],
                                      co_nlocals=test_code["co_nlocals"],
                                      co_varnames=test_code["co_varnames"])

del test_code

def auditHookHandler(e):
    def handler(x, _):
        if not (x == "object.__getattr__" or x == "object.__setattr__" or x == "code.__new__"):
            e(1) # plz don't smash _exit :)
            while(1): pass
    return handler


sys.addaudithook(auditHookHandler(os._exit))
del sys

test()

# free flag?! :)
os.system("cat /flag")

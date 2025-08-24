# this z3 script is kind of broken. It can't find the 2nd solution

from z3 import *


def all_smt(s, initial_terms):
    def block_term(s, m, t):
        s.add(t != m.eval(t, model_completion=True))

    def fix_term(s, m, t):
        s.add(t == m.eval(t, model_completion=True))

    def all_smt_rec(terms):
        if sat == s.check():
            m = s.model()
            yield m
            for i in range(len(terms)):
                s.push()
                block_term(s, m, terms[i])
                for j in range(i):
                    fix_term(s, m, terms[j])
                yield from all_smt_rec(terms[i:])
                s.pop()

    yield from all_smt_rec(list(initial_terms))


s = Solver()

key = [BitVec(f"key_{i}", 8) for i in range(32)]
s.add(key[23] + key[24] == 0x53)

chunk = Concat(key[23], key[22], key[21], key[20], key[19], key[18], key[17], key[16])
chunk2 = Concat(key[27], key[26], key[25], key[24])

verify_state = 0x1337C0DE12345678 ^ chunk
verify_state2 = 0x3EADBE3F ^ chunk2

verify_state = ((verify_state << 8) & 0xFFFFFFFFFFFFFFFF) | (
    (verify_state >> 56) & 0xFF
)

verify_state2 = ((verify_state2 << 4) & 0xFFFFFFFF) | ((verify_state2 >> 28) & 0xF)

verify_state = (verify_state + 0x0123456789ABCDEF) & 0xFFFFFFFFFFFFFFFF
verify_state2 = (verify_state2 + 0x87654321) & 0xFFFFFFFF

verify_state = verify_state ^ (ZeroExt(32, verify_state2) << 32)
verify_state2 = verify_state2 ^ Extract(31, 0, verify_state)

verify_state = verify_state ^ 0xFEDCBA9876543210
verify_state2 = verify_state2 ^ 0x13579BDF

s.add(verify_state == 0xC956B3009784E40F)
s.add(verify_state2 == 0x83C5A9D1)

for i in range(16, 28):
    s.add(key[i] >= 32)
    s.add(key[i] <= 126)


solutions = []
max_solutions = 50

for sol in all_smt(s, key[16:28]):
    solution = [sol[key[i]].as_long() for i in range(16, 28)]
    key_str = "".join(chr(c) if 32 <= c <= 126 else f"\\x{c:02x}" for c in solution)
    print(f"key[16:28]: {key_str}")

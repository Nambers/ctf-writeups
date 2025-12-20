from vcdvcd import VCDVCD
from tqdm import tqdm
import hashlib

# vcd = VCDVCD("trace.vcd")
vcd = VCDVCD("data.vcd")

flag = ""

ciphertext = b""
rounds_end = [0]

takens = [t for t, v in vcd["TOP.SOC.stdout_taken"].tv if v == "1"]
# get chipertext
for t, v in vcd["TOP.SOC.stdout.w_data[63:0]"].tv:
    if (t + 2) in takens:
        rounds_end.append(t)
# ciphertext = ciphertext.rstrip(b"\x00").removesuffix(b"H").rstrip(b"\n")
rounds_end = rounds_end[:-1]
rounds_i = []
# print(ciphertext)
keys = [0xF0F0F0F0, 0x0F0F0F0F]

couts = []
for i in range(len(rounds_end) - 1):
    couts.append([])
    last_pc = ""
    for j in range(rounds_end[i], rounds_end[i + 1]):
        # don't count if
        # - ALU_op is not add
        # - PC is outside TEA range
        # - stalled (same PC as last time)
        if (
            vcd["TOP.SOC.core.EX_stage.alu_.alu_op[2:0]"][j] == "010"
            and (
                (0x228)
                <= int(vcd["TOP.SOC.core.next_fetch_pc[63:0]"][j], 2)
                <= (0x270 + 0x10)
            )
            # and vcd["TOP.SOC.core.ID_stage.stall"][j] != "1"
        ):
            if vcd["TOP.SOC.core.next_fetch_pc[63:0]"][j] == last_pc:
                couts[-1].pop()
            else:
                last_pc = vcd["TOP.SOC.core.next_fetch_pc[63:0]"][j]
            couts[-1].append(
                {
                    j: [int(vcd["TOP.SOC.core.EX_stage.alu_.au_0.adder_0.cout"][j], 2)]
                    + [
                        int(
                            vcd[
                                f"TOP.SOC.core.EX_stage.alu_.au_0.genblk1[{k}].adder_0.cout"
                            ][j],
                            2,
                        )
                        for k in range(1, 64)
                    ]
                }
            )

    # should be 9 * 32 = 288 addition operations
    if len(couts[-1]) >= 288:
        print(f"Round {i+1}, area: {rounds_end[i]} - {rounds_end[i+1]}")
        rounds_i += [i]
        print("Addition count:", len(couts[-1]))
    else:
        couts.pop()


def simulate_addition_with_cout(a, b):
    result = 0
    carry = 0
    cout_bits = []

    for i in range(32):
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        sum_bit = bit_a ^ bit_b ^ carry
        carry = (bit_a & bit_b) | (bit_a & carry) | (bit_b & carry)
        cout_bits.append(carry)
        result |= sum_bit << i
    return result, cout_bits


ofs = 0
key0_ofs = 0
key1_ofs = 0

# based on the prefix, we can find the fixed offset of (v1 + sum) = 49
c = simulate_addition_with_cout(0x9E3779B9, int.from_bytes(b"flag", "little"))
c1 = simulate_addition_with_cout(
    keys[0], (int.from_bytes(b"flag", "little") << 4) & 0xFFFFFFFF
)
c2 = simulate_addition_with_cout(
    keys[1], (int.from_bytes(b"flag", "little") >> 5) & 0xFFFFFFFF
)
for e in couts[0]:
    if c[1] == list(e.values())[0][:32]:
        print("Found matching addition for 'flag':", e)
        ofs = list(e.keys())[0] - rounds_end[rounds_i[0]]
    if c1[1] == list(e.values())[0][:32]:
        print("Found matching addition for 'flag' (key0):", e)
        key0_ofs = list(e.keys())[0] - rounds_end[rounds_i[0]]
    if c2[1] == list(e.values())[0][:32] and key1_ofs == 0:
        print("Found matching addition for 'flag' (key1):", e)
        key1_ofs = list(e.keys())[0] - rounds_end[rounds_i[0]]
print(f"key0_ofs = {key0_ofs}, key1_ofs = {key1_ofs}, ofs = {ofs}")
# health check
# c = simulate_addition_with_cout(0x9E3779B9, int.from_bytes(b"{a4l", "little"))
# for e in couts[1]:
#     if c[1] == list(e.values())[0][:32]:
#         print("Found matching addition for '{a4l':", e)
# c = simulate_addition_with_cout(0x9E3779B9, int.from_bytes(b"g!c0", "little"))
# for e in couts[2]:
#     if c[1] == list(e.values())[0][:32]:
#         print("Found matching addition for 'g!c0':", e)
# c = simulate_addition_with_cout(0x9E3779B9, int.from_bytes(b"00l}", "little"))
# for e in couts[3]:
#     if c[1] == list(e.values())[0][:32]:
#         print("Found matching addition for '00l}':", e)

remaining = []
key0 = []
key1 = []
for i in range(1, 4):
    for a in couts[i]:
        if list(a.keys())[0] == rounds_end[rounds_i[i]] + (ofs):
            remaining.append(list(a.values())[0][:32])
        if list(a.keys())[0] == rounds_end[rounds_i[i]] + (key0_ofs):
            key0.append(list(a.values())[0][:32])
        if list(a.keys())[0] == rounds_end[rounds_i[i]] + (key1_ofs):
            key1.append(list(a.values())[0][:32])
print(remaining, key0, key1)

pflags = [set()] * len(remaining)

# health check
# print(hex(simulate_simple_hash(flags[-1].encode(), "ilov".encode())), hex(hashes[0]))

with open("./rockyou.txt", "r", encoding="utf-8", errors="ignore") as f:
    rockyou = f.readlines()

import string

for i in range(len(remaining)):
    bans = set()
    for w in tqdm(rockyou):
        if any([a in w for a in string.punctuation + string.digits]):
            continue
        w = w.strip()[:4]
        c = simulate_addition_with_cout(
            0x9E3779B9, int.from_bytes(w.encode(), "little")
        )
        c1 = simulate_addition_with_cout(
            keys[0], (int.from_bytes(w.encode(), "little") << 4) & 0xFFFFFFFF
        )
        c2 = simulate_addition_with_cout(
            keys[1], int.from_bytes(w.encode(), "little") >> 5
        )
        if (
            w not in bans
            and (c[1] == remaining[i])
            and (c1[1] == key0[i])
            and (c2[1] == key1[i])
            # and simulate_simple_hash(flags[-1].encode(), w.encode()) in hashes
        ):
            print(f"Found {i} part of the flag: {w}")
            pflags[i].add(w)
        bans.add(w)
    print(
        f"Possible parts for segment {i+1}:",
        pflags[i],
    )
# flag_love_play_pass
# md5sum = 12c1e3963c168d4cdfdf98398ad1d01b

# pflags = [
#     {"lovm", "lovu", "love"},
#     {"pley", "play", "love", "plei", "lovm", "lovu", "plai"},
#     {
#         "pasc",
#         "pley",
#         "pask",
#         "play",
#         "love",
#         "pass",
#         "pesk",
#         "plei",
#         "pesc",
#         "lovm",
#         "lovu",
#         "plai",
#         "pess",
#     },
# ]

# try all combinations
flags = ["flag"]
for a in pflags[0]:
    for b in pflags[1]:
        for c in pflags[2]:
            test_flag = flags[0] + "_" + a + "_" + b + "_" + c
            print(test_flag)
            if (
                hashlib.md5(test_flag.encode()).hexdigest()
                == "a23a6bff24f1db095015b55fbc0c8418"
            ):
                flags += [a, b, c]
                print("Found the flag:", "_".join(flags))
                break

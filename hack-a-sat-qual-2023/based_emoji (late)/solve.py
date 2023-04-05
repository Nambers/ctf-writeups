# *-* coding: utf-8 *-*
# each emoji represent a 32-based number
# use z3 to solve each emoji's value
# factors of each emoji
# 🛰 = 1

# -- emoji decode part --
words={'🎉': '0', '🛰': '1', '🥃': '2', '🌝': ' 🛰  🌝 ', '💾': ' 🛰  🦍  🌟  💾 ', '🛸': ' 🛰  🦍  🥃  🛸 ', '🤯': ' 🛰  🌎  🤯 ', '🙌': ' 🛰  🙌 ', '📡': ' 🛰  📡  🥃 ', '🦍': ' 🛰  🦍 ', '👀': ' 🛰  🥃  🌎  👀 ', '💥': ' 🦍  🥃  🛰  💩  💽  💥  📡  🛸 ', '🥵': ' 🥃  🛰  💩  📡  🥵 ', '💩': ' 💩  🛰  📡  🥃 ', '💵': ' 🦍  🌟  🥃  🛰  💵  🛸 ', '🌛': ' 🦍  🥃  🧠  🛰  🌎  👀  🌛  🛸 ', '🌞': ' 🛰  🌝  🥃  🌞 ', '🌟': ' 🛰  🦍  🌟 ', '👽': ' 🛰  👽 ', '🗿': ' 🛰  🗿  🦍  🚀 ', '🌎': ' 🛰  🌎 ', '💽': ' 🦍  🥃  🛰  💽  📡  🛸 ', '👄': ' 🛰  👄 ', '🍌': ' 🍌  🥃  🛰  🚀  📡  🧨 ', '🔥': ' 🛰  🔥 ', '🤟': ' 🛰  🤟 ', '🧨': ' 🛰  🚀  🧨  🥃 ', '🧂': ' 🛰  🧂 ', '🚀': ' 🛰  🚀 ', '🧠': ' 🛰  🌎  🦍  🧠 ', '💯': ' 🛰  🔥  💯  🥃 ', '📼': ' 🥃  🛰  🌎  📼  📡  👀 '}
from z3 import IntVal, Int, Solver, Distinct
s=Solver()
vals=[IntVal(a) for a in range(3)] + [Int("val" + str(i)) for i in range(3, len(words))]
      
for v in vals[3:]:
    s.add(v >= IntVal(3))
    s.add(v < IntVal(32))

keys=list(words.keys())

def addConstraintOfPrimeBit(num, bitNum):
    global s, vals
    val=vals[num]
    lowerBound=int('1' + '0' * (bitNum - 1), 2)
    s.add(val<=IntVal(int('1' * bitNum, 2)))
    s.add(val>=IntVal(lowerBound))
    # add prime constraint
    if lowerBound > 2:
        for i in range(2, lowerBound):
            # print(f"val{num} % {i} != 0")
            s.add(val % IntVal(i) != IntVal(0))

for i in range(3, len(keys)):
    x=keys[i]
    val=[keys.index(a) for a in words[x].strip().split(" ") if a != ""]
    for b in val:
        # print(i, "%", b, "==0")
        # vals[1] == 1
        if b != 1 and i != 1:
            s.add(vals[i] % vals[b] == IntVal(0))

s.add(Distinct(vals))

# 🇷 🇦 🇳 🇩 🇴 🇲   2⃣   ➖ 🇧 🇮 🇹   🇵 🇷 🇮 🇲 🇪   🟰    🦍
# 🦍 is prime and 🦍 is 2bits, so 2 < it <= 3
addConstraintOfPrimeBit(keys.index('🦍'), 2)

# 🇷 🇦 🇳 🇩 🇴 🇲   3⃣   ➖ 🇧 🇮 🇹   🇵 🇷 🇮 🇲 🇪   🟰    🌎
addConstraintOfPrimeBit(keys.index('🌎'), 3)

# 🇷 🇦 🇳 🇩 🇴 🇲   3⃣   ➖ 🇧 🇮 🇹   🇵 🇷 🇮 🇲 🇪   🟰    🚀
addConstraintOfPrimeBit(keys.index('🚀'), 3)

# 🇷 🇦 🇳 🇩 🇴 🇲   4⃣   ➖ 🇧 🇮 🇹   🇵 🇷 🇮 🇲 🇪   🟰    🔥
addConstraintOfPrimeBit(keys.index('🔥'), 4)

# 🇷 🇦 🇳 🇩 🇴 🇲   4⃣   ➖ 🇧 🇮 🇹   🇵 🇷 🇮 🇲 🇪   🟰    🌝
addConstraintOfPrimeBit(keys.index('🌝'), 4)

# 🇷 🇦 🇳 🇩 🇴 🇲   5⃣   ➖ 🇧 🇮 🇹   🇵 🇷 🇮 🇲 🇪   🟰    🙌
addConstraintOfPrimeBit(keys.index('🙌'), 5)

# 🇷 🇦 🇳 🇩 🇴 🇲   5⃣   ➖ 🇧 🇮 🇹   🇵 🇷 🇮 🇲 🇪   🟰    🧂
addConstraintOfPrimeBit(keys.index('🧂'), 5)

# 🇷 🇦 🇳 🇩 🇴 🇲   5⃣   ➖ 🇧 🇮 🇹   🇵 🇷 🇮 🇲 🇪   🟰    👄
addConstraintOfPrimeBit(keys.index('👄'), 5)


# these stuff will make solver be unsat. I don't know why
# #  🦍  🛰💯  🛸  💵  🌟  🥃  🛰  💾 of 6 bits
# random_6_bit = Int("random_6_bit")
# s.add(random_6_bit % vals[keys.index('🦍')] == IntVal(0))
# s.add(random_6_bit % vals[keys.index('🛰')] == IntVal(0))
# s.add(random_6_bit % vals[keys.index('💯')] == IntVal(0))
# s.add(random_6_bit % vals[keys.index('🛸')] == IntVal(0))
# s.add(random_6_bit % vals[keys.index('💵')] == IntVal(0))
# s.add(random_6_bit % vals[keys.index('🌟')] == IntVal(0))
# s.add(random_6_bit % vals[keys.index('🥃')] == IntVal(0))
# s.add(random_6_bit % vals[keys.index('💾')] == IntVal(0))
# s.add(random_6_bit >= IntVal(int('100000', 2)))
# s.add(random_6_bit <= IntVal(int('111111', 2)))

# #  🛰  🌝  🦍  🛰🚀 of 6 bits
# random_6_bit2 = Int("random_6_bit2")
# s.add(random_6_bit2 % vals[keys.index('🛰')] == IntVal(0))
# s.add(random_6_bit2 % vals[keys.index('🌝')] == IntVal(0))
# s.add(random_6_bit2 % vals[keys.index('🦍')] == IntVal(0))
# s.add(random_6_bit2 % vals[keys.index('🚀')] == IntVal(0))
# s.add(random_6_bit2 >= IntVal(int('100000', 2)))
# s.add(random_6_bit2 <= IntVal(int('111111', 2)))

# #  👀  🛰💩  🌎  🥃  💩  📼  📡  🛰 of 6 bits
# random_6_bit3 = Int("random_6_bit3")
# s.add(random_6_bit3 % vals[keys.index('👀')] == IntVal(0))
# s.add(random_6_bit3 % vals[keys.index('🛰')] == IntVal(0))
# s.add(random_6_bit3 % vals[keys.index('💩')] == IntVal(0))
# s.add(random_6_bit3 % vals[keys.index('🌎')] == IntVal(0))
# s.add(random_6_bit3 % vals[keys.index('🥃')] == IntVal(0))
# s.add(random_6_bit3 % vals[keys.index('💩')] == IntVal(0))
# s.add(random_6_bit3 % vals[keys.index('📼')] == IntVal(0))
# s.add(random_6_bit3 % vals[keys.index('📡')] == IntVal(0))
# s.add(random_6_bit3 >= IntVal(int('100000', 2)))
# s.add(random_6_bit3 <= IntVal(int('111111', 2)))

# # 🥃  🤟  🛰  🛰🛸 of 6 bits
# random_6_bit4 = Int("random_6_bit4")
# s.add(random_6_bit4 % vals[keys.index('🥃')] == IntVal(0))
# s.add(random_6_bit4 % vals[keys.index('🤟')] == IntVal(0))
# s.add(random_6_bit4 % vals[keys.index('🛰')] == IntVal(0))
# s.add(random_6_bit4 % vals[keys.index('🛸')] == IntVal(0))
# s.add(random_6_bit4 >= IntVal(int('100000', 2)))
# s.add(random_6_bit4 <= IntVal(int('111111', 2)))

# # 🍌  🦍🥵  🚀  🥃  🧨  🥵  💩  🛰💥  📡  🛰 of 7 bits
# random_7_bit = Int("random_7_bit")
# s.add(random_7_bit % vals[keys.index('🍌')] == IntVal(0))
# s.add(random_7_bit % (vals[keys.index('🦍')] * vals[keys.index('🥵')]) == IntVal(0))
# s.add(random_7_bit % vals[keys.index('🚀')] == IntVal(0))
# s.add(random_7_bit % vals[keys.index('🥃')] == IntVal(0))
# s.add(random_7_bit % vals[keys.index('🧨')] == IntVal(0))
# s.add(random_7_bit % vals[keys.index('🥵')] == IntVal(0))
# s.add(random_7_bit % vals[keys.index('💩')] == IntVal(0))
# s.add(random_7_bit % vals[keys.index('🛰')] == IntVal(0))
# s.add(random_7_bit % vals[keys.index('💥')] == IntVal(0))
# s.add(random_7_bit % vals[keys.index('📡')] == IntVal(0))
# s.add(random_7_bit >= IntVal(int('1000000', 2)))
# s.add(random_7_bit <= IntVal(int('1111111', 2)))

# #  🛰👽  🦍🥃  🧨  🥃  🚀  🛰 for 7 bits
# random_7_bit2 = Int("random_7_bit2")
# s.add(random_7_bit2 % (vals[keys.index('👽')]) == IntVal(0))
# s.add(random_7_bit2 % (vals[keys.index('🦍')] * vals[keys.index('🥃')]) == IntVal(0))
# s.add(random_7_bit2 % vals[keys.index('🧨')] == IntVal(0))
# s.add(random_7_bit2 % vals[keys.index('🥃')] == IntVal(0))
# s.add(random_7_bit2 % vals[keys.index('🚀')] == IntVal(0))
# s.add(random_7_bit2 % vals[keys.index('🛰')] == IntVal(0))
# s.add(random_7_bit2 >= IntVal(int('1000000', 2)))
# s.add(random_7_bit2 <= IntVal(int('1111111', 2)))

# manually found, if not, there will be some ambiguity, e.g. 💯 can be 22 or 26
s.add(vals[keys.index('📡')] == IntVal(4))
s.add(vals[keys.index('💩')] == IntVal(8))
s.add(vals[keys.index('🥵')] == IntVal(16))
s.add(vals[keys.index('🛸')] == IntVal(6))
s.add(vals[keys.index('💽')] == IntVal(12))
s.add(vals[keys.index('🚀')] == IntVal(7))
s.add(vals[keys.index('🌎')] == IntVal(5))
s.add(vals[keys.index('🔥')] == IntVal(11))
s.add(vals[keys.index('🌝')] == IntVal(13))
s.add(vals[keys.index('🧂')] == IntVal(23))
s.add(vals[keys.index('👽')] == IntVal(17))
s.add(vals[keys.index('🤟')] == IntVal(19))
s.add(vals[keys.index('🙌')] == IntVal(29))
s.add(vals[keys.index('👄')] == IntVal(31))


print("constraints added finished")
print(s.check())
model = str(s.model())
print(model)

vals_text = str(model).split("div0")[0].replace("[", "")\
    .replace(" ", "").replace("val", "").replace("\n", "").split(",")
emojis={'🎉': 0, '🛰': 1, '🥃': 2}
keys=list(words.keys())
for a in [a.split('=') for a in vals_text if a != ""]:
    emojis[keys[int(a[0])]] = int(a[1])
print(emojis)

# result
# {'🎉': 0, '🛰': 1, '🥃': 2, '💯': 22, '🧠': 15, '👀': 10, '🥵': 16, '🌛': 30, '🙌': 29, '👽': 17, '🤯': 25, '🌞': 26, '💾': 27, '💽': 12, '🗿': 21, '🚀': 7, 
# '💵': 18, '🌝': 13, '🧨': 14, '💥': 24, '💩': 8, '🤟': 19, '🧂': 23, '🦍': 3, '🔥': 11, '📡': 4, '👄': 31, '🛸': 6, '🌟': 9, '🌎': 5, '📼': 20, '🍌': 28}

# number sys: 0⃣ 1⃣ 2⃣ 3⃣ 4⃣ 5⃣ 6⃣ 7⃣ 8⃣ 9⃣

# -- RSA Signatures part --

transcript = emojis

import pwn


def digit_to_keycap(n: int) -> bytes:
    assert 0 <= n < 10
    return str(n).encode() + b"\xe2\x83\xa3"


def emojis_to_n(emojis: str) -> int:
    n = 0
    for emoji in emojis:
        x = transcript[emoji]
        n = n * 32 + x
    return n


pwn.context.log_level = "debug"

io = pwn.remote("emoji.quals2023.satellitesabove.me", 5300)
io.sendlineafter(
    b"Ticket please:\n",
    b"ticket",
)

io.recvuntil("🇳   🟰   ")
N = io.recvline().strip().decode()

io.recvuntil("🇪   🟰   ")
E = io.recvline().strip().decode()

io.recvuntil("🇨   🟰   ")
C = io.recvline().strip().decode()

n = emojis_to_n(N)
e = emojis_to_n(E)
c = emojis_to_n(C)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")

import Crypto.Util.number as cun

p = pow(c, e, n)

# flag
print(cun.long_to_bytes(p))
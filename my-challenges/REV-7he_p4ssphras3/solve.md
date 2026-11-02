# wp

## 源码分析

题目是关于加密算法, 然后相关区域在 `code` 到 `END`

```assembly
0000000000000208 <code>:
 208: 8c860000  lw a2,0(a0)
 20c: 3c0c9e37  lui t0,0x9e37
 210: 8c830004  lw v1,4(a0)
 214: 3c0bc6ef  lui a7,0xc6ef
 218: 00003825  move a3,zero
 21c: 258c79b9  addiu t0,t0,31161
 220: 256b3720  addiu a7,a7,14112
 224: 00000000  nop

0000000000000228 <T1>:
 228: 00000000  nop
 22c: 01873821  addu a3,t0,a3

0000000000000230 <T2>:
 230: 00000000  nop
 234: 8ca20000  lw v0,0(a1)
 238: 00034142  srl a4,v1,0x5
 23c: 8caa0004  lw a6,4(a1)
 240: 00e34821  addu a5,a3,v1
 244: 006210c5  lsa v0,v1,v0,0x4
 248: 010a4021  addu a4,a4,a6
 24c: 00481026  xor v0,v0,a4
 250: 00491026  xor v0,v0,a5
 254: 00463021  addu a2,v0,a2

0000000000000258 <T3>:
 258: 00000000  nop

000000000000025c <T4>:
 25c: 00000000  nop
 260: 8ca20008  lw v0,8(a1)
 264: 00064142  srl a4,a2,0x5
 268: 8caa000c  lw a6,12(a1)
 26c: 00e64821  addu a5,a3,a2
 270: 00c210c5  lsa v0,a2,v0,0x4
 274: 010a4021  addu a4,a4,a6
 278: 00481026  xor v0,v0,a4
 27c: 00491026  xor v0,v0,a5
 280: 00431821  addu v1,v0,v1

0000000000000284 <T5>:
 284: 00000000  nop

0000000000000288 <END>:
 288: 14ebffe7  bne a3,a7,228 <T1>
 28c: 00000000  nop
 290: ac860000  sw a2,0(a0)
 294: ac830004  sw v1,4(a0)
 298: 03e00009  jr ra
 29c: 00000000  nop

```

可以看出这是一个标准 TEA 算法:

- 9 个加法 2 x `lsa` + 7 x `addu`
- 循环
- xor
- 标准 Delta 值 `0x9e3779b9`

## 波形分析

`data.vcd` 里面主要就是 `alu` 的进位信息, 和 stdout 输出, 可以根据源码和波形看出每一轮会打印一次 `<REDECATED>` 和结束会打印 `HALT`

## 进位信息侧信道

注意到我们助记词都在 `v1` 的位置, `v0` 全是 `xxxx`. 我们只需要分析 `v1` 进行的加法运算, 根据 TEA:

```python
v0 = (v0 << 4) + k[0] ^ v0 + sum ^ (v0 >> 5) + k[1]
```

也就是3次加法的全部进位结果

### 收集全部加法进位

```python
from vcdvcd import VCDVCD

vcd = VCDVCD("data.vcd")

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
```

基本上就是

- 通过 stdout 输出的时机来判断大概轮次时间段
- 算术单元操作数要是 `010` (add)
- PC 要在 TEA 代码范围内
- 注意对于硬件流水线停顿(stall)的情况只记录最后一次(通过如果下一个 PC 和上一个相同就 pop 掉上一个)
- 只保留大于等于 288 次加法的轮次(其他的情况不属于一个有效的 TEA 轮次)
- 读取全部加法器进位拼接到一起

### 进位信息模拟

```python
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

```

### 已知前缀确定偏移量

已知第一个单词是 `flag`, 前两个 key 是 `0xf0f0f0f0` 和 `0x0f0f0f0f`, 以及 sum 的初始值是 Delta `0x9e3779b9`. 通过这些信息我们可以在第一个分段中找到相对于打印的偏移量,然后在其他分段根据这个偏移量找到对应的加法器进位.

```python
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
```

### 根据进位爆破

```python
pflags = [set()] * len(remaining)

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
        ):
            print(f"Found {i} part of the flag: {w}")
            pflags[i].add(w)
        bans.add(w)
    print(
        f"Possible parts for segment {i+1}:",
        pflags[i],
    )
```

### 根据 MD5 确定最终结果

```python
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

```

# RAID Safety Assays, But fixed
## Description
Author: cg

The flag to this challenge is all lowercase, with no underscores.  
```python
e = 65537
n = 4629059450272139917534568159172903078573041591191268130667
c = 6743459147531103219359362407406880068975344190794689965016

main.py:

from Crypto.Util.number import *
import random

p = getPrime(96)
q = getPrime(96)
n = p*q
e = 65537

flag = b'ctf{0000000000000000}'
flag = str(pow(bytes_to_long(flag), e, n))

perm = list(range(10))
random.shuffle(perm)
perm = list(map(str, perm))

c = ''.join([perm[int(x)] for x in flag])

print(f'e = {e}')
print(f'n = {n}')
print(f'c = {c}')
```
## Solution
Since this is a RSA chall, firstly I use `RsaCtfTool` to attack the RSA part:  
```
./RsaCtfTool.py -n 4629059450272139917534568159172903078573041591191268130667 -e 65537 --uncipher 6743459147531103219359362407406880068975344190794689965016 --dump

private argument is not set, the private key will not be displayed, even if recovered.

[*] Testing key /tmp/tmp7t_b98g3.
attack initialized...
attack initialized...
[*] Performing factordb attack on /tmp/tmp7t_b98g3.
[*] Attack success with factordb method !

Results for /tmp/tmp7t_b98g3:
n: 4629059450272139917534568159172903078573041591191268130667
e: 65537
d: 4043019407870016767317373108675128362740498634172596088193
p: 62682123970325402653307817299
q: 73849754237166590568543300233

Public key details for /tmp/tmp7t_b98g3
n: 4629059450272139917534568159172903078573041591191268130667
e: 65537
```  
Therefore, I got all I need for this chall.  
Since the c, cipher, is in different order as it should be. I made a brute-force script for it:  
```python
from Crypto.Util.number import *
from itertools import permutations
e = 65537
n = 4629059450272139917534568159172903078573041591191268130667
d = 4043019407870016767317373108675128362740498634172596088193
p = 62682123970325402653307817299
q = 73849754237166590568543300233

c = 6743459147531103219359362407406880068975344190794689965016
c = str(c)

numbers = list(range(10)) 

all_lists = permutations(numbers, 10)

count = 0
for lst in all_lists:
    l = list(lst)
    cc = int(''.join([str(l.index(int(ccc))) for ccc in c]))
    print(cc)
    # print(count)
    m = pow(cc, d, n)
    ans = long_to_bytes(m)
    if(ans.startswith(b"ctf") or str(m).startswith("6517862")):
        print(count)
        print(ans)
        break
    count += 1

# output:
# ...
# 2549403845098869183903921465462776627350944836534273320682
# 2548403945089968193803821465462776627350844936534273320692
# 2548403645086678163803821475472997729350844637534293320762
# 2549403645096679163903921475472887728350944637534283320762
# 2547403645076687163703721485482998829350744638534293320862
# 2547403645076697163703721495492889928350744639534283320962
# 2549403645096689163903921485482778827350944638534273320862
# 2548403645086698163803821495492779927350844639534273320962
# 2546403845068876183603621475472997729350644837534293320782
# 2546403945069976193603621475472887728350644937534283320792
# 1919965
# b'ctf{cryptpainfulflag}'
```
The flag appeared in 1919965th permutation.  
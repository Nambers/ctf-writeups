# Group Project
## Description
In any good project, you split the work into smaller tasks...  

nc group.chal.uiuc.tf 1337  

Author: Anakin  
## Attachment
chal.py
```python
from Crypto.Util.number import getPrime, long_to_bytes
from random import randint
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


with open("/flag", "rb") as f:
    flag = f.read().strip()

def main():
    print("[$] Did no one ever tell you to mind your own business??")

    g, p = 2, getPrime(1024)
    a = randint(2, p - 1)
    A = pow(g, a, p)
    print("[$] Public:")
    print(f"[$]     {g = }")
    print(f"[$]     {p = }")
    print(f"[$]     {A = }")

    try:
        k = int(input("[$] Choose k = "))
    except:
        print("[$] I said a number...")

    if k == 1 or k == p - 1 or k == (p - 1) // 2:
        print("[$] I'm not that dumb...")

    Ak = pow(A, k, p)
    b = randint(2, p - 1)
    B = pow(g, b, p)
    Bk = pow(B, k, p)
    S = pow(Bk, a, p)

    key = hashlib.md5(long_to_bytes(S)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    c = int.from_bytes(cipher.encrypt(pad(flag, 16)), "big")

    print("[$] Ciphertext using shared 'secret' ;)")
    print(f"[$]     {c = }")


if __name__ == "__main__":
    main()

```
## Solution
We can set `k=0` -> then `Ak = Bk = S = 1`.  
```python
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
g = 2
p = 120373170214735994238329787011767245123671930169635587246273691142366418742122645875746187548614510392312803227098321278331787786301030622666623176128678039473530545034135442178865721012859209331085130345669692792507269271857318000244039984586088651102752172950880965276526415625867302655484376146424554062891
A = 88537922083315761558991322940932850043257126422450195320381048555182982728773716352996143693963033744721377060333325561046831432700097085272880726875078137088607586719536238217441729129531292597657855521384460941830851898929667973971566070914636977020127379270779988492547305115971556200436404671689245009360
k = 0
# Ak = pow(A, k, p)
# b = randint(2, p - 1)
# B = pow(g, b, p)
# Bk = pow(B, k, p)
# S = pow(Bk, a, p)
Ak = 1
Bk = 1
S = 1
key = hashlib.md5(long_to_bytes(S)).digest()
cipher = AES.new(key, AES.MODE_ECB)
c = 31383420538805400549021388790532797474095834602121474716358265812491198185235485912863164473747446452579209175051706
f = 1
while True:
    try:
        print(cipher.decrypt(c.to_bytes(16 * f, 'big')))
        break
    except OverflowError:
        f += 1
```
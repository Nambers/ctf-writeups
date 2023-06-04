# MCV5U
## Description
Author: Ryzon

Ryzon, who just finished his ICS5U class, forgets that he also needs to finish his final MCV5U assignment, which is due on the same day!

Unfortunately, all of Ryzon's brain cells are destroyed due to how scuffed ICS5U is, and he begs you, his friend, to help him finish this assignment for him.

---
SPECIAL NOTE, PLEASE READ

The flag format for this problem is different from the rest, it is: ctf{[!-z]{6,128}} (the part inside the bracket can be any string of 6-128 printable ASCII characters, including letters, numbers, and symbols).
---
## Resources
Rev3.zip
## Solution
For this chall, at first I improve the code little bit:  
```python
def get_sequence(A, B, n, m):
    ans = [0] * (n + m - 1)
    sum = 0
    for x in range(n):
        for y in range(m):
            # ans[x + y] += A[x] * B[y]
            sum += A[x] * B[y]

    return sum
```  
But it still very very slow.  
Then, an idea just pop in my mind: what about change it to C++?  
I just ask ChatGPT to transfer it to cpp code(in [./a.cpp](./a.cpp)) and compile(by `g++ -O3 a.cpp -lcrypto`) it.  
After that, you know what? The program gave my `val=-182933520` in 0m22.357s XDDDD  
Then, I just put that val back to `main.py`(I don't know why my SHA256 result is incorrect) and got the flag.  
## Intended Solution
The intended solution is to use FFT to solve this problem.  
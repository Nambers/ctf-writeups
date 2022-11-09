# Challenge
## Description
I hid the flag somewhere on the website as a 48 byte hex value, so I know you'll never find it. Just, don't check out how the background is calculated.  
https://hambone.chall.pwnoh.io  
Note: the flag will be in lowercase, not uppercase
## Resource
A python script: dist.py
# Step
According to dist.py, the program calculate a hamming distance in a const and input (in 3 * 16 * 8 bits).  
So that, I for-loop each bit and flip them from 0 to 1, and add that hex into url to get the color hex of background color.  

PS:  
At first, I try to make a hex input that minimize background color, but that didn't give me flag.  
So that, I try to make a hex input that maximize background color, and it works.  
# Solution
```python
import requests
import re as regex

def get_result(hexInt: int) -> str:
    real_url = url + hex(hexInt).replace("0x", "")
    headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
    r = requests.get(real_url, headers=headers)
    r.raise_for_status()
    re = regex.findall("<body style=\"background: #(.*?)\">", r.text)
    return re[0]

url = "https://hambone.chall.pwnoh.io/"
default_hex = list("0" * 8 * 16 * 3)
default_re = int(get_result(0x0), 16)
    
for i in range(8 * 16 * 3):
    default_hex[i] = '1'
    hex_int = int(''.join(default_hex), 2)
    re = int(get_result(hex_int), 16)
    if re < default_re:
        default_hex[i] = '0'
    else:
        default_re = re


print(hex(int(''.join(default_hex), 2)))
```

output of `https://hambone.chall.pwnoh.io/ac72c3ecbd95984a48a1890735da8c10b7dd222b9addf2ab7b17778c6b8fc3537852861c969f6738865996481438b29d`:
```
Whoa! How'd you find this? Guess I owe you the flag: buckeye{th3_b4ckgr0und_i5_n0t_4_l13}
```
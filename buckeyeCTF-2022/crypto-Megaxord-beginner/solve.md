# Challenge
## Description
Some pesky wizard stole the article I was writing. I got it back, but it's all messed up now :(  
Hint: the wizard used the same magic on every character...  
## Resource
text file: megaxord.txt
# Step
At first, I try a regular ASCII char shifter (add or minus a character between 0 and 128), but it didn't work.  
After that, I try xor, and it work.  
# Solution
```python
import string
import io
text = io.open('/home/<usr name>/Desktop/megaxord.txt','r', encoding='iso-8859-15').read()
for c in range(0xFF):
    temp = ""
    for a in text:
        t = ord(a) ^ c
        if t < 0:
            break
        temp += chr(t)
    if "buckeye" in temp.replace("\n", "").replace(" ", "").lower():
        print(temp.replace("\n", "").replace(" ", "").lower())
        break
print("end")
``
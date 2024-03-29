# Challenge
## Description
nonce without a cipher
## resources
python encryption script: bonce.py
ciphertext text: output.txt
# Step
In the script, the program just xor each (after 10 line, it will be first 14 bytes) bytes in ciphertext with index of line.  
As we all know, xor operation can be reversed by xor (flag xor key = cipher and cipher xor key = flag).  
Thus, I just re-xor the ciphertext.  
# Solution
```python
texts = """
124 95 95 91 16 89 94 16 68 88 73 16 87 92 81 67 67 28 16 81 94 84 16 68 85 92 92 16 
69 89 84 17 87 80 82 84 17 69 89 94 68 17 71 88 84 70 84 66 69 127 94 70 17 88 66 17 
70 90 87 18 70 91 95 87 18 70 90 83 70 18 84 83 81 87 18 65 90 93 71 94 86 18 84 93 
65 94 19 82 93 92 71 91 86 65 8 100 91 92 64 86 19 85 65 86 64 91 19 65 86 67 82 90 
70 20 93 82 20 90 91 67 20 64 92 91 65 20 90 91 64 20 70 81 90 81 67 81 71 64 24 96 
93 90 64 21 81 90 70 65 21 87 80 82 64 92 89 80 21 65 93 80 21 66 90 71 89 81 25 21 
67 88 84 90 83 69 69 22 69 89 91 83 22 91 89 66 94 83 68 24 112 89 68 22 65 94 83 68 
82 23 94 68 23 68 95 82 23 68 88 23 81 86 94 69 23 64 95 88 68 82 23 66 89 82 86 69 
218 8340 8474 92 24 79 87 85 90 124 81 75 92 89 81 86 75 24 76 80 93 24 76 81 84 84 89 95 
92 25 86 95 25 77 81 64 25 81 76 74 91 88 87 93 75 64 6 118 75 25 78 81 86 25 80 74 
17 88 84 16 66 95 17 86 94 94 85 16 70 89 93 92 17 82 84 16 69 88 84 16 69 95 92 82 
126 87 17 89 88 66 17 66 84 93 87 28 93 94 71 84 29 17 69 94 17 66 69 94 65 17 65 94 
66 70 84 64 88 70 72 13 101 90 94 71 17 83 67 70 17 70 89 75 17 95 94 70 89 87 67 208 
8349 8465 66 19 86 95 80 64 66 31 17 82 95 87 17 64 89 86 17 90 95 19 69 91 84 86 114 82 
93 88 66 20 83 85 82 95 17 64 89 81 17 88 94 66 84 88 72 20 112 68 67 93 93 20 94 82 
17 93 84 71 17 69 67 92 92 80 11 102 94 21 69 93 94 64 17 65 89 71 94 64 86 93 17 66 
88 88 85 89 70 69 17 89 87 22 69 94 88 88 84 22 80 81 84 22 66 94 80 90 93 22 66 83 
84 115 84 68 65 94 69 82 17 88 87 23 70 69 88 89 90 91 84 68 17 67 89 94 66 23 69 95 
72 24 86 87 93 92 84 86 17 76 88 85 84 22 115 77 69 24 88 94 17 76 89 87 68 24 93 81 
83 76 82 82 84 64 84 66 66 86 92 92 110 74 80 64 110 74 94 84 84 95 88 74 89 3 24 68 
68 85 30 16 64 85 95 85 95 82 87 66 208 8348 8464 84 18 94 93 68 18 68 93 16 80 85 30 116 
91 84 18 66 91 95 85 93 87 29 18 80 92 85 18 69 90 88 92 84 18 88 95 80 85 84 18 85 
68 87 30 18 64 87 95 87 95 80 87 64 208 8350 8464 86 18 92 93 70 18 70 93 18 80 87 30 118 
64 19 91 85 18 93 93 68 18 71 90 92 71 19 92 92 70 19 64 86 92 86 69 86 65 71 30 103 
126 91 93 95 18 93 92 20 70 92 75 20 85 88 83 71 65 24 18 85 92 80 18 64 87 88 94 20 
65 65 87 71 91 65 75 10 102 93 93 64 18 84 64 65 18 65 90 76 18 88 93 65 90 80 64 215 
71 88 80 90 87 69 65 22 65 89 95 83 18 91 93 66 90 83 64 24 116 89 64 22 69 94 87 68 
87 23 91 68 18 68 90 82 18 68 93 23 84 86 91 69 18 64 90 88 65 82 18 66 92 82 83 69 
64 85 18 89 92 87 70 80 87 74 9 111 90 87 65 93 18 94 64 93 65 80 18 74 87 72 83 81 
68 92 30 25 64 92 95 92 95 91 87 75 208 8341 8464 93 18 87 93 77 18 77 93 25 80 92 30 125 
65 16 90 86 19 94 92 71 19 68 91 95 70 16 93 95 71 16 65 85 93 85 68 85 64 68 31 100 
65 92 19 80 93 94 71 89 86 67 8 102 91 94 64 84 19 87 65 84 64 89 19 67 86 65 82 88 
86 18 92 84 19 70 91 75 19 90 70 65 81 83 93 86 65 75 12 125 65 18 68 90 92 18 90 65 
86 19 90 64 19 64 91 86 19 64 92 19 85 82 90 65 19 68 91 92 64 86 19 70 93 86 82 65 
86 20 92 82 19 64 91 77 19 92 70 71 81 85 93 80 65 77 12 123 65 20 68 92 92 20 90 71 
95 89 64 21 81 84 80 94 19 65 91 80 19 89 92 67 86 89 74 21 114 69 65 92 95 21 92 83 
86 22 92 80 19 66 91 79 19 94 70 69 81 87 93 82 65 79 12 121 65 22 68 94 92 22 90 69 
69 82 31 23 65 82 94 82 94 85 86 69 209 8347 8465 83 19 89 92 67 19 67 92 23 81 82 31 115 
8351 8474 64 24 84 84 82 75 64 20 19 89 93 92 19 75 91 93 19 81 93 24 71 80 86 93 112 89 
65 84 19 88 93 86 71 81 86 75 8 110 91 86 64 92 19 95 65 92 64 81 19 75 86 73 82 80 
""".split("\n")[1:-1]

for i in range(len(texts)):
    temp = [int(a) for a in texts[i].split(" ")[:-1]]
    nonce = ""
    if i < 10:
        nonce = str(i) * 28
    else:
        nonce = str(i) * 14
    print(''.join([chr(a ^ ord(b)) for a,b in zip(temp, nonce)]))
```
output:
```
Look in thy glass, and tell 
the face thou viewestNow is 
the time that face should fo
rm another;Whose fresh repai
r if now thou not renewest,T
hou dost beguile the world, 
unbless some mother.For wher
e is she so fair whose unear
â€™d wombDisdains the tillag
e of thy husbandry?Or who is
 he so fond will be the tomb
Of his self-love, to stop po
sterity?Thou art thy motherâ
€™s glass, and she in theeCa
lls back the lovely April of
 her prime:So thou through w
indows of thine age shall se
eDespite of wrinkles this th
y golden time.But if thou li
buckeye{some_say_somefish:)}
ve, rememberâ€™d not to be,D
ie single, and thine image d
ve, rememberâ€™d not to be,D
r if now thou not renewest,T
Look in thy glass, and tell 
sterity?Thou art thy motherâ
unbless some mother.For wher
e is she so fair whose unear
rm another;Whose fresh repai
ve, rememberâ€™d not to be,D
r if now thou not renewest,T
rm another;Whose fresh repai
e of thy husbandry?Or who is
e is she so fair whose unear
e of thy husbandry?Or who is
lls back the lovely April of
e of thy husbandry?Or who is
ve, rememberâ€™d not to be,D
€™s glass, and she in theeCa
rm another;Whose fresh repai
```
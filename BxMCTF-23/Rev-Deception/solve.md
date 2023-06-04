# Deception
## Description
Author: Ryzon

One day, one of Ryzon's imaginary friends, Claudio, mysteriously gives him a text file and says that there is secret information within the file that is impossible to retrieve! So much so that he promises to give Ryzon $1,000,000 if he manages to get the info.

However, Claudio is a humongous troll and tries to deceive Ryzon as much as possible by spamming a bunch of useless information.

Can you help Ryzon retrieve the top-secret information? He promises to share the prize money with you if you do!

hint: The hint points to the year of the thing everyone should seek as a clue.
## Resources
Rev1.zip
## Solution
There is only one file in the zip file and obviously encoded with base64. Therefore, I decoded it with `www.base64decode.org`(enable `Decode each line separately (useful for when you have multiple entries).`) and got text in [decoded.txt](./decoded.txt).  
There is a Java program([decoded.java](./decoded.java)) in it with a suspicious link.  
The content in that link is wrote in brainfuck:   
```brainfuck
-[--->+<]>.--[--->+<]>----.+[-->+<]>++.--[
--->++<]>.--[---->+++<]>.--.-----------.+[
--->++++<]>-.--------------.-.------------
--.[--->+<]>--.[--->++<]>+.-.++.[--->+<]>--.>
+[--->++<]>++++.-[----->+<]>--.--[------->+<]
>.[----->+<]>.+++++++++++.[--->+<]>-----.-.++++
++++++.[->+++<]>.+[----->+<]>.>+[--->++<]>.[-->+<
]>+++++.+[->++<]>+.-[--->+<]>+++.+[-->+<]>+++++.-[-
-->+<]>---.-----.++++++++++.>-[--->+<]>.>+[----->+++<]>.-----
---------.++[->++++<]>+.+++++++++++.--[++>---<]>.----[->++<]>
.-------.[----->+<]>.[----->+<]>.++++++++.++++.++.+[->++++<]>
-.-----.[-->+<]>+.+++.+[->++<]>.[--->++<]>+.-.-[->+++++<]>+.++
++.------.++++++++++++.++[->+++<]>++.[-->+++<]>-.>-[------->+<
]>.-.++++++++++.+[----->+<]>-.-[->+++++<]>.-.------.--[++++>---
<]>.+++[->+++<]>.>-[----->+<]>-.-[--->++<]>---.------------.---.-[-
---->+<]>.-[-->+++<]>-.++++.[--->++<]>+.--.+++++++.[----->+<]>.[->++
+<]>+.+++++++++++.[->+++<]>.[--->+<]>--.>+[--->++<]>+++.>-[----->+<]>
.+++[-->+++<]>.>+[----->+++<]>.-------------.+[->++++<]>+.+++++++++++
.[->+++<]>.--------------.[--->++++<]>+.--.[----->+<]>.+++++++++++.---
------------.-[-->+++<]>-.++++.----------.+++++++.++[->+++<]>+.[--->++
<]>++++.[->++<]>+.[->++++++<]>+.>+[--->++<]>.>-[----->+<]>++.-[----->+
+<]>+.-.++++++.-[--->+<]>.-------------.[-->+<]>++.>+[--->++<]>.[--->+
<]>+.[->+++<]>+.-[----->+<]>--.-.-----[->++<]>.--[-
--->+++<]>.---.-.[--->+<]>.[----->+<]>-.-.+++++++++
+.--[--->+<]>-.[------->+<]>+.-------.--[->++++<]>-
-.>+[--->++<]>.++++++++++++.+++++++++++.-.[-->+<]>-
-.[----->++<]>+.----.>+[--->++<]>.---[----->+<]>.-[
->+++<]>.[-->+<]>+.++[-->+++<]>.-[--->+<]>.[--->++<
]>-.--.-.>----[-->+++<]>.>-[------->+<]>.--.--.-[--
>+++<]>+.--------------.>-[----->+<]>-.++[--->++<]>
.--[++>---<]>.----[->++<]>.---------.--[->++++<]>+..
```  
After compile and execute it, I got a base64 encoded string: `Um9zZXMgYXJlIHJlZCwKVmlvbGV0cyBhcmUgYmx1ZSwKSWYgb25lIHdhbnRzIHRvIHBpY2sgdGhlIGNvcnJlY3QgZmxhZywKVGhlbiB0aGV5IHNob3VsZCBzZWVrIHRoZSBVbml4IEVwb2NoIGFzIGEgY2x1ZQ==`  
After decoded it, I got a poem:  
```
Roses are red,
Violets are blue,
If one wants to pick the correct flag,
Then they should seek the Unix Epoch as a clue
```  
Combined `Unix Epoch` in it and the `year of the thing` in hint, I got 1970 as clue.  
It is not the input of the java program, because the input must < 1106(the table length).  
Then, it can be a part of the flag.  
Therefore, I just print all possible flags(in [flags.txt](./flags.txt)) and search 1970 in those flag to get the real flag.  

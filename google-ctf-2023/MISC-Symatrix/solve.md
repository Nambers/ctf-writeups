# Symatrix
## Description
The CIA has been tracking a group of hackers who communicate using PNG files embedded with a custom steganography algorithm.   
An insider spy was able to obtain the encoder, but it is not the original code.   
You have been tasked with reversing the encoder file and creating a decoder as soon as possible in order to read the most recent PNG file they have sent.  
## Attachments and official writeup
[https://github.com/google/google-ctf/tree/54f15c51f4b0267288f42274e8064fb2603da2ab/2023/misc-symatrix](https://github.com/google/google-ctf/tree/54f15c51f4b0267288f42274e8064fb2603da2ab/2023/misc-symatrix)
## Solution
1. use [extract.py](./extract.py) to extract origin encoder.py from `encoder.c`(in the comments)  
2. use rules from `encoder.py` to extract the flag from png.  
[solve script](./solve.ipynb)  
# Neddle in the Wifi Stack
## Resource
`frames.pcap` - pcap file
## Author
arcsolstice
## Solution
After open the pcap file, we can see the `SSID` value of every `IEEE 802.11` packets are encoded in base64. Therefore we can just simply decode the `SSID` value and get the flag by searching `bctf`.  
solve.py  
```python
from dpkt import pcap
import base64
text = []
for ts, pkt in pcap.Reader(open('frames.pcap', 'rb')):
    # the SSID has fixed offset
    text.append(base64.b64decode(pkt[15 + 0x20 - 1: -(0x20 - 6)]).decode())

with open("text.txt", "w") as f:
    f.write("\n".join(text))

```
# Challenge
## Description
I dug up my first ever JavaScript game, but this time, my AI is unbeatable!! Hah!  
https://pong.chall.pwnoh.io  
# Step
After I check the source code (by Chrome inspect), I figure out that this website construct a socket and just use `emit("score", val)` to communicate backend.
# Solution
repeat execute in chrome -> inspect -> console
```JavaScript
socket.emit("score", 999999);
```
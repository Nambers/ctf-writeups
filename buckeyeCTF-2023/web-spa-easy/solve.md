# SPA
## Description
Enjoy a relaxing visit to our spa.

https://spa.chall.pwnoh.io
## Author
mbund
## Solution
> This is just a tricky challenge.
0. By auditing the Network tab of Chrome DevTools, we can find that the program send some requests to `isAdmin`.
1. Then just globally search `admin`.
2. By auditing the javascript file that `admin` search result located, we can find that there is a weird base64: `ag = YmN0Zns3aDNfdWw3MW00NzNfNXA0XzE1XzRfcjM0YzdfNXA0fQo`.
3. Decode it and we can get the flag.
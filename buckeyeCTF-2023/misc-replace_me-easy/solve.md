# Replace me
## Description
I knew I shouldn't have gotten a cheap phone :/
## Author
rene
## Resources
`dist` - An android bootimg file (detected by `binwalk`)
## Solution
0. it is a Android bootimg file (by `binwalk`)
1. By doing some search on internet, we can use tool from [tool-boot-img-tools-unpack-repack-ramdisk](https://forum.xda-developers.com/t/tool-boot-img-tools-unpack-repack-ramdisk.2319018/) to extract it(by executing `./bootimg_tools/split_boot dist.img`)
2. Open the suspicious zip file, find the image in `res` folder (and it is the flag). The reason of that I firstly check the resource folder is that `res` folder is most suspicious folder than others.
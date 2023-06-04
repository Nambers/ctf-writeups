# Selfie
## Description
Author: clides

One day, clides secretly plugged a rubber ducky into Claudio Pacheco's laptop and gained control. While browsing through his files, he found this selfie which contains some secret information.

Can you help him find the secret information hidden in the selfie?
## Resources
BxMCTF-Foren-1.jpg
## Solution
use `exiftool BxMCTF-Foren-1.jpg`:  
```
ExifTool Version Number         : 12.40
File Name                       : BxMCTF-Foren-1.jpg
Directory                       : .
File Size                       : 68 KiB
File Modification Date/Time     : 2023:05:21 16:46:28+08:00
File Access Date/Time           : 2023:06:04 16:32:13+08:00
File Inode Change Date/Time     : 2023:06:04 16:32:00+08:00
File Permissions                : -rwxrwxrwx
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
Exif Byte Order                 : Big-endian (Motorola, MM)
XMP Toolkit                     : Image::ExifTool 12.60
License                         : Y3Rme25xaUoyQnQyaVZEa2d6fQ
Image Width                     : 1241
Image Height                    : 1157
Encoding Process                : Progressive DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 1241x1157
Megapixels                      : 1.4
```  
decoded license with base64 is the flag.  


# Street View
## Description
Author: clides

One day, clides was doing some detective work to try to catch the person who stole the 2 rubber duckies from the BxMCTF prize pool. He was doing some OSINT and he stumbled upon this street view image from ClaudsVille on Dread. Apparently, this image was sent from the thief.

Can you help clides to find out where the image was taken?

foren2.zip

Submit the domain name of the company that owns the building as the flag, wrapped in ctf{}
## Resources
BxMCTF-Foren-2.png
## Solution
Use `exiftool` in that image:  
```
ExifTool Version Number         : 12.40
File Name                       : BxMCTF-Foren-2.png
Directory                       : .
File Size                       : 1158 KiB
File Modification Date/Time     : 2023:05:21 16:56:04+08:00
File Access Date/Time           : 2023:06:04 15:16:50+08:00
File Inode Change Date/Time     : 2023:06:04 15:16:18+08:00
File Permissions                : -rwxrwxrwx
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 1203
Image Height                    : 709
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Exif Byte Order                 : Big-endian (Motorola, MM)
XMP Toolkit                     : Image::ExifTool 12.60
Latitude                        : 43 deg 52' 38.32" N
Longitude                       : 79 deg 24' 31.00" W
Image Size                      : 1203x709
Megapixels                      : 0.853
```  
We can have latitude and longitude.  
Search this latt and longt in Google Map, we can find the location is in Canada with a Walmart.  
Therefore, the flag is `ctf{walmart.ca}`
import re
with open("encoder.c", "r") as f:
    codes = f.read()
    # extract all code in comment like this:
    #     /* "encoder.py":5
    #  * import binascii
    #  * 
    #  * def hexstr_to_binstr(hexstr):             # <<<<<<<<<<<<<<
    #  *     n = int(hexstr, 16)
    #  *     bstr = ''
    #  */
    # also need line number after "encoder.py"
    codes = re.findall(r'\/\* "encoder\.py":(.*?)\n(.*?)\n\s*\*\/', codes, re.DOTALL)
    # all code, preallocate 100 lines
    codesArr = [None] * 100
    for line, code in codes:
        num = int(line)
        for c in code.split("\n"):
            codesArr[num] = c
            num += 1
    # then, join all codes into str
    codes = "\n".join([x for x in codesArr if x is not None])
    # remove all *
    codes = codes.replace(" * ", "")
    # and write to encoder.py
    with open("encoder.py", "w") as f:
        f.write(codes)

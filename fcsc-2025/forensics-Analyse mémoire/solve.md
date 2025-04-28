# Analyse mémoire

## Description

An FCSC agent starts their computer to brainstorm and jot down challenge ideas for next year. However, they reported that during startup, a strange red screen briefly appeared for just a second, then the system booted normally.

They were able to start working without any issues, but to ensure the problem isn’t caused by potential malware, we had them capture the system’s memory using the DumpIt tool. Analyze the memory and identify the malware attempting to exfiltrate the document.

## Solution

### 1 Exfiltration

Is `rundll32.exe` because in the result of `vol -f analyse-memoire.dmp windows.netscan` there is an entry of `rundll32.exe` and the cmdline of starting this executable is not valid for original executable.  
Also `rundll32.exe` is not suppose to make any http connection.  
Thus the answer is `TCP` connection `100.68.20.103:443`, `rundll32.exe`, `PID` is `1800`: `FCSC{rundll32.exe:1800:100.68.20.103:443:TCP}`.

### 2 Origine de la menace

Use `sudo vol -f analyse-memoire.dmp windows.psscan` to get `PPID` of `PID=1800` which is `936` and `svchost.exe`: `FCSC{svchost.exe:936}`.

### 3 Où est le pansement

I didn't make it in the contest but here are some of my tries:

```python
>>> "%016x" % 0x2244e9a0000
'000002244e9a0000'
>>> "%016x" % 0x2244dde0000
'000002244dde0000'
```

```log
> vol -f analyse-memoire.dmp windows.vadyarascan --pid 1800 --yara-file  malware_rules.yar
Volatility 3 Framework 2.11.0
Progress:  100.00               PDB scanning finished                                
Offset  PID     Rule    Component       Value

0x2244dde02c5   1800    Cobalt_functions        $h1     58 a4 53 e5
0x2244dde011e   1800    Cobalt_functions        $h2     4c 77 26 07
0x2244dde029b   1800    Cobalt_functions        $h4     44 f0 35 e0/
```

NO:
- `FCSC{1804:0x000002244e9a0000}`
- `FCSC{1804:0x000002244dde0000}`
- `FCSC{1804:0x000002244e9a0000}`
- `FCSC{7372:0x000002244dde0000}`

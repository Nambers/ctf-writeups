# Intended Solve

The intended solve is a real PACMAN / Spectre attack purely over a D-cache timing side channel: the core has a PAC-gated load gadget. Run it speculatively on a mispredicted branch — a good tag fills a user-owned PROBE line, a bad tag is NO_LOAD and, drained as speculative, never commits a fault. Time a PROBE reload to tell a correct guess (cache hit) from a wrong one (miss); recover the 8-bit tag silently in a single run, then jr {tag,0x2030} authenticates the gate and the kernel prints the flag.

## Some writeups

- <https://cybersecurityelite.com/ctf-writeups/r3ctf-2026-writeup/#2-blinky>
- <https://github.com/hax1ng/r3ctf-2026-writeups/blob/master/misc/Blinky.md>

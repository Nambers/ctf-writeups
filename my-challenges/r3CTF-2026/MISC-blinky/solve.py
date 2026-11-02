#!/usr/bin/env python3
r"""Reference solver / healthcheck client for the Blinky R3CTF challenge.

Submits the reference exploit -- a single-run recovery of the 8-bit PAC tag of the
kernel_flag VA (0x2030) via a D-cache TIMING side channel (see solve/ref.s) -- to
the challenge server and prints the response. The server splices it onto the secret
kernel (per-run random PAC key) and runs it; on a healthy instance the recovered tag
authenticates the gate and the kernel prints the flag.

  SERVER   base URL of the challenge server   (default: http://127.0.0.1:8080)
  EXPECT   flag-shaped regex to require        (default: R3CTF{...} or FLAG{...})
  TIMEOUT  request timeout, seconds            (default: 180)

Exit 0 iff a flag came back, 1 if the server answered without one, 2 on transport
error. Stdlib only.
"""
import os
import re
import sys
import urllib.request

HERE    = os.path.dirname(os.path.abspath(__file__))
SERVER  = os.environ.get("SERVER", "http://127.0.0.1:8080").rstrip("/")
EXPECT  = os.environ.get("EXPECT", r"(?i)(?:r3ctf|flag)\{[^}]*\}")
TIMEOUT = int(os.environ.get("TIMEOUT", "180"))
REF_MEM = os.environ.get("REF_MEM", os.path.join(HERE, "ref.mem"))


def main():
    with open(REF_MEM, "rb") as f:
        body = f.read()
    url = SERVER + "/submit"
    print("[*] submitting reference exploit (%s) to %s ..." % (
        os.path.basename(REF_MEM), url))
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/octet-stream"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            out = resp.read().decode("utf-8", "replace")
    except Exception as e:  # noqa: BLE001 -- healthcheck: report and fail
        print("[-] request failed: %s" % e)
        return 2
    print("[*] server response:")
    print(out.rstrip())
    m = re.search(EXPECT, out)
    if m:
        print("[+] flag: %s" % m.group(0))
        return 0
    print("[-] no flag matching /%s/ in response" % EXPECT)
    return 1


if __name__ == "__main__":
    sys.exit(main())
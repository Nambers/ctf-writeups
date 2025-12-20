from vcd import VCDWriter
from vcdvcd import VCDVCD

white_list = [
    "TOP.SOC.stdout_taken",
    "TOP.clk",
    "TOP.reset",
    "TOP.SOC.stdout.w_data[63:0]",
    "TOP.SOC.core.EX_stage.alu_.alu_op[2:0]",
    "TOP.SOC.core.EX_stage.alu_.au_0.adder_0.cout",
    "TOP.SOC.core.next_fetch_pc[63:0]",
    "TOP.SOC.core.ID_stage.stall",
] + [f"TOP.SOC.core.EX_stage.alu_.au_0.genblk1[{k}].adder_0.cout" for k in range(1, 64)]

vcd_read = VCDVCD("trace.vcd")

with VCDWriter(open("data.vcd", "w")) as writer:
    white_vars = []
    changes = []
    for sig in white_list:
        white_vars.append(
            writer.register_var(
                ".".join(sig.split(".")[:-1]),
                sig.split(".")[-1],
                "logic",
                size=len(vcd_read[sig].tv[0][1]),
            )
        )
    for sig in white_list:
        sigs = vcd_read[sig].tv
        var = white_list.index(sig)
        for timestamp, value in sigs:
            # value is a list of characters '0' or '1'
            changes.append((int(timestamp), var, "".join(value)))
    changes = sorted(changes, key=lambda x: x[0])
    for change in changes:
        writer.change(white_vars[change[1]], change[0], change[2])

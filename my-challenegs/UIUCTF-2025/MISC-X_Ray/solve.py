from vcdvcd import VCDVCD
import string

vcd = VCDVCD('trace.vcd')

# List all human readable signal names.
# print(vcd.references_to_ids.keys())
flag = ""
for t, v in vcd["TOP.SOC.core.MEM_stage.W_data[63:0]"].tv:
# for i, (t, v) in enumerate(vcd["TOP.SOC.core.MEM_stage.mem.data_in[63:0]"].tv):
    flag += ''.join([c for c in int(v, 2).to_bytes(8, 'little').decode("ascii", errors="ignore") if c in string.ascii_letters + string.digits + "{}_"])

print(flag)

import os

def check_flag(flag):
    flag = [flag[i:i + 4].encode().hex().ljust(8, '0') for i in range(0, len(flag), 4)]
    flag = [" ".join([a[i:i + 2] for i in range(0, len(a), 2)]) + "\n" for a in flag]

    with open("dist/memory.mem", "r") as f:
        lines = f.readlines()
        lines[3:len(flag) + 3] = flag[:]
    with open("memory.mem", "w") as f:
        f.writelines(lines)

    os.system("./dist/SOC_run_sim")
    os.system("rm memory.mem")

print("check correct flag")
check_flag("uiuctf{U_Uctf_m1psl0ver#0d00_abcdefghi}")
print("check wrong flag")
check_flag("uiuctf{U_Uctf_m1psl0ver#1d00_abcdefghi}")
check_flag("uiuctf{U_Uctf_m1psl0ver#0AR1_abcdefghi}")
# len
check_flag("uiuctf{U_Uctf_m1psl0ver#0d00_abcdefgh}")
check_flag("uiuctf{U_Uctf_m1psl0ver#0d00_abcdefgha}")
check_flag("uiuc1f{U_Uctf_m1psl0ver#0d00_abcdefghi}")
check_flag("uiuc1f{1_Uctf_m1psl0ver#0d00_abcdefghi}")


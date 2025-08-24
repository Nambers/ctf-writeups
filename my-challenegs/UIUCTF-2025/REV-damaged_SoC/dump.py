#!/usr/bin/env python3
import sys

def verilog_to_bin(input_file, output_file):
    memory_data = {}
    current_addr = 0
    
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line.startswith('@'):
            # addr
            current_addr = int(line[1:], 16)
            i += 1
        else:
            # 4 bytes per line
            bytes_data = [int(x, 16) for x in line.split()]
            for byte_val in bytes_data:
                memory_data[current_addr] = byte_val
                current_addr += 1
            i += 1
    
    with open(output_file, 'wb') as f_out:
        min_addr = min(memory_data.keys())
        max_addr = max(memory_data.keys())
        
        for addr in range(min_addr, max_addr + 1):
            byte_val = memory_data.get(addr, 0)
            f_out.write(bytes([byte_val]))


verilog_to_bin("memory.mem", "memory.bin")
# decompile with Mips64el

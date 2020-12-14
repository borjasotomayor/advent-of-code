"""
Day 14
https://adventofcode.com/2020/day/14

1st star: 00:12:14
2nd star: 00:30:39

Always fun to play around with bitmasks, although I ended up using
strings for the second part (and I'm kinda wondering whether there's
a way to do the second part with bitmasks too).
"""

import util
import math
import sys
import re

from util import log


def expand_floating(bin_str):
    """
    Recursively expands a binary string with 
    floating ("X") digits into a list of integers.
    """    
    if len(bin_str) == 0:
        return [0]
    else:
        exp = len(bin_str) - 1
        digit = bin_str[0]

        # Recursively obtain the list of values
        # from the rest of the string (minus the
        # first digit)
        rem_values = expand_floating(bin_str[1:])

        # Create return list
        rv = []
        for r in rem_values:
            if digit in ("0", "X"):
                rv.append(r)
            if digit in ("1", "X"):
                rv.append(2**exp + r)

        return rv


def update_memory(commands, version=1):
    mem = {}
    for cmd in commands:
        if cmd.startswith("mask ="):
            log(cmd)
            mask = cmd[7:]

            # For version 1, we create bitmasks that allow
            # us to do the necessary flips using bitwise AND
            # and OR operations.
            zeros_mask = mask.replace("X", "1")
            ones_mask = mask.replace("X", "0")
            zeros_mask = int(zeros_mask, 2)
            ones_mask = int(ones_mask, 2)
        elif cmd.startswith("mem["):
            addr, value = cmd.split(" = ")
            addr = int(addr[4:].replace("]",""))
            value = int(value)

            if version == 1:
                # Apply bitmasks to obtain actual value
                value = value & zeros_mask
                value = value | ones_mask

                log(f"mem[{addr}] = {value}")
                mem[addr] = value
            elif version == 2:
                # Apply mask
                bin_value = format(addr, '036b')
                new_value = ""
                for digit, mask_digit in zip(bin_value, mask):
                    if mask_digit in ("1", "X"):
                        new_value += mask_digit
                    elif mask_digit == "0":
                        new_value += digit
                    
                addrs = expand_floating(new_value)

                for addr in addrs:
                    log(f"mem[{addr}] = {value}")
                    mem[addr] = value

    return sum(mem.values())


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/14-1.in", sep="\n")
    sample2 = util.read_strs("input/sample/14-2.in", sep="\n")
    commands = util.read_strs("input/14.in", sep="\n")

    print("TASK 1")
    util.call_and_print(update_memory, sample1, 1)
    util.call_and_print(update_memory, commands, 1)

    print("\nTASK 2")
    util.call_and_print(update_memory, sample2, 2)
    util.call_and_print(update_memory, commands, 2)

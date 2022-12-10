"""
Day 10
https://adventofcode.com/2022/day/10

1st star: 00:20:16
2nd star: 00:30:40

This was a really nice problem (based on the real operation
of CRT monitors), but I lost a lot of time because I 
misinterpreted how the cycles worked in the first task.
"""

import util
import math
import sys
import re

from util import log


def crt(program):
    """
    Compute the signal strength and image produced by the CRT monitor
    """

    # Register
    X = 1

    # To be able to iterate through all the cycles,
    # we use these variables to keep track of the next 
    # cycle in which we would have to execute an operation,
    # as well as whether we need to add a value to X
    # during that cycle.
    next_op_cycle = 1
    next_op_add = None

    # Used to compute the strengths and the lines
    # we'll be displaying.
    strength = 0
    lines = []
    line = []

    for i in range(240):
        cycle = i + 1
        pos = i % 40

        # If we still have instructions left to run
        # and we are in the next_op_cycle
        if len(program) > 0 and cycle == next_op_cycle:
            # If there's a pending add operation, do it
            if next_op_add is not None:
                X += next_op_add
                next_op_add = None

            instr = program.pop(0)

            op = instr[0]
            if op == "noop":
                next_op_cycle = cycle + 1
            elif op == "addx":
                v = int(instr[1])
                next_op_cycle = cycle + 2
                next_op_add = v

        # Draw a pixe if the sprite overlaps with the 
        # current position...
        if X-1 <= pos <= X+1:
            line.append("#")
        else:
            line.append(".")

        # After 40 cycles, start a new line
        if cycle % 40 == 0:
            lines.append(line)
            line = []

        # In cycles 20, 60, 80, etc. update the strength
        if (cycle + 20) % 40 == 0:
            strength += cycle * X

    return strength, lines


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/10.in", sep="\n", sep2=" ")
    input = util.read_strs("input/10.in", sep="\n", sep2=" ")

    print("TASK 1")
    strength, lines_sample = crt(sample)
    print(f"Sample strength is {strength}")
    strength, lines_input = crt(input)
    print(f"Inpout strength is {strength}")

    print("\nTASK 2")
    print("Sample:")
    for l in lines_sample:
        print("".join(l))
    print("\nInput:")
    for l in lines_input:
        print("".join(l))
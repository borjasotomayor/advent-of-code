"""
Day 2
https://adventofcode.com/2021/day/2

1st star: 00:01:57
2nd star: 00:04:07

A fun little command-parsing problem. My original solution had
two separate functions for each task for the sake of expediency,
but I cleaned them up and refactored them into a single function.
"""

import util
import math
import sys
import re

from util import log


def submarine(commands, use_aim=False):
    """
    Process the given submarine commands.

    If use_aim is true, use the aim to compute the
    depth changes.
    """
    horizontal = 0
    depth = 0
    aim = 0
    for cmd in commands:
        direction, X = cmd.split()
        X = int(X)

        if direction == "forward":
            horizontal += X
            if use_aim:
                depth += aim * X
        elif direction == "down":
            aim += X
            if not use_aim:
                depth += X
        elif direction == "up":
            aim -= X
            if not use_aim:
                depth -= X
        
    return horizontal * depth


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/02.in", sep="\n")
    input = util.read_strs("input/02.in", sep="\n")

    print("TASK 1")
    util.call_and_print(submarine, sample)
    util.call_and_print(submarine, input)

    print("\nTASK 2")
    util.call_and_print(submarine, sample, True)
    util.call_and_print(submarine, input, True)
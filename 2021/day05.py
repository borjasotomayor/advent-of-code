"""
Day 5
https://adventofcode.com/2021/day/5

1st star: 00:09:46
2nd star: 00:20:39

My first approach to this problem treated horizontal, vertical, and
diagonal lines as three distinct cases (with lots of repeated code
across the three cases), so once I got the stars, this became a 
nice exercise in refactoring. I ended up with a function that
treats all lines the same way by figuring out the "step" that,
if added repeatedly to (x1, y1), will get your to (x2, y2)
"""

import util
import math
import sys
import re

from util import log, read_strs


def read_input(input):
    """
    Reads in the problem's input
    """
    lines = []
    for x1, y1, x2, y2 in util.iter_parse(input, "{:d},{:d} -> {:d},{:d}"):
        lines.append((x1, y1, x2, y2))
    return lines


def count_line_coordinates(lines, include_diagonals=False):
    """
    Counts the coordinates that a series of lines passes through
    """

    # We count up the coordinates with a dictionary
    coords = {}

    for x1, y1, x2, y2 in lines:
        # If this line is diagonal, but we're not including diagonals,
        # skip the line
        if not (x1 == x2 or y1 == y2) and not include_diagonals:
            continue
        
        # Find the step
        x_step = 0 if x2 == x1 else (1 if x2-x1 > 0 else -1)
        y_step = 0 if y2 == y1 else (1 if y2-y1 > 0 else -1)

        # Find the length of the line
        # (this is the number of times we need to add the step
        # to x1, y1 to get to x2, y2)
        line_len = max(abs(x2-x1), abs(y2-y1)) + 1

        for i in range(line_len):
            location = (x1 + i*x_step, y1 + i*y_step)
            coords[location] = coords.get(location, 0) + 1

    return coords


def do_task(input, include_diagonals=False):
    """
    Does the task (with or without diagonals)
    """
    lines = read_input(input)
    coords = count_line_coordinates(lines, include_diagonals)

    n = 0
    for v in coords.values():
        if v >= 2:
            n += 1
    return n


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/05.in", sep="\n")
    input = util.read_strs("input/05.in", sep="\n")

    print("TASK 1")
    util.call_and_print(do_task, sample)
    util.call_and_print(do_task, input)

    print("\nTASK 2")
    util.call_and_print(do_task, sample, True)
    util.call_and_print(do_task, input, True)

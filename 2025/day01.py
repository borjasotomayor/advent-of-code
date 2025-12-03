"""
Day 1
https://adventofcode.com/2025/day/1
"""

import util
import math
import sys
import re

from util import log


def count_zeroes(rotations: list[str], only_at_end: bool):
    """
    Count the number of zeroes we land on after each
    rotation (optionally includng the zeroes we pass)
    """
    cur = 50

    zeroes_at_end = 0
    total_zeroes_passed = 0

    for rot in rotations:
        dir = rot[0]
        clicks = int(rot[1:])

        if dir == "R":
            zeroes_passed = (cur + clicks) // 100
            cur = (cur + clicks) % 100
            
            # If we landed on 0, the formula for
            # zeroes_passed overshoots by one
            if cur == 0:
                zeroes_passed -= 1
        elif dir == "L":
            zeroes_passed = abs((cur - clicks) // 100)
            
            # If we started at 0, the formula for zeroes_passed
            # overshoots by one
            if cur == 0:
                zeroes_passed -= 1
            
            cur = (cur - clicks) % 100

        log(f"The dial is rotated {rot} to point at {cur}.")

        if cur == 0:
            zeroes_at_end += 1

        if zeroes_passed > 0:
            log(f"    and the dial passed through zero {zeroes_passed} times")

        total_zeroes_passed += zeroes_passed


    if only_at_end:
        return zeroes_at_end
    else:
        return zeroes_at_end + total_zeroes_passed


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/01.in", sep="\n")
    input = util.read_strs("input/01.in", sep="\n")

    print("TASK 1")
    util.call_and_print(count_zeroes, sample, True)
    util.call_and_print(count_zeroes, input, True)

    print("\nTASK 2")
    util.call_and_print(count_zeroes, sample, False)
    util.call_and_print(count_zeroes, input, False)

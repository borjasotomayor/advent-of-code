"""
Day 1
https://adventofcode.com/2022/day/X

1st star: 00:02:56
2nd star: 00:04:23

As usual, a nice and simple fun little problem to get started.
Lost a bit of time on the parsing so, when cleaning up the code,
took the opportunity to improve my read_strs and read_ints functions
so they can deal with groups of tokens.
"""

import util
import math
import sys
import re

from util import log


def sum_top_n(groups, n=1):
    """
    Given a list of groups (where each group is a list of integers),
    find the sum of the values in each group, and then add up the top N
    groups.
    """
    sums = []
    for group in groups:
        sums.append(sum(group))

    top_n = sorted(sums, reverse=True)[:n]

    return sum(top_n)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/01.in", sep="\n\n", sep2="\n")
    input = util.read_ints("input/01.in", sep="\n\n", sep2="\n")

    print("TASK 1")
    util.call_and_print(sum_top_n, sample)
    util.call_and_print(sum_top_n, input)

    print("\nTASK 2")
    util.call_and_print(sum_top_n, sample, 3)
    util.call_and_print(sum_top_n, input, 3)

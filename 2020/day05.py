"""
Day 5
https://adventofcode.com/2020/day/5

1st star: 00:09:58
2nd star: 00:13:15

This problem is fairly straightforward when you realize the row and column
numbers are just binary numbers (where F=0, B=1, L=0, R=1). My original
solution used a loop to add up the powers of two, but I changed it
afterwards to use Python's builtin casting from binary strings to integers.

Not gonna lie, for the second star I originally just printed out the
sorted id numbers on the terminal to get a better sense of what they
looked like, and then did a set difference between the id numbers and
set(range(78,892)). I polished up the code afterwards to be more general
purpose (my first approach involved using sets, but I also came up
with a version that avoids having to use sets, which would be more
efficient for large inputs)
"""

import util
import math
import sys
import re

from util import log


def decode(string, zero_char, one_char):
    """
    Convert a binary string to an integer,
    where zero_char represents zeroes and
    one_char represents ones.
    """
    binary_str = string.replace(zero_char, "0").replace(one_char, "1")

    return int(binary_str, 2)


def get_ids(boarding_passes):
    seat_ids = []
    for boarding_pass in boarding_passes:
        row_str = boarding_pass[:7]
        col_str = boarding_pass[7:]

        row = decode(row_str, "F", "B")
        col = decode(col_str, "L", "R")

        seat_id = row * 8 + col

        seat_ids.append(seat_id)

    return seat_ids


def task1(boarding_passes):
    ids = get_ids(boarding_passes)

    return max(ids)


def task2(boarding_passes):
    ids = get_ids(boarding_passes)

    min_id = min(ids)
    max_id = max(ids)

    all_ids = set(range(min_id, max_id + 1))

    missing = all_ids - set(ids)

    assert len(missing) == 1

    return missing.pop()


def task2_alt(boarding_passes):
    """
    Alternative implementation that avoids using sets:
    Add up all the ids between the minimum and maximum id
    (this can be done with a simple formula), add up all
    the ids from the input, and get the difference.
    """
    ids = get_ids(boarding_passes)

    min_id = min(ids)
    max_id = max(ids)

    sum_all_ids = ((max_id - min_id + 1)/2) * (min_id + max_id)
    sum_ids = sum(ids)

    return int(sum_all_ids) - sum_ids    


if __name__ == "__main__":
    util.set_debug(False)

    boarding_passes = util.read_strs("input/05.in", sep="\n")

    print("TASK 1")
    util.call_and_print(decode, "FBFBBFF", "F", "B")
    util.call_and_print(decode, "RLR", "L", "R")
    util.call_and_print(decode, "BFFFBBF", "F", "B")
    util.call_and_print(decode, "RRR", "L", "R")
    util.call_and_print(decode, "FFFBBBF", "F", "B")
    util.call_and_print(decode, "RRR", "L", "R")
    util.call_and_print(decode, "BBFFBBF", "F", "B")
    util.call_and_print(decode, "RLL", "L", "R")

    util.call_and_print(task1, ["FBFBBFFRLR"])

    util.call_and_print(task1, boarding_passes)

    print("\nTASK 2")
    util.call_and_print(task2, boarding_passes)
    util.call_and_print(task2_alt, boarding_passes)



"""
Day 3
https://adventofcode.com/2022/day/3

1st star: 00:05:59
2nd star: 00:10:05

Python sets FTW! My original solution had some very ad-hoc
code for each of the tasks, but then I cleaned it up
by writing a single function that can handle both tasks.
"""

import util
import math
import sys
import re

from util import log

def to_priority(c):
    """
    Converts a character to a priority code
    """
    if c.islower():
        return ord(c) - ord("a") + 1
    elif c.isupper():
        return ord(c) - ord("A") + 27

def sum_priorities(rucksacks, group_size=None):
    """
    Given a list of rucksacks, divide them up into groups
    find the common element in each group, and add up the
    priorities of each common element.
    """

    groups = []
    if group_size is None:
        # If no group size is specified, each
        # group contains the two halves of a rucksack
        for r in rucksacks:
            mid = len(r)//2
            groups.append([set(r[:mid]), set(r[mid:])])
    else:
        # Otherwise, we group the rucksacks in groups
        # of the specified size
        assert len(rucksacks) % group_size == 0

        for i in range(0, len(rucksacks), group_size):
            group = [set(r) for r in rucksacks[i:i+group_size]]
            groups.append(group)

    # Find the common element in each group,
    # and add up the priorities
    total_priorities = 0
    for group in groups:
        common = set.intersection(*group)
        
        assert len(common) == 1
        common = common.pop()

        total_priorities += to_priority(common)

    return total_priorities



if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/03.in", sep="\n")
    input = util.read_strs("input/03.in", sep="\n")

    print("TASK 1")
    util.call_and_print(sum_priorities, sample)
    util.call_and_print(sum_priorities, input)

    print("\nTASK 2")
    util.call_and_print(sum_priorities, sample, 3)
    util.call_and_print(sum_priorities, input, 3)

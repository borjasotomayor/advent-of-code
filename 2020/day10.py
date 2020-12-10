"""
Day 10
https://adventofcode.com/2020/day/10

1st star: 00:09:00
2nd star: 00:37:22

Welp, for the second star I spent way too much time going through
several inefficient solutions before I stared at the sequences,
realized I was counting up the same sequences over and over,
and what I needed was memoization.
"""

import util
import math
import sys
import re

from util import log


def count_differences(jolts):    
    """
    Find the differences between values in a sorted list,
    with 0 and max(lst) + 3 before and after the list,
    as required by the problem.
    """
    jolts = sorted(jolts)

    lst = [0] + jolts + [max(jolts)+3]

    diffs = {}
    for i in range(len(lst)-1):
        diff = lst[i+1] - lst[i]
        diffs[diff] = diffs.setdefault(diff, 0) + 1

    return diffs[1] * diffs[3]


def gen_arrangements(start_jolt, jolts):
    """
    Given a starting jolt, and a list of jolts,
    find all the possible arrangements of jolts.
    """

    # Base case: if there are no jolts, return
    # a list with a single arrangement: the 'empty'
    # arrangements
    if len(jolts) == 0:
        return [[]]

    arrangements = []
    for i, next_jolt in enumerate(jolts):
        if next_jolt - start_jolt <= 3:
            # If this is a valid next jolt, then recursively
            # generate all valid arrangements that start
            # with that jolt
            rem_arrangements = gen_arrangements(next_jolt, jolts[i+1:])
            for ra in rem_arrangements:
                arrangements.append([next_jolt] + ra)
        elif next_jolt - start_jolt > 3:
            # Otherwise, no sense in continuing to explore jolts
            break

    return arrangements


def count_arrangements_1(jolts):
    """
    First attempt: generate all possible arrangements and count them
    Works for the small examples, but takes too long for the actual
    input
    """

    arrangements = gen_arrangements(0, sorted(jolts))

    return len(arrangements)


def count_arrangements_2(jolts):
    """
    Second attempt: *count* all the possible arrangements. We don't
    need all those pesky lists floating around!
    """

    def count_recursive(jolts, start_jolt, next_index):

        if next_index >= len(jolts)-1:
            return 1

        n_arrangements = 0
        for i in range(next_index, len(jolts)):
            next_jolt = jolts[i]
            if next_jolt - start_jolt <= 3:
                n_arrangements += count_recursive(jolts, next_jolt, i+1)           
            elif next_jolt - start_jolt > 3:
                break

        return n_arrangements

    return count_recursive(sorted(jolts), 0, 0)


def count_arrangements_3(jolts):
    """
    Third attempt: Geez, FINE, I'll add memoization!
    """

    def count_recursive(jolts, start_jolt, next_index, memo):
        if (start_jolt, next_index) in memo:
            return memo[(start_jolt, next_index)]

        if next_index >= len(jolts)-1:
            return 1

        arrangements = 0
        for i in range(next_index, len(jolts)):
            next_jolt = jolts[i]
            if next_jolt - start_jolt <= 3:
                arrangements += count_recursive(jolts, next_jolt, i+1, memo)           
            elif next_jolt - start_jolt > 3:
                break

        memo[(start_jolt, next_index)] = arrangements

        return arrangements    

    return count_recursive(sorted(jolts), 0, 0, {})


if __name__ == "__main__":
    util.set_debug(True)

    sample1 = util.read_ints("input/sample/10-1.in")
    sample2 = util.read_ints("input/sample/10-2.in")
    jolts = util.read_ints("input/10.in")

    print("TASK 1")
    util.call_and_print(count_differences, sample1)
    util.call_and_print(count_differences, sample2)
    util.call_and_print(count_differences, jolts)

    print("\nTASK 2")
    util.call_and_print(count_arrangements_1, sample1)
    util.call_and_print(count_arrangements_2, sample1)
    util.call_and_print(count_arrangements_3, sample1)
    util.call_and_print(count_arrangements_1, sample2)
    util.call_and_print(count_arrangements_2, sample2)
    util.call_and_print(count_arrangements_3, sample2)
    util.call_and_print(count_arrangements_3, jolts)

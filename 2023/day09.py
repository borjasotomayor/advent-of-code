"""
Day 9
https://adventofcode.com/2023/day/9

1st star: 11:48:43 (*)
2nd star: 11:49:51 (*)

(*) Did not stay up to solve the problem at release time

This was a cute little problem. Not a fan of having to process
lists in an un-Pythonic way (mucking around with indexes directly)
but it got the job done.
"""

import util
import math
import sys
import re

from util import log

def find_next_value(history: list[int]) -> int:
    """
    Find the next value in the history
    """

    # We are going to build a list of lists containing
    # the differences at each level. Index 0 contains
    # the original history
    differences = [history]

    # Keep computing differences (and adding them to the
    # differences list) until we reach an all-zeroes list
    while not all(x == 0 for x in differences[-1]):
        last = differences[-1]
        diff = [last[i] - last[i-1] for i in range(1, len(last))]
        differences.append(diff)

    # Add the placeholders, and initialize the bottom
    # one to zero
    for diff in differences:
        diff.append(None)
    differences[-1][-1] = 0

    # Compute the next value in each list
    for i in range(len(differences)-2, -1, -1):
        cur = differences[i]
        cur[-1] = differences[i+1][-1] + cur[-2]

    # Return the next value in the original history
    return differences[0][-1]

def task1(histories: list[list[int]]) -> int:
    """
    Task 1: Add up the next values in each history
    """
    sum = 0
    for history in histories:
        sum += find_next_value(history)
    return sum


def task2(histories: list[list[int]]) -> int:
    """
    Task 2: Add up the prior values in each history
    """
    # Same as Task 1, but reversing the lists.
    sum = 0
    for history in histories:
        sum += find_next_value(list(reversed(history)))
    return sum


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/09.in", sep="\n", sep2=" ")
    input = util.read_ints("input/09.in", sep="\n", sep2=" ")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)

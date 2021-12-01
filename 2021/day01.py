"""
Day 1
https://adventofcode.com/2021/day/1

1st star: 00:01:57
2nd star: 00:04:07

Well, as usual, the first day problem is pretty straightforward, but
fun to speed-code. My code below is pretty similar to what I used 
to solve the problem, modulo a bit of cleaning up + documenting.
"""

import util
import math
import sys
import re

from util import log


def count_incrementing(nums):
    """
    Counts the number of values in a list that are
    larger than the preceding value.

    Args:
        nums (list of ints): List of values

    Returns:
        int: Number of times a value is larger than
             the preceding value
    """

    prev = None
    incr = 0
    for n in nums:
        if prev is not None:
            if n > prev:
                incr += 1
        prev = n
    return incr


def count_incrementing_window(nums, window=3):
    """
    Goes through a list with a sliding window,
    and counts the number of times the sum of 
    the values in a window is larger than the
    preceding window.

    Args:
        nums (list of ints): List of values
        window (int): Window size

    Returns:
        int: Number of times the sum of values
             in a window is larger than the 
             preceding window.
    """    
    prev = None
    incr = 0
    for i in range(len(nums)-window+1):
        win = nums[i:i+window]
        s = sum(win)
        if prev is not None:
            if s > prev:
                incr += 1
        prev = s

    return incr


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/01.in")
    input = util.read_ints("input/01.in")

    print("TASK 1")
    util.call_and_print(count_incrementing, sample)
    util.call_and_print(count_incrementing, input)

    print("\nTASK 2")
    util.call_and_print(count_incrementing_window, sample)
    util.call_and_print(count_incrementing_window, input)

"""
Day 9
https://adventofcode.com/2020/day/9

1st star: 00:06:10
2nd star: 00:11:39

Went for an uninspired brute-force algorith, which I was actually pretty
surprised to find worked fine (I was fully expecting to start burning
CPU on the real inputs, and have to go back to the drawing board
to find a more clever algorithm)

The code below is essentially like my original code, except for 
some minor cleaning up.
"""

import util
import math
import sys
import re
import itertools

from util import log


def has_pair_sum(numbers, target):
    """
    Given a list of numbers, check if there is a pair of numbers
    that adds up to a target value
    """
    for a, b in itertools.combinations(numbers, 2):
        if a + b == target:
            return True
    
    return False


def task1(numbers, preamble_len):
    """
    Using a sliding window of length 'preamble_len',
    check if there is a pair of values in the sliding
    window that add up to the value immediately
    after the sliding window.
    """
    sliding_window = numbers[:preamble_len]
    remaining_values = numbers[preamble_len:]

    while len(remaining_values) > 0:
        number = remaining_values.pop(0)
        if not has_pair_sum(sliding_window, number):
            return number
        
        sliding_window.pop(0)
        sliding_window.append(number)
            
    return None


def task2(numbers, preamble_len):
    """
    Find a contiguous set of at least two numbers 
    that add up to the invalid number from the previous task.
    """    
    target = task1(numbers, preamble_len)

    for i in range(len(numbers)):
        range_sum = numbers[i]
        for j in range(i+1, len(numbers)):
            range_sum += numbers[j]
            if range_sum == target:
                sublist = numbers[i:j+1]
                return min(sublist) + max(sublist)
            elif range_sum > target:
                break


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/09.in")
    numbers = util.read_ints("input/09.in")

    print("TASK 1")
    util.call_and_print(task1, sample, 5)
    util.call_and_print(task1, numbers, 25)

    print("\nTASK 2")
    util.call_and_print(task2, sample, 5)
    util.call_and_print(task2, numbers, 25)

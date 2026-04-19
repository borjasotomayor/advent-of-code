"""
Day 1
https://adventofcode.com/2024/day/1

A nice, simple list processing problem.
"""

import util

from util import log

def read_lists(input: list[int]) -> tuple[list[int], list[int]]:
    """Parses input into two lists (one per column)"""
    l1 = input[0::2]
    l2 = input[1::2]

    return l1, l2

def add_differences(l1: list[int], l2: list[int]) -> int:
    """Task 1: Add up the differences between the (sorted) lists"""    

    total = 0
    for a, b in zip(sorted(l1), sorted(l2)):
        total += abs(a - b)
    
    return total
    

def count_occurrences(l1: list[int], l2: list[int]) -> int:
    """ 
    Task 2: Product of numbers in first list times
    the number of times each number appears in the
    second list
    """

    # Count up numbers in the 2nd list
    counts: dict[int, int] = {}
    for n in l2:
        counts[n] = counts.setdefault(n, 0) + 1

    # Add up products
    total = 0
    for n in l1:
        total += n * counts.get(n, 0)

    return total


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/01.in")
    input = util.read_ints("input/01.in")

    lst1s, lst2s = read_lists(sample)
    lst1, lst2 = read_lists(input)

    print("TASK 1")
    util.call_and_print(add_differences, lst1s, lst2s)
    util.call_and_print(add_differences, lst1, lst2)

    print("\nTASK 2")
    util.call_and_print(count_occurrences, lst1s, lst2s)
    util.call_and_print(count_occurrences, lst1, lst2)

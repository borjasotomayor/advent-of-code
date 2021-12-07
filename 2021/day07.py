"""
Day 7
https://adventofcode.com/2020/day/7

1st star: 00:03:27
2nd star: 00:05:39

Welp, this problem was way easier than I expected for a day 7 problem.
Apparently there is a more clever O(n) solution, but my O(n^2) solution 
seems to work just fine.
"""

import util
import math
import sys
import re

from util import log


def task1(crabs):
    min_fuel = None

    for i in range(min(crabs), max(crabs)+1):
        fuel = sum(abs(crab-i) for crab in crabs)
        min_fuel = fuel if min_fuel is None else min(fuel, min_fuel)

    return min_fuel


def sum_n(n):
    """
    Returns the sum of 1..n
    """
    return (n*(n+1))//2


def task2(crabs):
    min_fuel = None

    for i in range(min(crabs), max(crabs)+1):
        fuel = sum(sum_n(abs(crab-i)) for crab in crabs)
        min_fuel = fuel if min_fuel is None else min(fuel, min_fuel)

    return min_fuel


# One-line solutions, just for the heck of it

def task1_alt(crabs):
    return min(sum(abs(crab-i) for crab in crabs) for i in range(min(crabs), max(crabs)+1))

def task2_alt(crabs):
    return min(sum(abs(crab-i)*(abs(crab-i)+1)//2 for crab in crabs) for i in range(min(crabs), max(crabs)+1))


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/07.in", sep=",")
    input = util.read_ints("input/07.in", sep=",")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)

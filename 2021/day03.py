"""
Day 3
https://adventofcode.com/2021/day/3

1st star: 00:05:35
2nd star: 00:25:27

This was a fun problem but, hoo boy, my original code for 
Task 2 was an unholy mess. The version below is the
result of a looot of refactoring.
"""

import util
import math
import sys
import re

from util import log


def count_digits(numbers, pos):
    """
    Given a list of strings representing binary numbers,
    count the 0's and 1's at position pos in each number.
    
    Returns a (zeros, ones) tuple
    """
    rv = [0, 0]
    for number in numbers:
        if number[pos] == "0":
            rv[0] += 1
        if number[pos] == "1":
            rv[1] += 1

    return tuple(rv)


def count_all_digits(numbers):
    """
    Given a list of strings representing binary numbers,
    count the 0's and 1's in each position of the string.
    
    Returns a list of (zeros, ones) tuple (one per position)
    """    
    len_number = len(numbers[0])
    rv = []
    for i in range(len_number):
        rv.append(count_digits(numbers, i))
    return rv


def power_consumption(numbers):
    """
    Computes the power consumption (Task 1)
    """
    counts = count_all_digits(numbers)

    gamma = []
    epsilon = []
    for zeros, ones in counts:
        if ones > zeros:
            gamma.append("1")
            epsilon.append("0")
        else:
            gamma.append("0")
            epsilon.append("1")

    gamma = int("".join(gamma), 2)
    epsilon = int("".join(epsilon), 2)

    return gamma * epsilon


def filter(numbers, ones_value, zeros_value):
    """
    Given a list of strings representing binary numbers,
    do a "bit criteria filtering" (as described in Task 1)

    The "ones_value" parameter specifies the value that
    we should filter by when the number of ones is greater
    than or equal to the number of zeros. Otherwise we filter
    by "zeros_value"

    Returns the binary number that results from the filtering.
    """
    len_number = len(numbers[0])

    possible_numbers = set(numbers)
    for i in range(len_number):
        zeros, ones = count_digits(possible_numbers, i)
        if ones >= zeros:
            filter_by = ones_value
        else:
            filter_by = zeros_value
        for number in list(possible_numbers):
            if number[i] != filter_by:
                possible_numbers.discard(number)
                if len(possible_numbers) == 1:
                    break
        if len(possible_numbers) == 1:
            break

    assert len(possible_numbers) == 1

    return possible_numbers.pop()


def life_support_rating(numbers):
    """
    Computes the life support rating (Task 2)
    """

    oxy = filter(numbers, "1", "0")
    co2 = filter(numbers, "0", "1")
    
    return int(oxy, 2) * int(co2, 2)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/03.in", sep="\n")
    input = util.read_strs("input/03.in", sep="\n")

    print("TASK 1")
    util.call_and_print(power_consumption, sample)
    util.call_and_print(power_consumption, input)

    print("\nTASK 2")
    util.call_and_print(life_support_rating, sample)
    util.call_and_print(life_support_rating, input)

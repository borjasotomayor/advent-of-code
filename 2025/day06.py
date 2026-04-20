"""
Day 6
https://adventofcode.com/2025/day/6

At its core, this is a pretty easy problem, except the
parsing is really cumbersome in Part 2. My initial solution
was a hacky mess that was an affront to the laws of men and 
gods. After solving it, I spent a fair amount of time 
cleaning up the code so it was somewhat presentable.

I originally used NumPy for Part 1 (which made adding/multiplying
the columns pretty straightforward), but did more manual processing
in Part 2. When cleaning up the code, I was hoping to find a Numpy
way of solving Part 2, but it turned out to be easier to use lists
(except I figured out a much more straightforward way of doing so)
"""

import util
import math
from util import log

from typing import Sequence

import numpy as np
import numpy.typing as npt



def parse_regular(lines: list[str]) -> tuple[npt.NDArray, list[str]]:
    """
    Parse the math formulas for Part 1. Returns the numbers as
    a NumPy 2-D array
    """
    # Split and strip
    fields = [line.strip().split() for line in lines]

    # Numbers and operations
    numbers = np.array([[int(v) for v in line] for line in fields[:-1]])
    ops = fields[-1]

    return numbers, ops
    

def solve_regular(lines: list[str]) -> int:
    """
    Part 1: Process each problem using regular math
    """
    numbers, ops = parse_regular(lines)

    # To process each operation, we iterate over the transpose
    # of the array, which effectively allows us to process one
    # column at a time.
    total = 0
    for i, col in enumerate(numbers.T):
        if ops[i] == "+":
            total += np.sum(col)
        elif ops[i] == "*":
            total += np.prod(col)
    return total


def parse_cephalopod(lines: list[str]) -> tuple[list[list[int]], list[str]]:
    """
    Parse the problems using cephalopod math

    The general approach is to load the numbers (everything but the
    last line) into a character array, and transpose it, so we end up
    with one number per row (and a row of spaces between problems).
    Then, all we need to do is join those strings to produce the numbers.

    My original solution was an unholy mess of loops and indices that
    started by figuring out the width of each problem, and then iterating
    over the columns within that width to obtain each number. This is
    much better.
    """

    # It doesn't look like there is a native way in Numpy to
    # take all the strings in a row or column, and join them into a single
    # string, so we'll have to use lists instead.
    numchars: list[Sequence[str]] = [list(line) for line in lines[:-1]]
    numchars = list(zip(*numchars)) # <- Transposes the matrix
    ops = lines[-1].strip().split()

    # Numbers will contain a list of problems (each problem
    # is a list of numbers)
    problems: list[list[int]] = [[]]
    for col in numchars:
        num = "".join(col).strip()
        if num == "":
            # Problem separator. We start a new list of
            # numbers.
            problems.append([])
        else:
            # Append the number to the last list in the
            # list of numbers
            problems[-1].append(int(num))

    return problems, ops    


def solve_cephalopod(lines: list[str]) -> int:
    """
    Part 2: Process each problem using cephalopod math.
    """
    numbers, ops = parse_cephalopod(lines)

    total = 0
    for i, nums in enumerate(numbers):
        if ops[i] == "+":
            total += sum(nums)
        elif ops[i] == "*":
            total += math.prod(nums)
    return total


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/06.in", sep="\n", strip=False)
    input = util.read_strs("input/06.in", sep="\n", strip=False)

    print("TASK 1")
    util.call_and_print(solve_regular, sample)
    util.call_and_print(solve_regular, input)

    print("\nTASK 2")
    util.call_and_print(solve_cephalopod, sample)
    util.call_and_print(solve_cephalopod, input)

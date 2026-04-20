"""
Day 7
https://adventofcode.com/2024/day/7

This is is the kind of problem where I naturally
gravitate towards recursion (at least for me,
the computation feels more natural than futzing
around with itertools to find all possible orderings
of operators, and then evaluating that expression)

The only thing that tripped me up was the left-to-right
evaluation, since breaking up the list of operands
into (lst[0], lst[1:]) will result in a right-to-left
evaluation.
"""

import util

from util import log


def parse_input(filename: str) -> list[tuple[int, list[int]]]:
    """
    Parse the input
    """
    lines = util.read_strs(filename, sep="\n", sep2=": ")
    equations = []
    for target, operands in lines:
        equations.append((int(target), [int(x) for x in operands.split()]))
    return equations


def explore_operands(target: int, operands: list[int], concat: bool) -> set[int]:
    """
    Given a target and a list of operands, return a set with all the
    possible values of the equation using addition and multiplication
    (and, optionally, concatenation)
    """
    # This ensures left-to-right evaluation.
    val = operands[-1]
    rem = operands[:-1]

    # Base case: if the list only has one element, that's the only
    # possible value of the equation
    if len(rem) == 0:
        return {val}
    
    # Recursive case: find the values resulting from trying
    # all the different operators in the remaining operands
    rv = set()
    other_vals = explore_operands(target, rem, concat)
    
    # Then, add/multiply/concatenate those values with
    # the current value. If they don't exceed the target,
    # add them to the return set
    for other in other_vals:
        if other + val <= target:
            rv.add(other + val)
        if other * val <= target:
            rv.add(other * val)
        if concat:
            nv = int(str(other) + str(val))
            if nv <= target:
                rv.add(nv)

    return rv


def process_equations(equations: list[tuple[int, list[int]]], concat: bool) -> int:
    """
    Parts 1 and 2. Find the satisfiable equations, and return the
    sum of their targets.
    """
    total = 0
    for target, operands in equations:
        vals = explore_operands(target, operands, concat)
        if target in vals:
            total += target
    return total


if __name__ == "__main__":
    util.set_debug(False)

    sample = parse_input("input/sample/07.in")
    input = parse_input("input/07.in")

    print("TASK 1")
    util.call_and_print(process_equations, sample, False)
    util.call_and_print(process_equations, input, False)

    print("\nTASK 2")
    util.call_and_print(process_equations, sample, True)
    util.call_and_print(process_equations, input, True)

"""
Day 5
https://adventofcode.com/2025/day/5

This was a fun problem to work through. I tried
brute force in Part 2, in case it happened to work,
and it very much didn't. Figuring out how to work
around that was a fun little puzzle.
"""

import util

from util import log


def parse_input(lines: list[str]) -> tuple[list[tuple[int, int]], list[int]]:
    """
    Parse input data into a list of ranges, and a list of ingredients.
    """
    ranges = []
    ingredients = []
    for line in lines:
        line = line.strip()
        if "-" in line:
            lb, ub = map(int, line.split("-"))
            ranges.append((lb, ub))
        elif line != "":
            ingredients.append(int(line))

    return ranges, ingredients


def count_fresh(ingredients: list[int], ranges: list[tuple[int, int]]) -> int:
    """
    Part 1: Count the number of fresh ingredients (check if each ingredient
    is in any of the ranges)
    """
    fresh = 0
    for ing in ingredients:
        for lb, ub in ranges:
            if lb <= ing <= ub:
                fresh += 1
                break

    return fresh


def combine_ranges(ranges: list[tuple[int,int]]) -> list[tuple[int, int]]:
    """
    Recursively combine a list of (sorted) ranges so there are no
    overlapping ranges.

    This is not a particularly recursive problem but, somehow,
    tail recursion felt more natural here (instead of iterating
    over a list of ranges with two indices)
    """

    # Base case: If we only have one range, there is nothing to combine
    if len(ranges) <= 1:
        return ranges
    
    # Start with the first range
    range = ranges[0]

    # It may be possible to combine this range with
    # some of the next ranges. If the next range overlaps
    # with the range, we update the range itself, and look
    # at the next range, and so on.
    i = 1
    while i < len(ranges) and ranges[i][0] - 1 <= range[1]:
        range = (range[0], max(range[1], ranges[i][1]))
        i += 1

    # At this point, `range` contains a single range
    # combining all the ranges up to (but not including)
    # position `i`. We recursively explore the rest
    # of the ranges.
    return [range] + combine_ranges(ranges[i:])


def count_fresh_ranges(ranges: list[tuple[int,int]]) -> int:
    """
    Part 2: Count the fresh ranges.
    """
    # If we try to just add up the individual ingredients in all
    # the ranges (while accounting for repeated values in overlapping
    # ranges), the code will take too long to run. We need to
    # first consolidate all the ranges to remove all overlaps.
    combined = combine_ranges(sorted(ranges))

    # Once we have that, we just add them up
    return sum((ub - lb + 1) for lb, ub in combined)
   

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/05.in", sep="\n")
    input = util.read_strs("input/05.in", sep="\n")

    ranges_sample, ingredients_sample = parse_input(sample)
    ranges, ingredients = parse_input(input)

    print("TASK 1")
    util.call_and_print(count_fresh, ingredients_sample, ranges_sample)
    util.call_and_print(count_fresh, ingredients, ranges)

    print("\nTASK 2")
    util.call_and_print(count_fresh_ranges, ranges_sample)
    util.call_and_print(count_fresh_ranges, ranges)

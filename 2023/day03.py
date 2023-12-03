"""
Day 3
https://adventofcode.com/2023/day/3

1st star: 00:07:42
2nd star: 00:18:50

Once again, the Grid class I've been developing over the
course of several advents of code comes to the rescue!
It made traversing the grid and checking for adjacent values
much simpler, which saved me a lot of time.

After solving the problem, I mostly refactored my code
to extract the part numbers in a separate function,
and creating a simple PartNumber class to make the code
more readable when manipulating part numbers.
"""

import util
import math
import sys
import re

from util import log

from util import Grid


class PartNumber:
    """
    Class for representing part numbers
    """

    coords: set[tuple[int, int]]
    value: int

    def __init__(self, number_coords: list[tuple[int, int, int]]):
        self.coords = set((x, y) for x, y, _ in number_coords)
        self.value = int("".join(str(v) for _, _, v in number_coords))


def get_part_numbers(grid: Grid) -> list[PartNumber]:
    """
    Extract the part numbers from the grid. Each PartNumber
    object contains the coordinates of each digit of the
    part number, as well as the numerical value of the part
    number.
    """

    # We start by extracting all the numbers from the
    # grid (including their coordinates)
    # Each individual number is a list of (x, y, v) tuples
    # where 'v' is the value at (x, y)
    numbers: list[list[tuple[int, int, int]]] = []
    cur_number: list[tuple[int, int, int]] = []
    for y in range(grid.max_y):
        for x in range(grid.max_x):
            v = grid.get(x, y)

            if not v.isnumeric() and cur_number == []:
                # Not part of a number and we're not processing
                # a number. Nothing to do.
                continue
            elif not v.isnumeric() and cur_number != []:
                # Not part of a number, but we were processing
                # a number, which means the number is done. We
                # add it to the list of numbers
                numbers.append(cur_number)
                cur_number = []
            elif v.isnumeric() and cur_number == []:
                # Part of a number and we're not currently
                # processing a number, so this is the start
                # of a number
                cur_number = [(x, y, v)]
            elif v.isnumeric() and cur_number != []:
                # Part of a number, and we're currently
                # processing a number, so we add it to the
                # current number
                cur_number.append((x, y, v))

    # Once we have the numbers, we figure out which of them
    # are part numbers, and we create PartNumber objects for
    # them.
    part_numbers: list[PartNumber] = []

    for number in numbers:
        is_part_number = False
        for x, y, _ in number:
            for dx, dy in Grid.DIRECTIONS:
                adj = grid.getdefault(x+dx, y+dy, ".")
                if not adj.isnumeric() and not adj == ".":
                    part_numbers.append(PartNumber(number))
                    is_part_number = True
                    break
            # We don't need to process the rest of the digits
            # in the number if we already know it's a part number.
            if is_part_number:
                break

    return part_numbers


def sum_part_numbers(grid: Grid) -> int:
    """
    Task 1: Sum of the value of the part numbers
    """
    part_numbers = get_part_numbers(grid)

    return sum(pn.value for pn in part_numbers)


def sum_gear_ratios(grid: Grid) -> int:
    """
    Task 2: Sum of gear ratios
    """
    part_numbers = get_part_numbers(grid)

    # This dictionary will maps gear locations
    # to a set of adjacent part numbers for that gear
    gears: dict[tuple[int, int], set[PartNumber]] = {}

    # For each part number, look at its adjacent
    # coordinates. If there is a gear, update the gears
    # dictionary to note that the part number is adjacent
    # to that gear
    for pn in part_numbers:
        for x, y in pn.coords:
            for dx, dy in Grid.DIRECTIONS:
                nx, ny = x+dx, y+dy
                adj = grid.getdefault(nx, ny, ".")
                if adj == "*":
                    gears.setdefault((nx, ny), set()).add(pn)

    # Now, all we need to do is identify the gears that have
    # exactly two adjacent part numbers, and multiply their values
    sum = 0
    for adj_part_numbers in gears.values():
        if len(adj_part_numbers) == 2:
            sum += math.prod(pn.value for pn in adj_part_numbers)

    return sum


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/03.in", sep="\n")
    input = util.read_strs("input/03.in", sep="\n")

    sample_grid = Grid(sample)
    grid = Grid(input)

    print("TASK 1")
    util.call_and_print(sum_part_numbers, sample_grid)
    util.call_and_print(sum_part_numbers, grid)

    print("\nTASK 2")
    util.call_and_print(sum_gear_ratios, sample_grid)
    util.call_and_print(sum_gear_ratios, grid)

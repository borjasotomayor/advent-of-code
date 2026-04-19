"""
Day 4
https://adventofcode.com/2024/day/4

I brute-forced Part 1, fully expecting I would have to write
some sort of fancy dynamic programming algorithm for Part 2,
and then Part 2 turned out to be brute-forceable as well
(at least for this input)

As usual, my trusty Grid class made the code much easier to write.
"""

import util
from grid import Grid

from util import log


def count_xmas(grid):
    """
    Count occurrences of XMAS in the grid
    """
    total = 0
    for r, c, v in grid:
        if v == "X":
            for dr, dc in Grid.DIRECTIONS:
                if (grid.getdefault(r + dr  , c + dc  ) == "M" and 
                    grid.getdefault(r + dr*2, c + dc*2) == "A" and 
                    grid.getdefault(r + dr*3, c + dc*3) == "S"):
                    total += 1
    return total


def count_masx(grid):
    """
    Count occurrences of MAS (in an X) in the grid
    """
    total = 0
    for r, c, v in grid:
        if v == "A":
            # Creating all these sets is not great, but it avoids a huge mess
            # of conditionals to check all arrangements of the MAS shape
            diag1 = {grid.getdefault(r - 1, c - 1), grid.getdefault(r + 1, c + 1)}
            
            # Bail out if we can already tell this is not an MAS shape
            if diag1 != {"M", "S"}:
                continue

            diag2 = {grid.getdefault(r - 1, c + 1), grid.getdefault(r + 1, c - 1)}

            # We've already established that one diagonal has an M and an S,
            # so now we just need to check for equality
            if diag1 == diag2:
                total += 1

    return total



if __name__ == "__main__":
    util.set_debug(False)

    sample = Grid.from_file("input/sample/04.in")
    input = Grid.from_file("input/04.in")

    print("TASK 1")
    util.call_and_print(count_xmas, sample)
    util.call_and_print(count_xmas, input)

    print("\nTASK 2")
    util.call_and_print(count_masx, sample)
    util.call_and_print(count_masx, input)

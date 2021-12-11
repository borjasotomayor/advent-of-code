"""
Day 11
https://adventofcode.com/2021/day/11

1st star: 00:17:07	
2nd star: 00:19:08

Once again, my Grid class comes to the rescue! It's nice to be able to
focus on the problem at hand without having to futz around with grid 
boundaries, making sure you're hitting the right adjacent positions, etc.

Also, I was surprised my step() code for Part 1 worked out of the box
for Part 2. I was fully expecting to start burning CPU in Part 2 because
you needed some clever way to identify repeating patterns, so I was
relieved when I got a (correct) solution simply by looping until all 100
octopuses flashed.
"""

import util
import math
import sys
import re

from util import log


def step(grid):
    """
    Perform one step of the simulation.

    Returns the number of flashes in this step.
    """

    flashes = set()

    # Start by incrementing every position by one
    for x in range(grid.max_x):
        for y in range(grid.max_y):
            v = grid.get(x, y)
            grid.set(x, y, v+1)


    while True:
        # In each iteration of this loop, we go through every position
        # of the grid, and flashes the position if necessary.
        # We break out of the loop if, at the end of the iteration.,
        # there have been no flashes.

        some_flashes = False
        for x in range(grid.max_x):
            for y in range(grid.max_y):
                v = grid.get(x, y)

                if v > 9 and (x, y) not in flashes:
                    # If the value is greater than 9, and hasn't already been
                    # flashed, we increment each adjancent position by one.
                    # We don't initiate a "flashing chain reaction"; that
                    # will be handled by the next iteration of the main
                    # while loop.
                    for (dx, dy) in util.Grid.DIRECTIONS:
                        ax, ay = x+dx, y+dy
                        av = grid.getdefault(ax, ay)
                        if av is not None:
                            grid.set(ax, ay, av+1)

                    # Add this position to the set of flashes
                    flashes.add((x, y))
                    some_flashes = True

        # If we didn't encounter any flashes, we're done.
        if not some_flashes:
            break

    # At the end of the step, we reset all the flashed positions to zero
    for (x,y) in flashes:
        grid.set(x, y, 0)

    return len(flashes)


def task1(grid):
    """
    Count up the number of flashes after 100 steps
    """
    n_flashes = 0
    for i in range(100):
        n_flashes += step(grid)

    return n_flashes


def task2(grid):
    """
    Find the first step where all octopuses flash
    """
    n = 1
    while True:
        if step(grid) == 100:
            return n
        n += 1


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.Grid.from_file("input/sample/11.in", cast=int)
    input = util.Grid.from_file("input/11.in", cast=int)

    print("TASK 1")
    util.call_and_print(task1, sample.copy())
    util.call_and_print(task1, input.copy())

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)

"""
Day 14
https://adventofcode.com/2022/day/14

1st star: 00:27:30
2nd star: 00:34:01

Ah, I do love a discrete-event simulation! I took the approach
of building up a set of coordinates that would be updated
as sand is added to the cave (and updating the sand at each step)

My first solution was... inelegant, to put it mildly. I took 
the approach of detecting whether something was falling into 
the void by checking if its y coordinate reached 1,000,000, 
and for Part 2 I added coordinates for the floor extending 2,000
positions to the left and right of the minimum/maximum x value.

The code below is heavily cleaned up, and checks for the simulation's
stopping conditions more elegantly.
"""

import util
import math
import sys
import re

from util import log


def simulate(coords, floor=False):
    """
    Simulate dropping sand into the cave until a stopping
    condition is reached (Part 1: sand falls into the void,
    Part 2: the sand source gets clogged)
    """
    max_y = max(y for _, y in coords)

    nsand = 0

    # Outer loop. One iteration per sand dropped
    # until one of the stopping conditions is reached.
    while True:

        if (500, 0) in coords:
            # Stopping condition in Part 2: If there's already 
            # something at the sand source, we can't add more sand
            return nsand

        # Generate one sand
        sand = (500,0)
        coords.add(sand)
        nsand += 1
  
        # Inner loop. Let it drop until it comes to rest
        # (or until we reach the Part 1 stopping condition)
        while True:
            sx, sy = sand

            # In Part 2, if we're right over the floor,
            # we can't do anything else with this sand
            if floor and sy+1 == max_y + 2:
                break   

            # Check all the possible next positions
            next = (sx, sy+1)
            if next in coords:
                next = (sx-1, sy+1)
                if next in coords:
                    next = (sx+1, sy+1)
                    if next in coords:
                        # The sand has come to rest
                        break

            # If it has fallen past the lowest rock,
            # it will fall into the void
            if not floor and sy+1 == max_y:
                # We subtract 1 because the sand that falls
                # into the void isn't counted
                return nsand-1             

            # Update the set of coordinates
            coords.remove(sand)
            coords.add(next)
            sand = next


def input_to_coords(input):
    """
    Parse the input to produce a set of coordinates described by
    the lines in the input.
    """
    coords = set()

    lines = [[[int(v) for v in p.split(",")] for p in line] for line in input]

    for line in lines:
        px, py = line[0]
        for x, y in line[1:]:
            assert px==x or py==y

            if px==x:
                lb = min(py, y)
                ub = max(py, y)
                for iy in range(lb, ub+1):
                    coords.add((x, iy))

            if py==y:
                lb = min(px, x)
                ub = max(px, x)
                for ix in range(lb, ub+1):
                    coords.add((ix, y))
            px, py = x, y

    return coords


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/14.in", sep="\n", sep2=" -> ")
    input = util.read_strs("input/14.in", sep="\n", sep2=" -> ")

    print("TASK 1")
    util.call_and_print(simulate, input_to_coords(sample))
    util.call_and_print(simulate, input_to_coords(input))

    print("\nTASK 2")
    util.call_and_print(simulate, input_to_coords(sample), True)
    util.call_and_print(simulate, input_to_coords(input), True)

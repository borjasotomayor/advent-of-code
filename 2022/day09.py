"""
Day 9
https://adventofcode.com/2022/day/9

1st star: 00:20:50
2nd star: 00:30:40

My initial Part 1 implementation was an unholy mess
of head[0], head[1], tail[0], and tail[1] so I appreciated
how Part 2 forced me to generalize the solution and
construct a nice Knot class to keep track of each
knot in a linked-list manner (should've really taken
the hint with "head" and "tail" in Part 1)
"""

import util
import math
import sys
import re

from util import log

class Knot:
    """
    Class for representing a knot on the rope
    """

    def __init__(self, x, y, prev=None):
        """
        Constructor. We provide the initial coordinates,
        and the previous knot (if any)
        """
        self.x = x
        self.y = y
        self.prev = prev

    def move(self, dir):
        """
        Move the knot in the specified direction,
        and check whether we need to pull the preceding knot.
        """
        if dir == "R":
            self.x += 1
        elif dir == "L":
            self.x -= 1
        elif dir == "U":
            self.y += 1
        elif dir == "D":
            self.y -= 1

        self.update_prev()

    def update_prev(self):
        """
        "Pull" the preceding knot
        """
        if self.prev is None:
            return

        # Same row
        if self.prev.y == self.y:
            # two positions behind
            if self.prev.x == self.x-2:
                self.prev.x += 1
            # Two positions ahead
            elif self.prev.x == self.x+2:
                self.prev.x -= 1
        # Same column
        elif self.prev.x == self.x:
            # Two positions above
            if self.prev.y == self.y+2:
                self.prev.y -= 1
            # Two positions below
            elif self.prev.y == self.y-2:
                self.prev.y += 1
        # Not on the same column or row *and* not touching
        # Just need to check if the absolute difference in 
        # either x or y is greater than 1
        elif abs(self.prev.x-self.x) > 1 or abs(self.prev.y-self.y) > 1:
            # Bottom-left
            if self.prev.x < self.x and self.prev.y < self.y:
                self.prev.x += 1
                self.prev.y += 1
            # Top-left
            if self.prev.x < self.x and self.prev.y > self.y:
                self.prev.x += 1
                self.prev.y -= 1
            # Bottom-right
            if self.prev.x > self.x and self.prev.y < self.y:
                self.prev.x -= 1
                self.prev.y += 1
            # Top-right
            if self.prev.x > self.x and self.prev.y > self.y:
                self.prev.x -= 1
                self.prev.y -= 1

        # Keep going down the rope an update the preceding knot
        self.prev.update_prev()


def move_rope(movements, num_knots):
    # Generate the knots
    tail = Knot(0,0)
    prev = tail
    for _ in range(num_knots - 1):
        knot = Knot(0,0,prev)
        prev = knot

    # The last value of prev will be the head
    head = prev

    # Process the movements and keep track
    # of the position of the tail
    tail_positions = set()
    tail_positions.add((tail.x, tail.y))
    for dir, n in movements:
        for _ in range(int(n)):
            head.move(dir)
            tail_positions.add((tail.x, tail.y))

    return len(tail_positions)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/09-1.in", sep="\n", sep2=" ")
    sample2 = util.read_strs("input/sample/09-2.in", sep="\n", sep2=" ")
    input = util.read_strs("input/09.in", sep="\n", sep2=" ")

    print("TASK 1")
    util.call_and_print(move_rope, sample, 2)
    util.call_and_print(move_rope, input, 2)

    print("\nTASK 2")
    util.call_and_print(move_rope, sample, 10)
    util.call_and_print(move_rope, sample2, 10)
    util.call_and_print(move_rope, input, 10)

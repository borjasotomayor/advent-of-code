"""
Day 23
https://adventofcode.com/2022/day/23

1st star: 00:57:54
2nd star: 00:59:47

This was a fun "Game of Life" style problem where you just
had to be very careful about implementing every condition
correctly. I was glad that Part 2 was pretty straightforward
(in fact, I basically had all the code for it ready to go because
I had spent a bit of time implementing a "print_elves" function
that had to compute the minimum rectangle). After Day 21,
I was afraid Part 2 was going to involve some massive twist 
like "after 1,000,000 rounds, the elves will end up forming 
a polygon of N sides. Find N"
"""

import util
import math
import sys
import re

from util import log

# Cardinal directions
DIRECTIONS = { "NW": (-1, -1), "N": (0, -1), "NE": (+1,-1),
                "W": (-1,  0),                "E": (+1, 0),
               "SW": (-1, +1), "S": (0, +1), "SE": (+1,+1) }

# The directions an elf can propose
DIR_PROPOSAL = [("N", ("N", "NE", "NW")),
                ("S", ("S", "SE", "SW")),
                ("W", ("W", "NW", "SW")),
                ("E", ("E", "NE", "SE"))]

class Elf:
    """
    Simple class for keeping track of elves
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Elf({self.x}, {self.y})"


def get_next_pos(elves, elf, round_number):
    """
    Given the current set of elves, and the round number,
    find the next position for the given elf.
    """

    # Check whether there are any elves around is.
    # If not, we won't move.
    can_move = False
    for dx, dy in DIRECTIONS.values():
        nx, ny = elf.x + dx, elf.y + dy
        if (nx, ny) in elves:
            can_move = True
            break
    
    if not can_move:
        return elf.x, elf.y

    # This is the starting index into the DIR_PROPOSAL list
    start_pos = round_number % 4

    # Check all four directions
    for i in range(4):
        mov, adjs = DIR_PROPOSAL[(start_pos + i) % 4]

        # Check the 3 adjacent positions
        # If there is an elf in any of them, we don't move
        can_move = True
        for adj in adjs:
            dx, dy = DIRECTIONS[adj]
            nx, ny = elf.x + dx, elf.y + dy

            if (nx, ny) in elves:
                can_move = False
                break

        # If the 3 adjacent positions are empty,
        # we return the next position
        if can_move:
            dx, dy = DIRECTIONS[mov]
            nx, ny = elf.x + dx, elf.y + dy
            return nx, ny

    # If we can't move in any of the four directions, we stay put
    return elf.x, elf.y


def round(round_number, elves):
    """
    Perform one round. Returns True if at least one elf moved,
    False otherwise.
    """

    # Dictionary mapping elves to their next position
    next_pos = {}

    # Find the next position for every elf
    for elf in elves.values():
        nx, ny = get_next_pos(elves, elf, round_number)
        next_pos[elf] = (nx, ny)

    # Count up how many elves want to move to
    # each position
    count = {}
    for nx, ny in next_pos.values():
        count[(nx,ny)] = count.get((nx,ny), 0) + 1

    # Try to move each elf
    moved_some = False
    for elf, (nx, ny) in next_pos.items():
        # If the elf is staying put, nothing to do
        if elf.x == nx and elf.y == ny:
            continue

        # If more than one elf wants to move to this position
        # we don't move
        if count[(nx, ny)] > 1:
            continue

        # Otherwise we move (and update the elves dictionary)
        del elves[(elf.x, elf.y)]
        elf.x = nx
        elf.y = ny
        elves[(elf.x, elf.y)] = elf
        moved_some = True

    return moved_some


def print_elves(elves):
    """
    Prints the elves in a grid (for debugging only)
    """
    min_x = min(elf.x for elf in elves.values())
    max_x = max(elf.x for elf in elves.values())
    min_y = min(elf.y for elf in elves.values())
    max_y = max(elf.y for elf in elves.values())

    grid_max_x = max_x - min_x
    grid_max_y = max_y - min_y

    grid = util.Grid.empty(grid_max_x+1, grid_max_y+1, ".")

    for elf in elves.values():
        grid.set(elf.x-min_x, elf.y-min_y, "#")

    print(grid)


def count_empty(elves):
    """
    Count the number of empty spaces in the smallest
    rectangle containing elves
    """
    min_x = min(elf.x for elf in elves.values())
    max_x = max(elf.x for elf in elves.values())
    min_y = min(elf.y for elf in elves.values())
    max_y = max(elf.y for elf in elves.values())

    grid_max_x = max_x - min_x
    grid_max_y = max_y - min_y

    return (grid_max_x+1) * (grid_max_y+1) - len(elves)


def read_input(input):
    """
    Read the input and generate a dictionary
    mapping elf coordinates to Elf objects
    """

    max_x = len(input[0])
    max_y = len(input)

    elves = {}
    for x in range(max_x):
        for y in range(max_y):
            if input[y][x] == "#":
                elves[(x,y)] = Elf(x, y)

    return elves

def task1(input):
    """
    Task 1: Count the number of empty spots after 10 rounds
    """
    elves = read_input(input)

    for i in range(10):
        round(i, elves)

    return count_empty(elves)
    

def task2(input):
    """
    Find the round at which the elves stop moving
    """
    elves = read_input(input)

    i = 0
    while True:
        moved = round(i, elves)

        if not moved:
            break

        i += 1

    return i+1


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/23-1.in", sep="\n")
    sample2 = util.read_strs("input/sample/23-2.in", sep="\n")
    input = util.read_strs("input/23.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample1)
    util.call_and_print(task1, sample2)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample2)
    util.call_and_print(task2, input)

"""
Day 12
https://adventofcode.com/2020/day/12

1st star: 00:11:01
2nd star: 00:30:33

Well, I was able to use a bunch of classes related to directions, bearings,
movements in directions, rotations, etc. that I wrote last year for
various AoC problems, so it turned out to be mostly a question of
putting all the pieces together (and not worry too much about whether
I was updating all the coordinates correctly, etc.)
"""

import util
import math
import sys
import re

from util import log
from util import Direction, rotate_clockwise, rotate_counterclockwise


def task1(actions):
    coords = (0, 0)
    cur_dir = Direction.EAST()

    for action_str in actions:
        log(action_str, coords)
        action = action_str[0]
        value = int(action_str[1:])

        if action in ("N", "S", "E", "W", "F"):
            if action == "N":
                move_dir = Direction.NORTH()
            elif action == "S":
                move_dir = Direction.SOUTH()
            elif action == "E":
                move_dir = Direction.EAST()
            elif action == "W":
                move_dir = Direction.WEST()
            elif action == "F":
                move_dir = cur_dir

            for _ in range(value):
                coords = move_dir.move_grid_coordinates(coords)
        elif action == "L":
            cur_dir.rotate_counterclockwise(value)
        elif action == "R":
            cur_dir.rotate_clockwise(value)

        log(f"New coordinates {coords}\n")

    return abs(coords[0]) + abs(coords[1])


def task2(actions):
    ship_coords = (0, 0)
    wayp_coords = (10, 1)

    for action_str in actions:
        log(action_str, ship_coords, wayp_coords)
        action = action_str[0]
        value = int(action_str[1:])

        if action in ("N", "S", "E", "W"):
            if action == "N":
                move_dir = Direction.NORTH()
            elif action == "S":
                move_dir = Direction.SOUTH()
            elif action == "E":
                move_dir = Direction.EAST()
            elif action == "W":
                move_dir = Direction.WEST()

            for _ in range(value):
                wayp_coords = move_dir.move_grid_coordinates(wayp_coords)
        elif action == "F":
            ship_coords = (ship_coords[0] + value * wayp_coords[0], ship_coords[1] + value * wayp_coords[1])
        elif action == "L":
            wayp_coords = rotate_counterclockwise(wayp_coords, value, origin=(0,0))
        elif action == "R":
            wayp_coords = rotate_clockwise(wayp_coords, value, origin=(0,0))

        log(f"New coordinates {ship_coords} {wayp_coords}\n")

    return abs(int(ship_coords[0])) + abs(int(ship_coords[1]))


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/12.in", sep="\n")
    actions = util.read_strs("input/12.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, actions)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, actions)

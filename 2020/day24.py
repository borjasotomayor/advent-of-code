"""
Day 24
https://adventofcode.com/2020/day/24

1st star: 00:42:10
2nd star: 01:51:43

I got the gist of both parts pretty quickly, but then ended up spending a
lot of time tracking down what turned out to be pretty silly bugs in
the code :-( Still pretty proud of how clean my code turned out to be
(and how fast it runs)
"""

import util
import math
import sys
import regex

from util import log


# The hex grid is represented using "offset coordinates",
# and these vectors tell us how much to update each coordinate
# in each direction.
VECTORS = {"e": (2,0),
           "w": (-2,0),
           "nw": (-1,1),
           "ne": (1,1),
           "sw": (-1,-1),
           "se": (1, -1)}


class Tile:
    """
    Simple class for manipulating tiles
    """

    WHITE = -1
    BLACK = 1

    def __init__(self, coords, color=WHITE):
        self.coords = coords
        self.color = color

    def flip(self):
        self.color = -self.color

    def __str__(self):
        return f"Tile({self.coords[0]}, {self.coords[1]})"

    def __repr__(self):
        return str(self)
    

def parse_instructions(instructions):
    """
    Parse the instructions using a regex
    """
    regex_str = "({})+".format("|".join(VECTORS.keys()))

    m = regex.match(regex_str, instructions)

    return m.captures(1)


def install_floor(instructions):
    """
    Install the initial floor
    """
    reference_tile = Tile((0,0))
    all_tiles = {(0,0):reference_tile}

    for line in instructions:
        current_tile = all_tiles[(0,0)]
        directions = parse_instructions(line)
        for direction in directions:
            x1, y1 = current_tile.coords
            dx, dy = VECTORS[direction]

            x2, y2 = x1+dx, y1+dy

            new_coords = (x2, y2)
            if new_coords in all_tiles:
                current_tile = all_tiles[new_coords]
            else:
                new_tile = Tile(new_coords)
                all_tiles[new_coords] = new_tile
                current_tile = new_tile

        current_tile.flip()

    return all_tiles


def task1(instructions):
    """
    Install the initial floot, and then count the number
    of black tiles
    """
    all_tiles = install_floor(instructions)

    n_black = 0
    for tile in all_tiles.values():
        if tile.color == Tile.BLACK:
            n_black += 1
        
    return n_black


def get_adjacent_tiles(all_tiles, coords):
    """
    Get all the tiles adjacent to the given coordinates.
    """
    tile = all_tiles[coords]

    adj = []
    for dx, dy in VECTORS.values():
        x1, y1 = tile.coords
        x2, y2 = x1+dx, y1+dy

        new_coords = (x2, y2)

        if new_coords in all_tiles:
            adj.append(all_tiles[new_coords])

    return adj


def expand(all_tiles):
    """
    Expand the floor by adding any missing tiles that would be
    adjacent to existing black tiles (since those are the only
    ones that could be affected by the update rule)
    """
    new_tiles = []

    for tile in all_tiles.values():
        if tile.color == Tile.BLACK:
            for dx, dy in VECTORS.values():
                x1, y1 = tile.coords
                x2, y2 = x1+dx, y1+dy

                new_coords = (x2, y2)
                if new_coords not in all_tiles:
                    new_tiles.append(Tile(new_coords))

    for new_tile in new_tiles:
        all_tiles[new_tile.coords] = new_tile

         
def task2(instructions, days):
    """
    Install the initial floor, and then run the "living art exhibit"
    """
    all_tiles = install_floor(instructions)    

    for _ in range(days):
        expand(all_tiles)

        to_flip = []
        for coords in all_tiles:
            tile = all_tiles[coords]

            adj = get_adjacent_tiles(all_tiles, coords)
            n_black = 0
            for adj_tile in adj:
                if adj_tile.color == Tile.BLACK:
                    n_black += 1

            if tile.color == Tile.BLACK and (n_black == 0 or n_black > 2):
                to_flip.append(coords)
            elif tile.color == Tile.WHITE and (n_black == 2):
                to_flip.append(coords)

        for coords in to_flip:
            all_tiles[coords].flip()

    n_black = 0
    for tile in all_tiles.values():
        if tile.color == Tile.BLACK:
            n_black += 1

    return n_black           


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/24.in", sep="\n")
    input = util.read_strs("input/24.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, ["esew"])
    util.call_and_print(task1, ["nwwswee"])
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample, 100)
    util.call_and_print(task2, input, 100)

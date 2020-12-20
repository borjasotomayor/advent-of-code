"""
Day 20
https://adventofcode.com/2020/day/20

1st star: 00:37:57
2nd star: 02:19:22

Sooo, at first I felt really proud of myself because I was able to compute 
the corners without actually stitching the image together:

 - There is only one possible stitching
 - Each tile has 8 possible edges (original and flipped)
 - We don't really care what direction the edges match in;
   we just care what other tiles could match.
 - A corner tile is thus a tile that can only match with two
   other tiles.

So, just compute the number of possible adjacent tiles for each
tile, and keep the ones with only two adjacent tiles.

And then there was part 2...

I ultimately got the right answer after using lots of numpy trickery, 
but I'm guessing there are cleaner algorithms for stitching images together.
"""

import util
import math
import sys
import re
import numpy as np

from util import log


def get_edge(tile, direction):
    """
    Given a tile, return a 1-dimensional numpy array with
    the up, down, left, or right edge.
    """
    if direction == "up":
        return tile[0]
    elif direction == "down":
        return tile[-1]
    elif direction == "left":
        return tile[:,0]
    elif direction == "right":
        return tile[:,-1]


def get_mirror_direction(direction):
    """
    Given a direction (up, down, left, right) return the
    mirror direction.
    """
    if direction == "up":
        return "down"
    elif direction == "down":
        return "up"
    elif direction == "left":
        return "right"
    elif direction == "right":
        return "left"


def test_adjacency(tile, other_tile, direction):
    """
    Given a tile, test whether some other tile can
    be stitched to it in the given direction.

    Returns the appropriately rotated/flipped other tile
    if a stitching is possible, otherwise returns None.
    """
    
    edge_to_match = get_edge(tile, direction)
    mirror_direction = get_mirror_direction(direction)

    candidate_tile = other_tile

    # Try four rotations, flip, try four rotations
    for i in range(8):
        if i == 4:
            candidate_tile = np.flip(candidate_tile, 0)

        edge = get_edge(candidate_tile, mirror_direction)
        if np.array_equal(edge, edge_to_match):
            return candidate_tile

        candidate_tile = np.rot90(candidate_tile)

    return None


# The coordinates of a sea creature in a 3x20 array
SEA_CREATURE_COORDS = [(0,18), 
                       (1,0), (1,5), (1,6), (1,11), (1,12), (1,17), (1,18), (1,19),
                       (2,1), (2,4), (2,7), (2,10), (2,13), (2,16)]


SEA_CREATURE_SIZE = len(SEA_CREATURE_COORDS)


def check_for_sea_creature(image, i, j):
    """
    Check whether there is a sea creature in the image at
    coordinates (i, j)
    """

    candidate_sea_creature = image[i:i+3,j:j+20]
    for k, l in SEA_CREATURE_COORDS:
        if candidate_sea_creature[k,l] == 0:
            return False

    return True


def count_sea_creatures(image):
    """
    Count the number of sea creatures in an image
    """
    N = len(image)
    num_sea_creatures = 0
    for i in range(N-4):
        for j in range(N-21):
            if check_for_sea_creature(image, i, j):
                num_sea_creatures += 1

    return num_sea_creatures


def ahash(array):
    """
    Given a 1-dimensional array of zeros and ones,
    return the integer that results from interpreting
    the array as a binary number. We use this as a hash
    to be able to assign identifiers to a tile's edges.
    """
    return np.sum(2**np.arange(len(array)-1, -1, -1) * array)


def read_tiles(input):
    """
    Read the tiles from the provided input.

    Besides reading the tiles into numpy arrays (with 0 for "."
    and 1 for "#"), it also returns a dictionary mapping tile
    numbers to the tiles that can be stitched to that tile
    """
    tile_nums = []
    tiles = {}
    tile_edges = {}
    for tile_txt in input:
        lines = tile_txt.split("\n")
        tile_num_txt = lines.pop(0)
        tile_num = int(tile_num_txt.split()[1][:-1])

        array = []
        for line in lines:
            array_row = []
            for c in line:
                if c == ".":
                    array_row.append(0)
                elif c== "#":
                    array_row.append(1)
            array.append(array_row)
        tile = np.array(array)

        tile_nums.append(tile_num)

        tiles[tile_num] = tile

        # We can convert each edge to an integer (by interpreting it
        # like a binary number), which makes it easier to check whether
        # two tiles have edges in common.
        # For each tile, we add four edges: the four edges exactly as given
        # and those same four edges but flipped.
        tile_edges[tile_num] = set()
        tile_edges[tile_num].add(ahash(tile[0]))
        tile_edges[tile_num].add(ahash(tile[-1]))
        tile_edges[tile_num].add(ahash(np.flip(tile[0])))
        tile_edges[tile_num].add(ahash(np.flip(tile[-1])))
        tile_edges[tile_num].add(ahash(tile[:,0]))
        tile_edges[tile_num].add(ahash(tile[:,-1]))
        tile_edges[tile_num].add(ahash(np.flip(tile[:,0])))
        tile_edges[tile_num].add(ahash(np.flip(tile[:,-1])))

    # Create an adjacency dictionary mapping tile number to the tiles
    # that could potentially be stiched to it.
    adjacencies = {tile_num:set() for tile_num in tile_nums}
    for i, tile_num1 in enumerate(tile_nums):
        for j in range(i+1, len(tile_nums)):
            tile_num2 = tile_nums[j]
            common_edges = tile_edges[tile_num1].intersection(tile_edges[tile_num2])
            if len(common_edges) > 0:
                adjacencies[tile_num1].add(tile_num2)
                adjacencies[tile_num2].add(tile_num1)

    return tiles, adjacencies


def find_corners(input):
    """
    Find the corners. We do this by computing the adjacencies of each tile,
    and identifying the ones with just two adjacencies.
    """

    _, adjacencies = read_tiles(input)

    corners = []
    for tile_num, edges in adjacencies.items():
        if len(edges) == 2:
            corners.append(tile_num)

    return math.prod(corners)
        
    
def get_top_left_corner(corner_num, tiles, adjacencies):
    """
    Given a corner tile, rotate/flip it so it can act as the top-left
    corner of the image. It can only have adjacent tiles to the
    right and to the bottom
    """
    corner = tiles[corner_num]

    # Try four rotations, flip, try four rotations
    for i in range(8):
        if i == 4:
            corner = np.flip(corner, 0)

        has_right = False
        has_down = False
        for tile_num in adjacencies[corner_num]:
            if test_adjacency(corner, tiles[tile_num], "right") is not None:
                has_right = True
            if test_adjacency(corner, tiles[tile_num], "down") is not None:
                has_down = True

        if has_right and has_down:
            return corner

        corner = np.rot90(corner)

    return None


def stitch_image(tiles, adjacencies):
    """
    Stitch together the tiles into an image.
    """

    # We create NxN lists to contain the tile numbers in the stitched
    # image, and the tiles themselves (represented as numpy arrays)
    # Initially, all values are set to None.
    N = int(math.sqrt(len(tiles)))
    image_tilenums = []
    image_arrays = []
    for _ in range(N):
        image_tilenums.append([None] * N)
        image_arrays.append([None] * N)

    # Pick an arbitrary corner
    for tile_num, edges in adjacencies.items():
        if len(edges) == 2:
            corner_num = tile_num
            break

    # We want this corner to specifically act as the top-left corner,
    # which means we need to find a rotation/flip of this tile such that
    # it only has tiles adjacent to the right and to its bottom.
    corner = get_top_left_corner(corner_num, tiles, adjacencies)

    # Set the corner as the top-left tile
    image_tilenums[0][0] = corner_num
    image_arrays[0][0] = corner

    # List of tiles that remain to be stitched
    remaining_tiles = list(tiles.keys())
    remaining_tiles.remove(corner_num)

    # Fill in first row. Starting from the top-left corner, go right
    # and find tiles that can be stitched in that direction.
    for i in range(1, N):
        prev_tilenum = image_tilenums[0][i-1]
        prev_tile = image_arrays[0][i-1]

        for r in remaining_tiles:
            if r in adjacencies[prev_tilenum]:
                # Possible match! Can we stitch it to the right?
                adj_tile = test_adjacency(prev_tile, tiles[r], "right")
                if adj_tile is not None:
                    image_tilenums[0][i] = r
                    image_arrays[0][i] = adj_tile        
                    remaining_tiles.remove(r)
                    break

    # Once we have the first row, we can now start filling downwards.
    for i in range(0, N):
        for j in range(1, N):
            prev_tilenum = image_tilenums[j-1][i]
            prev_tile = image_arrays[j-1][i]

            for r in remaining_tiles:
                if r in adjacencies[prev_tilenum]:
                    # Possible match! Can we stitch it going down?
                    adj_tile = test_adjacency(prev_tile, tiles[r], "down")
                    if adj_tile is not None:
                        image_tilenums[j][i] = r
                        image_arrays[j][i] = adj_tile        
                        remaining_tiles.remove(r)
                        break

    # Stitch all the tiles together into an image
    row_arrays = []
    for row in image_arrays:
        row_subarrays = [a[1:-1,1:-1] for a in row]
        row_array = np.concatenate(row_subarrays, axis=1)
        row_arrays.append(row_array)

    image = np.concatenate(row_arrays)

    return image


def compute_roughness(input):
    """
    Stitch the tiles into an image, and then rotate/flip it until
    we find the sea creatures (and, from there, the roughness)
    """
    tiles, adjacencies = read_tiles(input)

    image = stitch_image(tiles, adjacencies)

    # Try four rotations, flip, try four rotations
    for i in range(8):
        if i == 4:
            image = np.flip(image, 0)
            
        num_sea_creatures = count_sea_creatures(image)
        if num_sea_creatures > 0:
            return np.sum(image) - (num_sea_creatures * SEA_CREATURE_SIZE)

        image = np.rot90(image)

    return None  


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/20.in", sep="\n\n")
    input = util.read_strs("input/20.in", sep="\n\n")

    print("TASK 1")
    util.call_and_print(find_corners, sample)
    util.call_and_print(find_corners, input)

    print("\nTASK 2")
    util.call_and_print(compute_roughness, sample)
    util.call_and_print(compute_roughness, input)

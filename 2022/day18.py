"""
Day 18
https://adventofcode.com/2022/day/18

1st star: 00:06:58
2nd star: 00:46:49

This was a nice palate cleanser after the previous two days, and
felt more like a fun puzzle than a gratuitously difficult problem.
Part 1 was pretty straightforward and, for Part 2, I ended up
using BFS to find all the connected components (and then
subtracting the ones that corresponded to air)
"""

import util
import math
import sys
import re

from util import log


DIRECTIONS = [(-1,0,0),
               (1,0,0),
               (0,1,0),
               (0,-1,0),
               (0,0,1),
               (0,0,-1)]

# We need to increase the recursion limit for BFS to work
# in this problem
sys.setrecursionlimit(7500)

def find_connected_volumes(cubes):
    """
    Find the connected volumes in the provided cubes. We take the
    approach of defining a bounding volume around the cubes
    (that would correspond to the air *around* the lava, as opposed
    to the air trapped inside it). We then use BFS to find the
    connected volumes, distinguishing between "air volumes" and
    "lava volumes"
    """

    # Set the bounds of the bounding volume
    min_x = min(x for x, _, _ in cubes) - 1
    max_x = max(x for x, _, _ in cubes) + 1
    min_y = min(y for _, y, _ in cubes) - 1 
    max_y = max(y for _, y, _ in cubes) + 1
    min_z = min(z for _, _, z in cubes) - 1
    max_z = max(z for _, _, z in cubes) + 1    

    def bfs3d(volume, x, y, z, is_lava, visited):
        """
        BFS function that does most of the heavy lifting.
        """

        # Skip coordinates that are out of bounds
        if not (min_x <= x <= max_x and min_y <= y <= max_y and min_z <= z <= max_z):
            return

        # Skip coordinates we have visited
        if (x, y, z) in visited:
            return

        # If we're filling a lava volume, skip
        # the coordinates if they don't correspond
        # to a cube. Similarly, skip coordinates
        # that correspond to a cube if we're filling
        # an air volume
        is_cube = (x, y, z) in cubes
        if is_lava and not is_cube:
            return
        if not is_lava and is_cube:
            return

        # Add the coordinates to the volume and visited sets
        visited.add((x,y,z))
        volume.add((x,y,z))

        # Recursively check neighboring coordinates
        for dx, dy, dz in DIRECTIONS:
            bfs3d(volume, x+dx, y+dy, z+dz, is_lava, visited)

    # Check every coordinate in the bounding volume (most of these
    # will get skipped as we fill in the visited set)
    visited = set()
    volumes = []
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            for z in range(min_z, max_z+1):
                if (x,y,z) not in visited:
                    # Will this be a lava volume?
                    is_lava = (x, y, z) in cubes

                    # Determine the volume starting at x, y, z
                    volume = set()
                    bfs3d(volume, x, y, z, is_lava, visited)
                    volumes.append((volume, is_lava))

    # The first volume (starting at coordinates min_x, min_y, min_z)
    # corresponds to the bounding volume, so we discard it.
    volumes.pop(0)

    return volumes


def count_exposed(cubes, exclude_air=False):
    """
    Count the number of exposed surfaces, potentially excluding
    air trapped inside the lava.
    """

    # Find the total number of exposed surfaces.
    # For each cube, we check whether there is another
    # cube in any of its six sides
    total_exposed = 0
    for x, y, z in cubes:
        for dx, dy, dz in DIRECTIONS:
            if (x+dx, y+dy, z+dz) not in cubes:
                total_exposed += 1

    if exclude_air:
        # If we're excluding air, find the connected volumes,
        # and subtract the ones that are made up of air.
        volumes = find_connected_volumes(cubes)

        for volume, is_lava in volumes:
            if not is_lava:
                total_exposed -= count_exposed(volume)        

    return total_exposed


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/18.in", sep="\n", sep2=",")
    input = util.read_ints("input/18.in", sep="\n", sep2=",")

    sample_cubes = {tuple(cube) for cube in sample}
    input_cubes = {tuple(cube) for cube in input}

    print("TASK 1")
    util.call_and_print(count_exposed, sample_cubes)
    util.call_and_print(count_exposed, input_cubes)

    print("\nTASK 2")
    util.call_and_print(count_exposed, sample_cubes, True)
    util.call_and_print(count_exposed, input_cubes, True)

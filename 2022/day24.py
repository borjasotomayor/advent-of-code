"""
Day 24
https://adventofcode.com/2022/day/24

1st star: 11:57:58 (*)
2nd star: 12:06:41 (*)

(*) I was on vacation this day, so I didn't solve it until
    the morning after.

I approached this problem as a breadth-first search where you
had to account for the fact that the map changes at each step,
which means you're really doing a BFS through a three-dimensional
space (where time is the third dimension)

The main insight is realizing that the position of the blizzards
repeats every lcm(width, height) steps. Given the relatively
small size of the maps, you can just pre-compute the position
of the blizzards at every step, instead of computing them
on-the-fly during the BFS.
"""

import util
import math
import sys
import re

from util import log

def update_blizzards(blizzards, mx, my):
    """
    Given a set of (bx, by, bdir), where bx, by is the
    position of the blizzard and bdir is the direction,
    find the next positions of the blizzards (taking into
    account the maximum x and y of the map, mx and my)
    """
    new_blizzards = set()

    for x, y, dir in blizzards:
        if dir == ">":
            if x == mx-2:
                nx, ny = 1, y
            else:
                nx, ny = x+1, y
        if dir == "<":
            if x == 1:
                nx, ny = mx-2, y
            else:
                nx, ny = x-1, y
        if dir == "v":
            if y == my-2:
                nx, ny = x, 1
            else:
                nx, ny = x, y+1
        if dir == "^":
            if y == 1:
                nx, ny = x, my-2
            else:
                nx, ny = x, y-1
        new_blizzards.add((nx,ny,dir))
    
    return new_blizzards

def draw_map(mx, my, ex, ey, blizzards):
    """
    For debugging purposes only. Draw the map, 
    including the blizzards and the position of
    the expedition.
    """
    grid = util.Grid.empty(mx, my, ".")

    # Draw the walls
    for x in range(mx):
        grid.set(x, 0, "#")
        grid.set(x, my-1, "#")

    for y in range(my):
        grid.set(0, y, "#")
        grid.set(mx-1, y, "#")

    # Draw the start and end points
    grid.set(1, 0, " ")
    grid.set(mx-2, my-1, " ")

    # Draw the blizzards
    for bx, by, dir in blizzards:
        v = grid.get(bx, by)
        if v == ".":
            grid.set(bx, by, dir)
        elif v in ("<", ">", "^", "v"):
            grid.set(bx, by, "2")
        elif v.isnumeric():
            grid.set(bx, by, int(v)+1)

    # Draw the expedition
    grid.set(ex, ey, "E")

    print(grid)


def compute_blizzard_positions(blizzards, mx, my):
    """
    Pre-compute the positions of the blizzards from
    step 0 to step LCM(mx-2, my-2) and place them
    into a list. Since the positions repeat after
    LCM(mx-2, my-2), we can just index into this
    list modulo LCM(mx-2, my-2) to find the position
    of the blizzards at any given step.
    """
    lcm = abs((mx-2)*(my-2)) // math.gcd(mx-2, my-2)
    
    blizzards_pos = [None] * lcm

    for i in range(lcm):
        blizzards_pos[i] = blizzards
        blizzards = update_blizzards(blizzards, mx, my)

    return blizzards_pos


def blizzard_bfs(blizzards_pos, mx, my, sx, sy, sstep, tx, ty):
    """
    Do a breadth-first where:
    
     - mx, my are the maximum x and y of the map (i.e., the
       width and length)
     - sx, sy are the starting coordinates
     - sstep is the step ("minute") at which we start
     - tx, ty are the target coordinates
    """

    # See compute_blizzard_positions for the significance
    # of this LCM
    lcm = abs((mx-2)*(my-2)) // math.gcd(mx-2, my-2)

    # We greedily explore moves that get us closer to the target first,
    # followed by staying put and moving backwards.
    DIRECTIONS = [(+1, 0), (0, +1), (0, 0), (0, -1), (-1,  0)]

    # Queue
    q = []
    q.append((sx,sy,sstep))

    # Set of visited locations
    visited = {(sx,sy,sstep)}

    # Distance and previous-location dictionaries
    dist = {}
    dist[(sx,sy,sstep)] = 0
    prev = {}
    prev[(sx,sy,sstep)] = None
    target = None

    # Ye olde BFS loop
    while len(q) > 0:
        cur = q.pop(0)
        cx, cy, cstep = cur

        # Check if we've reached the target
        if (cx, cy) == (tx, ty):
            target = cur
            break

        # Check the neighbors
        for dx, dy in DIRECTIONS:
            neigh = (cx+dx, cy+dy, cstep+1)
            nx, ny, nstep = neigh 

            # Don't check neighbors that are out of bounds
            if not (1 <= nx <= mx-2 and 1 <= ny <= my-2):
                if not( (nx, ny) == (sx, sy) or (nx, ny) == (tx, ty) ):
                    continue
            
            # Don't check neighbors we've already visited
            if (nx, ny, cstep+1) in visited:
                continue

            # Find the position of the blizzards at this step
            blizzards = blizzards_pos[nstep%lcm]

            # Don't explore neighbors that contain a blizzard
            if any((nx, ny, dir) in blizzards for dir in ("^", "v", ">", "<")):
                continue

            visited.add((nx, ny, cstep+1))
            prev[neigh] = cur
            dist[neigh] = dist[cur] + 1
            q.append(neigh)
    
    # Generate path
    path = [target]
    pos = target
    while pos != (sx,sy,sstep):
        pos = prev[pos]
        path.append(pos)
    path.reverse()

    return path


def read_input(input):
    """
    Reads the input. We really only care about the position
    of the blizzards
    """
    max_x = len(input[0])
    max_y = len(input)

    blizzards = set()
    for x in range(max_x):
        for y in range(max_y):
            v = input[y][x]
            if v in ("<", ">", "v", "^"):
                blizzards.add((x,y,v))

    return blizzards, max_x, max_y


def find_best_path(input, num_trips=1):
    blizzards, mx, my = read_input(input)

    # Starting coordinates
    sx, sy = 1, 0

    # Target coordinates
    tx, ty = mx-2, my-1

    # Pre-compute the blizzard positions at each step
    blizzards_pos = compute_blizzard_positions(blizzards, mx, my)

    # Make the trips
    sstep = 0
    total_path = []
    for _ in range(num_trips):
        path = blizzard_bfs(blizzards_pos, mx, my, sx, sy, sstep, tx, ty)

        # Extract the final coordinates of the path
        fx, fy, fstep = path[-1]
        assert (tx, ty) == (fx, fy)

        if len(total_path) > 0:
            total_path.pop()

        total_path += path

        # Flip the start and target coordinates,
        # and update the step number
        sx, sy, tx, ty = tx, ty, sx, sy
        sstep = fstep

    return len(total_path) - 1


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/24-1.in", sep="\n")
    sample2 = util.read_strs("input/sample/24-2.in", sep="\n")
    input = util.read_strs("input/24.in", sep="\n")

    print("TASK 1")
    util.call_and_print(find_best_path, sample2)
    util.call_and_print(find_best_path, input)

    print("\nTASK 2")
    util.call_and_print(find_best_path, sample2, 3)
    util.call_and_print(find_best_path, input, 3)

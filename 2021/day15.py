"""
Day 15
https://adventofcode.com/2021/day/15

1st star: 00:52:41
2nd star: 01:19:31

This took me way longer than expected because of 30 minutes tracking
down this silly bug:

    nx, ny = x+dx, y+dx

And then having to re-learn Dijkstra's from scratch, even though I
really should review it before AoC starts each year. That said,
after those hurdles, it was a pretty satisfying application of
Dijkstra's algorithm on an atypical (non-graph) setting.
"""

import util
import sys

import heapq
from util import log


def get_risk(grid, x, y, tiling):
    """
    Compute the risk, taking into account the tiling.
    """

    tile_size = grid.max_x

    tile_x = x // tile_size
    tile_y = y // tile_size

    if not (0 <= tile_x <= tiling-1) or not (0 <= tile_y <= tiling-1):
        return None

    ox = x % tile_size
    oy = y % tile_size

    risk = grid.get(ox, oy)

    tile_distance = tile_x + tile_y

    adjusted_risk = risk + tile_distance

    # Evil wrap-around
    if adjusted_risk > 9:
        adjusted_risk -= 9

    return adjusted_risk


def find_min_risk(grid, tiling):
    """
    Find the path with the lowest total risk, using Dijkstra's Algorithm.
    """

    start = (0, 0)
    end = (grid.max_x*tiling-1, grid.max_y*tiling-1)

    # List that we'll use like a priority queue with heapq
    h = []

    # Distance and previous-node dictionaries
    node_dist = {}
    node_dist[start] = 0
    prev = {}
    prev[start] = None

    # Add the start node
    heapq.heappush(h, (0, start))

    # Ye olde Dikstra loop
    while len(h) > 0:
        dist, cur_node = heapq.heappop(h)

        # We've reached the end and don't need to check further
        if cur_node == end:
            break

        # Check the neighbors
        x, y = cur_node
        for dx, dy in util.Grid.CARDINAL_DIRS:
            
            nx, ny = x+dx, y+dy

            adj_risk = get_risk(grid, nx, ny, tiling)

            if adj_risk is None:
                continue

            # Update distance/prev/queue if necessary
            new_distance = node_dist[cur_node] + adj_risk
            if new_distance < node_dist.get((nx,ny), sys.maxsize):
                node_dist[(nx,ny)] = new_distance
                prev[(nx,ny)] = cur_node
                heapq.heappush(h, (new_distance, (nx,ny)))

    return node_dist[end]


def task1(grid):
    """
    Task 1: Find the min-risk path with no tiling
    """
    return find_min_risk(grid, tiling=1)


def task2(grid):
    """
    Task 1: Find the min-risk path with 5x5 tiling
    """
    return find_min_risk(grid, tiling=5)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.Grid.from_file("input/sample/15.in", cast=int)
    input = util.Grid.from_file("input/15.in", cast=int)

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)

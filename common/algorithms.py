"""
This file contains a couple of useful algorithms that tend to
come in handy in some Advent of Code problems.

- Depth-First Search on graphs
- Depth-First Search on grids (using my util.Grid class)
- Dijkstra's shortest path algorithm

Each algorithm includes a test_algorithm function with a simple
test to show how to set up the data structures and use the algorithm.
Running this Python file will run all the tests.
"""

###############################################################################
# 
#  GRAPH DEPTH-FIRST SEARCH
# 
###############################################################################   

def dfs(graph, start_node, visit_func=print):
    """
    Depth-first search (DFS) on a graph

    Parameters:
    - graph: The graph to do DFS on. It should be provided as a
             dictionary mapping node labels (strings) to lists of
             node labels (the neighbors of the node)
    - start_node: The node label to start DFS on
    - visit_func: A function that will be called on each node

    Returns: nothing
    """

    def dfs_r(graph, start_node, visit_func, visited):
        if start_node in visited:
            return

        visited.add(start_node)
        visit_func(start_node)
        for neighbor in graph[start_node]:
            dfs_r(graph, neighbor, visit_func, visited)

    # Call the recursive function with an empty set of visited nodes
    dfs_r(graph, start_node, visit_func, visited=set())

def test_graph_dfs():
    graph = {"A": ["B", "C"],
             "B": ["A", "C", "D", "E"],
             "C": ["A", "B", "D", "E"],
             "D": ["B", "C", "E", "F"],
             "E": ["B", "C", "D", "F"],
             "F": ["D", "E"]}

    print("DFS Starting at A")
    dfs(graph, "A")

    print("\nDFS starting at E")
    dfs(graph, "E")


###############################################################################
# 
#  GRID DEPTH-FIRST SEARCH
# 
###############################################################################       

from util import Grid

def grid_dfs(grid, x, y, visit_func, iswall_func):
    """
    Depth-first search (DFS) on a grid.

    Parameters:
    - grid: The grid to do DFS on ()
    - x, y: The coordinates to start DFS on
    - visit_func: A function that will be called on each position
                  of the grid. Function must take (grid, x, y)
                  as parameters.
    - iswall_func: A function that determinesw hether a given
                   coordinate of a grid is a "wall" (and should 
                   not be processed). Must take (grid, x, y)
                   as parameters.

    Returns: nothing
    """

    def grid_dfs_r(grid, x, y, visit_func, iswall_func, visited):
        if not grid.valid(x, y):
            return

        if iswall_func(grid, x, y):
            return

        if (x,y) in visited:
            return
        
        visited.add((x,y))
        visit_func(grid, x, y)

        for dx, dy in Grid.CARDINAL_DIRS:
            grid_dfs_r(grid, x+dx, y+dy, visit_func, iswall_func, visited)

    # Call the recursive function with an empty set of visited nodes
    grid_dfs_r(grid, x, y, visit_func, iswall_func, visited=set())

def test_grid_dfs():

    # We're going to test our Grid DFS by doing flood-filling

    grid_str = \
"""
################
#..............#
#...######.....#
#...#.....#....#
#....#.....#...#
#... #....#....#
#....#####.....#
################
"""

    grid = Grid.from_string(grid_str)

    def visit(grid, x, y):
        grid.set(x, y, "x")

    def is_wall(grid, x, y):
        v = grid.get(x, y)
        return v == "#"


    print(grid)

    grid_dfs(grid, 7, 5, visit, is_wall)

    print()
    print(grid)

    grid_dfs(grid, 1, 1, visit, is_wall)

    print()
    print(grid)

###############################################################################
# 
#  DIJKSTRA
# 
###############################################################################    

import heapq
import sys

def dijkstra(graph, from_node, to_node):
    """
    Dijkstra's shortest-path algorithm

    Parameters:
    - graph: The graph. It should be provided as a
             dictionary mapping node labels (strings) to lists of
             (node, distance) tuples (the neighbors of the node,
             and the distance to that neighbor)
    - from_node, to_node: The nodes we want to find the shortest
                          distance between

    Returns: The shortest distance, and the shortest path
    """

    # List that we'll use like a priority queue with heapq
    h = []

    # Distance and previous-node dictionaries
    node_dist = {}
    node_dist[from_node] = 0
    prev = {}
    prev[from_node] = None

    # Add the start node
    heapq.heappush(h, (0, from_node))

    # Ye olde Dikstra loop
    while len(h) > 0:
        dist, cur_node = heapq.heappop(h)

        # We've reached the end and don't need to check further
        if cur_node == to_node:
            break

        # Check the neighbors
        for neighbor, distance in graph[cur_node]:
            # Update distance/prev/queue if necessary
            new_distance = node_dist[cur_node] + distance
            if new_distance < node_dist.get(neighbor, sys.maxsize):
                node_dist[neighbor] = new_distance
                prev[neighbor] = cur_node
                heapq.heappush(h, (new_distance, neighbor))

    # Generate path
    path = [to_node]
    node = to_node
    while node != from_node:
        node = prev[node]
        path.append(node)
    path.reverse()

    return node_dist[to_node], path

def test_dijkstra():
    graph = {"A": [("B",20), ("C",10)],
             "B": [("A",20), ("C",20), ("D",15), ("E", 5)],
             "C": [("A",10), ("B",20), ("D",50), ("E",20)],
             "D": [("B",15), ("C",50), ("E", 5), ("F",10)],
             "E": [("B", 5), ("C",20), ("D", 5), ("F",30)],
             "F": [("D",10), ("E",30)]}

    print("Dijkstra A -> F")
    print(dijkstra(graph, "A", "F"))

    print("Dijkstra D -> A")
    print(dijkstra(graph, "D", "A"))


###############################################################################       


if __name__ == "__main__":
    test_graph_dfs()
    print()
    test_grid_dfs()
    print()
    test_dijkstra()

"""
Day 6
https://adventofcode.com/2019/day/6

1st star: 00:13:43
2nd star: 00:31:57

This turned out to be a pretty straightforward if you're comfortable with
recursion which, fortunately, I was knee-deep in at the time due to my teaching.
"""

import util

def compute_orbits(graph, pre):
    """
    Compute the number of direct an indirect orbits
    """

    def visit(node):
        """
        Traverse the graph recursively, counting up the orbits
        """
        if node not in pre:
            num_orbits[node] = 0
        else:
            num_orbits[node] = 1 + num_orbits[pre[node]]

        next = [n for n in graph.get(node, []) if n != pre.get(node)]

        for child in next:
            visit(child)

    # The origin is the node with no predecessor
    origin = set(graph.keys()) - set(pre.keys())
    origin = origin.pop()

    num_orbits = {}
    visit(origin)

    return sum(num_orbits.values())


def shortest_path(graph, start, end, visited=None):
    """
    Use DFS to find the shortest path between two nodes.
    """

    if visited is None:
        visited = set()

    if start not in visited:
        visited.add(start)

    if start == end:
        return [end]
    else:      
        smallest = None
        for child in graph[start]:
            if child not in visited:
                rem_route = shortest_path(graph, child, end, visited)
                if not rem_route is None:
                    route = [start] + rem_route
                    if smallest is None:
                        smallest = route
                    elif len(route) < len(smallest):
                        smallest = route
        return smallest


def read_graph(input):
    """
    Read the graph from the provided input.

    Returns the graph as a dictionary, as well as a dictionary
    mapping each node to its predecessor.
    """
    orbits = [x.split(")") for x in input]

    graph = {}
    pre = {}

    for p1, p2 in orbits:
        graph.setdefault(p1, []).append(p2)
        graph.setdefault(p2, []).append(p1)
        pre[p2] = p1

    return graph, pre


def task1(input):
    """
    Task 1: Count orbits
    """
    graph, pre = read_graph(input)

    return compute_orbits(graph, pre)


def task2(input):
    """
    Task 2: Find the minimum number of orbit transfers (the length
    of the shortest path)
    """
    graph, _ = read_graph(input)

    shortest = shortest_path(graph, "YOU", "SAN")

    return len(shortest) - 3


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/06-1.in", sep="\n")
    sample2 = util.read_strs("input/sample/06-2.in", sep="\n")
    input = util.read_strs("input/06.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample1)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample2)
    util.call_and_print(task2, input)


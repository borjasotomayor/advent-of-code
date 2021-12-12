"""
Day 12
https://adventofcode.com/2021/day/12

1st star: 00:10:42	
2nd star: 00:26:44

The first part of this problem was a pretty standard DFS, but in the second
part I ended up writing an overcomplicated solution involving passing a
dictionary of counts of visited nodes, but which got the job done. Once
I got the second star, I though about it a bit more and rewrote the code
so it just uses a set of visited nodes, plus an additional boolean variable
to keep track of whether we've visited a small cave twice already.
"""

import util
import math
import sys
import re

from util import log


def gen_paths_r(graph, start, target, visited, allow_second_visit, second_visit_done):
    """
    Recursively compute all the paths from "start" to "target" in "graph", using "visited"
    to keep track of visited nodes. "allow_second_visit" tells us whether we're allowed
    to visit a lowercase node a second time and, if so, "second_visit_done" tells us 
    if we've already visited such a node twice.
    """

    # Base case: we've reached the target node
    if start == target:
        return [[target]]

    # We use this variable to keep track of whether we added the
    # start node to the visited set (since, unlike regular DFS,
    # this won't happen unconditionally). This allows us to
    # remove the node from the list of visited nodes at the
    # end of the function.
    added = False
    if start.islower():
        if start in visited:
            # The function shouldn't be called on the same node
            # unless we (1) are allowing second visits and 
            # (2) have yet to make the second visit to a small cave
            assert allow_second_visit and not second_visit_done

            second_visit_done = True
        else:
            visited.add(start)
            added = True

    paths = []
    for next in graph[start]:
        if next == "start":
            continue

        # Kinda verbose way of checking whether to go
        # to the next node, to avoid having a gigantic
        # boolean expression in the if before the recursive
        # call.
        follow_next = False
        if allow_second_visit:
            if not second_visit_done:
                follow_next = True
            elif second_visit_done and next not in visited:
                follow_next = True
        elif not allow_second_visit and next not in visited:
            follow_next = True

        if follow_next:
            # Recursive case: we get the paths starting from the next node...
            next_paths = gen_paths_r(graph, next, target, visited,
                                     allow_second_visit, second_visit_done)

            # ... and we slap a start node at the front of each path
            for np in next_paths:
                paths.append([start] + np)

    if added:
        visited.discard(start)

    return paths


def gen_paths(graph, start, target, allow_second_visit):
    """
    Wrapper function for gen_paths_r
    """
    return gen_paths_r(graph, start, target, set(), 
                       allow_second_visit, second_visit_done=False)


def read_graph(input):
    """
    Reads the input into a dictionary representing a graph
    """
    graph = {}
    
    for line in input:
        a, b = line.split("-")
        graph.setdefault(a,set()).add(b)
        graph.setdefault(b,set()).add(a)

    return graph


def task1(input):
    """
    Task 1: Second visits not allowed
    """
    graph = read_graph(input)
    paths = gen_paths(graph, "start", "end", allow_second_visit=False)

    return len(paths)


def task2(input):
    """
    Task 2: Second visits allowed
    """
    graph = read_graph(input)
    paths = gen_paths(graph, "start", "end", allow_second_visit=True)

    return len(paths)


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/12-1.in", sep="\n")
    sample2 = util.read_strs("input/sample/12-2.in", sep="\n")
    sample3 = util.read_strs("input/sample/12-3.in", sep="\n")
    input = util.read_strs("input/12.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample1)
    util.call_and_print(task1, sample2)
    util.call_and_print(task1, sample3)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample1)
    util.call_and_print(task2, sample2)
    util.call_and_print(task2, sample3)
    util.call_and_print(task2, input)

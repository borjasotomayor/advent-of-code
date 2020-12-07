"""
Day 7
https://adventofcode.com/2020/day/7

1st star: 00:21:25
2nd star: 00:31:54

Welp, I guess it's time to start reviewing basic graph algorithms.
Lost a fair amount of time trying to fetch DFS from my brain's L3 cache but,
once that was done, this involved some pretty routine graph traversals.

The original parsing was also much uglier in my original version (using
lots of repeated calls to the split() method). I cleaned it up a bit
by using a regex to parse out the basic components contained in each line.
"""

import util
import math
import sys
import re


from util import log

def read_rules(lines):
    """
    Given the text input, convert it to a graph-like structure.
    Specifically, a dictionary mapping colors to a list of (color, amount)
    tuples.
    """

    rules = {}

    for line in lines:
        m = re.match("(.*) bags contain (.*)\.", line)
        container_bag, contained_bags = m.groups()

        if contained_bags == "no other bags":
            bags = []
        else:
            bags = []
            bag_strs = contained_bags.split(", ")
            for bag in bag_strs:
                amount, color1, color2, _ = bag.split()
                bags.append((f"{color1} {color2}", int(amount)))
            
        rules[container_bag] = bags

    return rules


def is_reachable(rules, start_color, target_color, visited=None):
    """
    Do a depth-first search to check whether target_color
    is reachable from start_color.

    The provided rules don't seem to contain any cycles,
    so, strictly speaking, we wouldn't need to keep track
    of the set of visited nodes.
    """

    if visited is None:
        visited = set()

    visited.add(start_color)
    for color, _ in rules[start_color]:
        if color == target_color:
            return True
        else:
            if color not in visited:
                if is_reachable(rules, color, target_color):
                    return True

    return False


def task1(lines):
    """
    Task 1: for each bag color, check whether "shiny gold"
    is reachable from that color
    """
    rules = read_rules(lines)

    count = 0
    for color in rules:
        if is_reachable(rules, color, "shiny gold"):
            count += 1

    return count


def count_bags(rules, start_color):
    """
    Count all the bags that are stored inside start_color
    Assumes no cycles in the graph.
    """
    bags = rules[start_color]

    n_bags = 0
    for color, amount in bags:
        # Add the bag immediately contained inside start_color...
        n_bags += amount

        # ... and recursively count the bags contained in that bag.
        n_sub_bags = count_bags(rules, color)        
        n_bags += amount * n_sub_bags

    return n_bags


def task2(lines):
    rules = read_rules(lines)
    return count_bags(rules, "shiny gold")



if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/07-1.in", sep="\n")
    sample2 = util.read_strs("input/sample/07-2.in", sep="\n")

    lines = util.read_strs("input/07.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, lines)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, sample2)
    util.call_and_print(task2, lines)

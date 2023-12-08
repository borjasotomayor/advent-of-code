"""
Day 8
https://adventofcode.com/2023/day/8

1st star: 00:08:20
2nd star: 00:36:38

The first part of the problem was pretty straightforward and,
not surprisingly, that solution turned out to be too inefficient
for Part 2. At first, I thought (and hoped) that memoization was
enough to make it run faster, but no luck.

I eventually figured out this involved taking the Least Common Multiple
of the number of steps required to reach a **Z label from each starting
point. In hindsight, I should've paid more attention to how the
labels were highlighted in the second part, hinting at their periodicity.
"""

import util
import math

from parse import parse


def read_input(input: list[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    """
    Reads the input into a direction string and a dictionary mapping
    labels to their left/right labels.
    """
    directions = input[0]

    network = {}
    for line in input[2:]:
        label, left, right = parse("{} = ({}, {})", line)
        network[label] = (left, right)

    return directions, network


def find_steps_to_z(start: str, directions: list[str],
                    network: dict[str, tuple[str, str]],
                    match_last_only: bool) -> int:
    """
    Starting at a given label, find the number of steps to the Z label
    (if match_last_only is True, we match any label with Z as its
    last character; otherwise, we match "ZZZ")
    """
    steps = 0
    cur = start
    while True:
        for dir in directions:
            if dir == "L":
                cur = network[cur][0]
            elif dir == "R":
                cur = network[cur][1]
            steps += 1
            if (match_last_only and cur[2] == "Z") or (not match_last_only and cur == "ZZZ"):
                return steps


def task1(directions: list[str], network: dict[str, tuple[str, str]]) -> int:
    """
    Task 1: Find the number of steps to ZZZ
    """
    return find_steps_to_z("AAA", directions, network, match_last_only=False)


def task2(directions: list[str], network: dict[str, tuple[str, str]]) -> int:
    """
    Task 2: Find the number of steps from all the **A labels
    to all the **Z labels
    """

    starting_labels = [k for k in network if k[2] == "A"]

    # Find the number of steps starting at each label
    steps = []
    for label in starting_labels:
        n = find_steps_to_z(label, directions, network, match_last_only=True)
        steps.append(n)

    # The answer is the Least Common Multiple of all the steps
    return math.lcm(*steps)


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/08-1.in", sep="\n")
    sample2 = util.read_strs("input/sample/08-2.in", sep="\n")
    sample3 = util.read_strs("input/sample/08-3.in", sep="\n")
    input = util.read_strs("input/08.in", sep="\n")

    dirs_sample_1, network_sample_1 = read_input(sample1)
    dirs_sample_2, network_sample_2 = read_input(sample2)
    dirs_sample_3, network_sample_3 = read_input(sample3)
    dirs, network = read_input(input)

    print("TASK 1")
    util.call_and_print(task1, dirs_sample_1, network_sample_1)
    util.call_and_print(task1, dirs_sample_2, network_sample_2)
    util.call_and_print(task1, dirs, network)

    print("\nTASK 2")
    util.call_and_print(task2, dirs_sample_3, network_sample_3)
    util.call_and_print(task2, dirs, network)

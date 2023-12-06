"""
Day 6
https://adventofcode.com/2023/day/6

1st star: 00:06:26
2nd star: 00:08:58

This was a pleasantly simple problem after being murdered by
the Day 5 problem. Like Day 5, there is a more clever solution
(computing the range using the quadratic formula) but
I coded a simple brute-force solution, and it happened to
work just fine (Part 2 just takes a few seconds to run).
"""

import util
import math


def compute_ways_to_win(time: int, distance: int) -> int:
    """
    Compute the number of ways to win in a race with a given
    time and distance
    """

    wins = 0
    # Check each possible way of conducting the race
    # (every possible duration for pressing the button)
    for time_pressing in range(time + 1):
        time_left = time - time_pressing
        speed = time_pressing
        new_distance = speed * time_left
        if new_distance > distance:
            wins += 1
        elif wins > 0 and new_distance < distance:
            # Bail out once we press the button so
            # long that we can't possibly win
            break

    return wins


def task1(input: list[str]) -> int:
    """
    Task 1: Compute the ways to win in several races
    """
    times = [int(x) for x in input[0].split()[1:]]
    distances = [int(x) for x in input[1].split()[1:]]

    wins = []
    for time, dist in zip(times, distances):
        n = compute_ways_to_win(time, dist)
        if n > 0:
            wins.append(n)

    return math.prod(wins)


def task2(input: list[str]) -> int:
    """
    Task 2: Computer the ways to win in one big race
    """
    time = int("".join(input[0].split()[1:]))
    dist = int("".join(input[1].split()[1:]))

    return compute_ways_to_win(time, dist)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/06.in", sep="\n")
    input = util.read_strs("input/06.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)

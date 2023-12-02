"""
Day 2
https://adventofcode.com/2023/day/2

1st star: 00:06:24
2nd star: 00:09:24

This was a welcome change of pace after getting murdered by
Part 2 of Day 1 :-P

My original solution had a lot of hard-coded values, and more
kludgy parsing, so I polished it up so the functions are a bit
more general (and could work with more colors, and not just the
red, green, blue colors in the problem).
"""

import math

from parse import parse

import util


def read_input(input: list[str]) -> dict[int, list[dict[str, int]]]:
    """
    Read the input and return a dictionary mapping game numbers
    to a list of dictionaries. Each dictionary represents a "subset of cubes",
    mapping color names to quantities.
    """
    games: dict[int, list[dict[str, int]]] = {}
    for line in input:
        game_num, subsets_str = parse("Game {:d}: {}", line)
        subsets_strs = subsets_str.split("; ")
        games[game_num] = []
        for subset in subsets_strs:
            cubes_strs = subset.split(", ")
            cubes = {}
            for c in cubes_strs:
                num, color = parse("{:d} {}", c)
                cubes[color] = num
            games[game_num].append(cubes)

    return games


def is_possible(sets: list[dict[str, int]], max_colors: dict[str, int]):
    """
    Is the game possible? Check that, for each set of cubes, the number
    of cubes of each color does not exceed the maximum specified in
    the max_colors dictionary
    """
    for s in sets:
        for color, max_color in max_colors.items():
            if s.get(color, 0) > max_color:
                return False

    return True


def sum_possible_games(input: list[str], max_colors: dict[str, int]) -> int:
    """
    Task 1: Add up the game numbers of all the possible games.
    """
    games = read_input(input)

    sum = 0
    for game_num, game in games.items():
        if is_possible(game, max_colors):
            sum += game_num

    return sum


def power(sets: list[dict[str, int]], colors: list[str]) -> int:
    """
    Compute the power of a game
    """
    d = {color: 0 for color in colors}
    for s in sets:
        for color in colors:
            d[color] = max(s.get(color, 0), d[color])

    return math.prod(d.values())


def sum_power(input: list[str], colors: list[str]) -> int:
    """
    Task 2: Add up the powers of all the games
    """
    games = read_input(input)

    sum = 0
    for game_num, game in games.items():
        sum += power(game, colors)

    return sum


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/02.in", sep="\n")
    input = util.read_strs("input/02.in", sep="\n")

    print("TASK 1")
    max_colors = {"red": 12, "green": 13, "blue": 14}
    util.call_and_print(sum_possible_games, sample, max_colors)
    util.call_and_print(sum_possible_games, input, max_colors)

    print("\nTASK 2")
    colors = ["red", "green", "blue"]
    util.call_and_print(sum_power, sample, colors)
    util.call_and_print(sum_power, input, colors)

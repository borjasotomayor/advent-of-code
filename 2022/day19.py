"""
Day 19
https://adventofcode.com/2022/day/19

1st star: 01:34:52
2nd star: 02:42:30

I briefly toyed with whether this required some fancy flow algorithm
to solve and instead opted for just doing a fairly brute-force 
depth-first search of every possible state (branching at each
minute, depending on the robots that could be built at each minute),
but also trying to prune the search space as much as possible.

This turned out to be a sensible approach, but I bungled up some
of the pruning heuristics, which involved a lot of debugging to
get Part 2 right. In the end, the only pruning I implemented
in my original solution was to give up on a path if it couldn't
possible produce as many geodes as the best number of geodes
we've seen so far. This was enough to produce the right solution
(although it took several minutes to do so), so I later added
two other pruning strategies mentioned in the subreddit:

(1) If you have enough (non-geode) robots to produce enough minerals
    per minute to build any robot that depends on those minerals,
    then there's no point in building more robots of that type.
(2) If you are able to build a geode robot, only explore that option
    (it is pointless to explore paths were you don't create the geode
    robot, since they'll always result in fewer geodes)
"""

import util
import math
import sys
import re

from util import log


class Blueprint:
    """
    Class for storing information about a blueprint
    """

    def __init__(self, id, ore_cost, clay_cost, 
                       obsidian_cost_ore, obsidian_cost_clay, 
                       geode_cost_ore, geode_cost_obsidian):
        self.id = id
        self.ore_cost = ore_cost
        self.clay_cost = clay_cost
        self.obsidian_cost_ore = obsidian_cost_ore
        self.obsidian_cost_clay = obsidian_cost_clay
        self.geode_cost_ore = geode_cost_ore
        self.geode_cost_obsidian = geode_cost_obsidian


def find_max_geodes(blueprint, ore, clay, obsidian, geode, 
                    ore_robots, clay_robots, obsidian_robots, geode_robots, 
                    minutes, best_score=0, memo={}):
    """
    Do a depth-first search of every possible action in every minute, and
    return the maximum number of geodes that can be generated. Along
    the way, do some judicious pruning of the search space.

    The ore, clay, obsidian, and geode parameters specify how many of each we have.

    The *_robots parameters specify how many of each robot we have.

    minutes is the number of minutes left

    best_score is used to keep track of the maximum number of geodes we've
    found so far (the "best score" so far)

    memo is a dictionary for memoization
    """

    # Memoization
    score = memo.get((ore, clay, obsidian, geode, ore_robots, clay_robots, obsidian_robots, geode_robots, minutes))
    if score is not None:
        return score

    # We compute the maximum possible number of geodes we could generate
    # starting from the current state. This is the number of geodes we
    # would generate if we were able to create a new geode robot every
    # minute of our remaining time (and added it to the number of)
    # geodes we already have. If that number is not larger than the
    # best score we've found so far, then this is not a productive
    # path to explore (since it can't possible be better than the
    # best score we've already found)
    max_possible_geodes = geode + (minutes * (2*geode_robots + minutes))/2
    if max_possible_geodes < best_score:
        return 0

    # If time's up, return the number of geodes
    if minutes == 0:
        return geode

    # Explore every possible action, and find the maximum number of geodes
    # starting from that action. We then pick the largest of all these values.
    scores = []

    # If we have enough minerals to build a geode robot, see what happens
    # if we build it.
    if ore >= blueprint.geode_cost_ore and obsidian >= blueprint.geode_cost_obsidian:
        score = find_max_geodes(blueprint,
                                ore + ore_robots - blueprint.geode_cost_ore,
                                clay + clay_robots,
                                obsidian + obsidian_robots - blueprint.geode_cost_obsidian,
                                geode + geode_robots,
                                ore_robots, clay_robots, obsidian_robots, geode_robots+1,
                                minutes - 1, best_score, memo)
        best_score = max(best_score, score)
        scores.append(score)
    else:
        # Notice how we don't explore any other options if we're able to build
        # a geode robot, since that's always the best action to take (if we
        # have enough minerals for it)

        # If we have enough minerals to build an obsidian robot, see what happens
        # if we build it *unless* we already have enough obsidian robots to
        # generate the obsidian for a geode robot (if so, getting more obsidian
        # robots is pointless)
        if obsidian_robots < blueprint.geode_cost_obsidian and ore >= blueprint.obsidian_cost_ore and clay >= blueprint.obsidian_cost_clay:
            score = find_max_geodes(blueprint,
                                    ore + ore_robots - blueprint.obsidian_cost_ore,
                                    clay + clay_robots - blueprint.obsidian_cost_clay,
                                    obsidian + obsidian_robots,
                                    geode + geode_robots,
                                    ore_robots, clay_robots, obsidian_robots+1, geode_robots,
                                    minutes - 1, best_score, memo)
            best_score = max(best_score, score)
            scores.append(score)

        # If we have enough minerals to build a clay robot, see what happens
        # if we build it *unless* we already have enough clay robots to
        # generate the clay for an obsidian robot (if so, getting more clay
        # robots is pointless)
        if clay_robots < blueprint.obsidian_cost_clay and ore >= blueprint.clay_cost:
            score = find_max_geodes(blueprint,
                                    ore + ore_robots - blueprint.clay_cost,
                                    clay + clay_robots,
                                    obsidian + obsidian_robots,
                                    geode + geode_robots,
                                    ore_robots, clay_robots+1, obsidian_robots, geode_robots,
                                    minutes - 1, best_score, memo)
            best_score = max(best_score, score)
            scores.append(score)            

        # If we have enough minerals to build an ore robot, see what happens
        # if we build it *unless* we already have enough ore robots to
        # generate the ore for whatever robot requires the most ore
        # (if so, getting more ore robots is pointless)
        if ore_robots < max(blueprint.clay_cost, blueprint.obsidian_cost_ore, blueprint.geode_cost_ore) and ore >= blueprint.ore_cost:
            score = find_max_geodes(blueprint,
                                    ore + ore_robots - blueprint.ore_cost,
                                    clay + clay_robots,
                                    obsidian + obsidian_robots,
                                    geode + geode_robots,
                                    ore_robots+1, clay_robots, obsidian_robots, geode_robots,
                                    minutes - 1, best_score, memo)
            best_score = max(best_score, score)
            scores.append(score)     

        # See what happens if we don't do anything.
        score = find_max_geodes(blueprint,
                                ore + ore_robots,
                                clay + clay_robots,
                                obsidian + obsidian_robots,
                                geode + geode_robots,
                                ore_robots, clay_robots, obsidian_robots, geode_robots,
                                minutes - 1, best_score, memo)
        
        scores.append(score)

    # Return the best score, and update the memoization dictionary
    best_score = max(scores)
    memo[(ore, clay, obsidian, geode, ore_robots, clay_robots, obsidian_robots, geode_robots, minutes)] = best_score

    return best_score


# f-String for parsing the input
BLUEPRINT_FSTRING = "Blueprint {:d}: Each ore robot costs {:d} ore. " + \
                    "Each clay robot costs {:d} ore. " + \
                    "Each obsidian robot costs {:d} ore and {:d} clay. " + \
                    "Each geode robot costs {:d} ore and {:d} obsidian."


def parse_input(input):
    """
    Parses the input into a list of Blueprint objects
    """
    blueprints = []
    for values in util.iter_parse(input, BLUEPRINT_FSTRING):
        b = Blueprint(*values)
        blueprints.append(b)
    return blueprints


def task1(blueprints):
    """
    Task 1: Find the quality level of each blueprint and return the sum.
    """
    quality_levels = []
    for i, b in enumerate(blueprints):
        num_geodes = find_max_geodes(b,0,0,0,0,1,0,0,0,24, memo={})
        
        log(f"Blueprint {i+1} produces {num_geodes} geodes")

        quality_levels.append((i+1)*num_geodes)

    return sum(quality_levels)


def task2(blueprints):
    """
    Task 2: Multiply the maximum number of geodes produced by the
            first three blueprints.
    """
    geodes = []
    for i, b in enumerate(blueprints[:3]):
        num_geodes = find_max_geodes(b,0,0,0,0,1,0,0,0,32, memo={})
        log(f"Blueprint {i+1} produces {num_geodes} geodes")

        geodes.append(num_geodes)

    return math.prod(geodes)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/19.in", sep="\n")
    input = util.read_strs("input/19.in", sep="\n")

    sample_blueprints = parse_input(sample)
    blueprints = parse_input(input)

    print("TASK 1")
    util.call_and_print(task1, sample_blueprints)
    util.call_and_print(task1, blueprints)

    print("\nTASK 2")
    util.call_and_print(task2, sample_blueprints)
    util.call_and_print(task2, blueprints)

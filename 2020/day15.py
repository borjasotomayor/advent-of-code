"""
Day 15
https://adventofcode.com/2020/day/15

1st star: 00:12:41
2nd star: 00:14:55

I think my love of caches helped me on this one, because I immediately 
gravitated towards caching the previous two turns (and only the previous
two turns) for every number in the first part, which meant the second part 
ran in a decent amount of time despite the larger inputs. It still takes 
several seconds to run, though, so I'm still wondering whether there's 
a more efficient solution.
"""

import util
import math
import sys
import re

from util import log


def memory_game(numbers, target):
    # Maps turns to numbers. Not strictly necessary, but useful
    # for debugging
    turns = {}

    # Maps numbers to a list with the turns when the number was
    # last mentioned (we only need to store up to two)
    prev_turns = {}
    
    # Initialize the first turns
    for i, n in enumerate(numbers):
        turns[i+1] = n
        prev_turns[n] = [i+1]

    for turn in range(len(numbers)+1, target+1):
        prev_number = turns[turn-1]

        # Determine the number based on how many times it's been mentioned
        if len(prev_turns[prev_number]) == 1:
            number = 0
        else:
            number = prev_turns[prev_number][1] - prev_turns[prev_number][0]

        # Update data structures
        turns[turn] = number
        prev_turns.setdefault(number, []).append(turn)
        # We only keep two values around, as we could otherwise
        # end up with fairly large lists
        if len(prev_turns[number]) == 3:
            prev_turns[number].pop(0)

    return turns[target]


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/15.in", sep=",")
    numbers = util.read_ints("input/15.in", sep=",")

    print("TASK 1")
    util.call_and_print(memory_game, sample, 2020)
    util.call_and_print(memory_game, [1,3,2], 2020)
    util.call_and_print(memory_game, [2,1,3], 2020)
    util.call_and_print(memory_game, [1,2,3], 2020)
    util.call_and_print(memory_game, [2,3,1], 2020)
    util.call_and_print(memory_game, [3,2,1], 2020)
    util.call_and_print(memory_game, [3,1,2], 2020)
    util.call_and_print(memory_game, numbers, 2020)

    print("\nTASK 2")
    util.call_and_print(memory_game, sample, 30000000)
    util.call_and_print(memory_game, [1,3,2], 30000000)
    util.call_and_print(memory_game, [2,1,3], 30000000)
    util.call_and_print(memory_game, [1,2,3], 30000000)
    util.call_and_print(memory_game, [2,3,1], 30000000)
    util.call_and_print(memory_game, [3,2,1], 30000000)
    util.call_and_print(memory_game, [3,1,2], 30000000)
    util.call_and_print(memory_game, numbers, 30000000)

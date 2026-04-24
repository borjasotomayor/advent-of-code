"""
Day 11
https://adventofcode.com/2024/day/11

A fun problem to solve where the first part is pretty
straightforward, and the trick is figuring out how
to count the stones without generating every stone
individually.
"""

import util
from collections import Counter

from util import log

def blink(stones: list[int]) -> list[int]:
    """
    Generate all stones after a blink
    """
    new_stones = []

    for stone in stones:
        if stone == 0:
            new_stones.append(1)
            continue

        ss = str(stone)
        if len(ss) % 2 == 0:
            new_stones.append(int(ss[:len(ss)//2]))    
            new_stones.append(int(ss[len(ss)//2:]))
        else:
            new_stones.append(stone*2024)

    return new_stones

def count_stones(stones: list[int], nblinks: int) -> int:
    """
    Part 1: Count number of stones after some number of blinks.

    Generates all the individual stones, so only works for
    a small number of blinks.
    """
    for _ in range(nblinks):
        stones = blink(stones)
        
    return len(stones)


def blink_opt(counts: Counter[int]) -> Counter[int]:
    """
    Optimized blinking function: instead of generating all the
    individual stones, we just keep track of the counts of each
    stone.
    """
    # New dictionary. We set the value for 1 given the likelyhood
    # we'll be adding to it
    new_counts: Counter[int] = Counter()
    for stone, n in counts.items():
        if stone == 0:
            new_counts[1] += n
            continue

        ss = str(stone)
        if len(ss) % 2 == 0:
            s1 = int(ss[:len(ss)//2])
            s2 = int(ss[len(ss)//2:])
            new_counts[s1] += n
            new_counts[s2] += n
        else:
            new_counts[stone*2024] += n

    return new_counts

def count_stones_opt(stones: list[int], nblinks: int) -> int:
    """
    Part 2: Count the number of stones without generating every
    individual stone.
    """
    counts = Counter(stones)
    for _ in range(nblinks):
        counts = blink_opt(counts)
    
    return sum(counts.values())


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = [0, 1, 10, 99, 999]
    sample2 = [125, 17]
    input = [41078, 18, 7, 0, 4785508, 535256, 8154, 447]

    print("TASK 1")
    util.call_and_print(count_stones, sample1, 1)
    util.call_and_print(count_stones, sample2, 6)
    util.call_and_print(count_stones, sample2, 25)
    util.call_and_print(count_stones, input, 25)

    print("\nTASK 2")
    util.call_and_print(count_stones_opt, sample1, 1)
    util.call_and_print(count_stones_opt, sample2, 6)
    util.call_and_print(count_stones_opt, sample2, 25)
    util.call_and_print(count_stones_opt, input, 25)
    util.call_and_print(count_stones_opt, input, 75)

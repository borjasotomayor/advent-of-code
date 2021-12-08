"""
Day 8
https://adventofcode.com/2021/day/8

1st star: 00:06:23
2nd star: 00:54:36

This was one of those problems where I took the approach of progressively
narrowing down the list of possible mappings, without really knowing
whether it was guaranteed to arrive at a unique mapping (but praying that
it did and, much to my relief, it did!)

The code I originally wrote was a hot mess full or rote code with tons of 
repeated code everywhere. The version below involved a lot of cleaning up, 
and figuring out what data structures I needed to be able to do certain 
operations more cleanly in a loop.

All that said, kinda wish I had gone with my first instinct to just brute force
this, which feels like it would be doable, and might even result in a
more compact and readable solution.
"""

import util
import math
import sys
import re

from util import log


# All the segments
ALL_SEGMENTS = set(["a", "b", "c", "d", "e", "f", "g"])

# Maps segment configurations to digits
DIGITS = {frozenset(["a", "b", "c", "e", "f", "g"]): "0",
          frozenset(["c", "f"]): "1",
          frozenset(["a", "c", "d", "e", "g"]): "2",
          frozenset(["a", "c", "d", "f", "g"]): "3",
          frozenset(["b", "c", "d", "f"]): "4",
          frozenset(["a", "b", "d", "f", "g"]): "5",
          frozenset(["a", "b", "d", "e", "f", "g"]): "6",
          frozenset(["a", "c", "f"]): "7",
          frozenset(["a", "b", "c", "d", "e", "f", "g"]): "8",
          frozenset(["a", "b", "c", "d", "f", "g"]): "9"
}

# Maps digits to segment configurations
SEGMENTS = {v: k for k, v in DIGITS.items()}

# The segments that one or more digits (with N segments) have
# in common
COMMON = {2: SEGMENTS["1"],
          3: SEGMENTS["7"],
          4: SEGMENTS["4"],
          5: SEGMENTS["2"] & SEGMENTS["3"] & SEGMENTS["5"],
          6: SEGMENTS["0"] & SEGMENTS["6"] & SEGMENTS["9"]}


def decode_single_pattern(signals, outputs):
    """
    Decodes a single pattern (one line of input in the problem)
    """

    # This dictionary maps a segment in a 7-segment display
    # to a "signal wire". 
    mapping = {s: set(ALL_SEGMENTS) for s in ALL_SEGMENTS}

    # We use this to keep track of what segments appear in
    # all digits with a given number of segments
    common = {x: set(ALL_SEGMENTS) for x in (2,3,4,5,6,7)}

    # First sieve: For the digits with a unique number
    # of segments, their "off" segments can't be mapped
    # to any of the signal wires Additionally, we use this
    # first pass to build the 'common' dictionary
    for signal in signals:
        signal = set(signal)
        n = len(signal)

        if n in (2, 3, 4):
            segments = COMMON[n]
            for segment in ALL_SEGMENTS - segments:
                mapping[segment].difference_update(signal)

        common[n].intersection_update(signal)

    # Second sieve: Given the segments that appear across
    # all digits with N segments, each segment must be mapped
    # to one of the common segments we identified in the signal
    # wires.
    for n, segments in COMMON.items():
        for segment in segments:
            mapping[segment].intersection_update(common[n])

    # At this point, we should have some segments mapped to
    # a single segment, which means we've found the mapping
    # for that segment. So, we remove them from other mappings.
    singletons = [s for s in mapping.values() if len(s)==1]
    for s in mapping.values():
        if len(s) > 1:
            for singl in singletons:
                s.difference_update(singl)

    # Invert the dictionary
    map = {}
    for k,v in mapping.items():
        # Oh, god, please don't fail
        assert len(v) == 1
        map[v.pop()] = k

    # Find the digit corresponding to each output
    num = ""
    for o in outputs:
        actual = frozenset(map[c] for c in o)
        d = DIGITS[actual]
        num += d

    return int(num)


def decode(patterns):
    """
    Decode all the patterns and add them up for Task 2
    """
    sum = 0
    for signals, outputs in patterns:
        sum += decode_single_pattern(signals, outputs)

    return sum


def read_input(input):
    """
    Read in the input
    """
    patterns = []
    for line in input:
        signals, outputs = line.split(" | ")

        signals = signals.split()
        outputs = outputs.split()

        patterns.append((signals, outputs))

    return patterns


def task1(input):
    """
    Task 1: just count the outputs of a certain length
    """
    patterns = read_input(input)

    n = 0
    for _, outputs in patterns:
        for o in outputs:
            if len(o) in (2,3,4,7):
                n += 1
    return n


def task2(input):
    """
    All the heavy lifting happens in decode()
    """
    return decode(read_input(input))


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/08-1.in", sep="\n")
    sample2 = util.read_strs("input/sample/08-2.in", sep="\n")
    input = util.read_strs("input/08.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample1)
    util.call_and_print(task1, sample2)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample1)
    util.call_and_print(task2, sample2)
    util.call_and_print(task2, input)

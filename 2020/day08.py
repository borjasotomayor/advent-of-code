"""
Day 8
https://adventofcode.com/2020/day/8

1st star: 00:05:28
2nd star: 00:13:29

woooooo, my favorite part of Advent of Code: simulating computer architectures!

My original solution was a very rote implementation of the instruction
processing, but I then wrote a proper Console class in console.py
"""

import util
import math
import sys
import re

from util import log
from console import Console


def task1(console):
    # Just need to run the console and return the accumulator
    console.run()

    return console.acc


def task2(console):
    # We iterate through the instructions and, if we
    # encounter a nop or jmp, we switch the instruction
    # and try running the program
    for i, (op, param) in enumerate(console.prog):
        if op in ("nop", "jmp"):
            # Reset console back to original state and program
            # (undoing any previous changes to program)
            console.reset()

            # Replace instruction
            if op == "nop":
                console.prog[i] = ("jmp", param)
            elif op == "jmp":
                console.prog[i] = ("nop", param)

            # Run console and check for normal termination
            console.run()
            if console.normal_termination():
                return console.acc                
    

if __name__ == "__main__":
    util.set_debug(False)

    sample = Console.from_file("input/sample/08.in")
    real = Console.from_file("input/08.in")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, real)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, real)

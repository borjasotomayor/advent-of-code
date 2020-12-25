"""
Day 25
https://adventofcode.com/2020/day/25

1st star: 00:14:43
2nd star: 00:14:51

WOOOOOO! Advent of Code is done and I can go back to a regular
sleeping schedule!
"""

import util
import math
import sys
import re

from util import log


def find_loop_size(pk):
    """
    Good ol' brute force does the trick: try every possible 
    loop size (except keep the value from the previous iteration,
    instead of computing it from scratch)
    """
    value = 1
    subject_number = 7
    for loop_size in range(1, pk):

        value *= subject_number
        value %= 20201227

        if value == pk:
            return loop_size


def transform(subject_number, loop_size):
    """
    Transform the subject number
    """
    value = 1

    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227

    return value


def crack_keys(card_pk, door_pk):
    """
    Extract the encryption key from the public keys
    """    
    card_loop = find_loop_size(card_pk)
    door_loop = find_loop_size(door_pk)

    card_key = transform(door_pk, card_loop)
    door_key = transform(card_pk, door_loop)

    assert card_key == door_key
   
    return card_key


if __name__ == "__main__":
    util.set_debug(False)

    print("TASK 1")
    util.call_and_print(crack_keys, 5764801, 17807724)
    util.call_and_print(crack_keys, 14788856, 19316454)
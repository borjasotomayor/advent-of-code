"""
Day 3
https://adventofcode.com/2025/day/3

The first part of the problem was relatively straightforward,
but the second part required a bit more thought. The main 
insight was that, if a bank has N digits, and the joltage
has M digits (M < N), then the largest joltage must
start with the largest digit in the first N-M+1 digits

In the sample data, this means we start by looking
at the first 4 digits of the 15 digit bank, since 
we're looking for a joltage with 12 digits.

Suppose there was a 9 in the first 4 digits, and a 9
in the latter 11 digits. We can't choose the 9 in the
latter 11 digits because then we wouldn't have enough
digits to form a 12-digit joltage.

Once we've found the largest digit in the first 4 digits,
we basically repeat the process for the "sub-bank" starting
in the digit after the largest digit (and so on, until
we've found all 12 digits)

My first solution was iterative, but I then realized this
lends itself to a more elegant recursive solution.
"""

import util
import math
import sys
import re

from util import log


def find_max_digit(bank: str, start: int, end: int) -> tuple[str, int]:
    """
    Find the largest digit (and its index) in
    a substring of the bank (from index 'start'
    up to, but not including 'end')

    This is basically a slightly more efficient way
    of calling .max followed by .index
    """
    max_digit = ""
    max_digit_idx = -1
    for i in range(start, end):
        if bank[i] > max_digit:
            max_digit = bank[i]
            max_digit_idx = i

    return max_digit, max_digit_idx
                

def compute_joltage(bank: str, joltage_length:int) -> int:
    """
    Compute the largest joltage for a given bank

    Iterative solution
    """
    len_bank = len(bank)
    joltage = []

    idx = 0
    # This loop iterates from joltage_length
    # down to 1 (representing the 'remaining digits'
    # we still have to find)
    for dr in range(joltage_length, 0, -1):
        # Find maximum digit and index
        max_digit, max_digit_idx = find_max_digit(bank, idx, len_bank - dr + 1)

        # In the next iteration,
        idx = max_digit_idx + 1
        joltage.append(max_digit)

    return int("".join(joltage))


def compute_joltage_r(bank: str, joltage_length:int) -> str:
    """
    Compute the largest joltage for a given bank

    Recursive solution
    """

    # Base case: if we reach a joltage length of zero, we
    # return an empty string
    if joltage_length == 0:
        return ""
    
    # Find the maximum digit (and index) in the first
    # len(bank) - joltage_length + 1 digits
    max_digit, max_digit_idx = find_max_digit(bank, 0, len(bank) - joltage_length + 1)

    # Recursive case: repeat the search in the substring
    # starting after the maximum digit we just found
    # (looking for a joltage with one less digit)
    rem_bank = bank[max_digit_idx+1:]
    rem_joltage = compute_joltage_r(rem_bank, joltage_length-1)

    return max_digit + rem_joltage


def compute_total_joltages(banks: list[str], joltage_length: int):
    """
    Compute the total joltages (using the iterative implementation)
    """
    total = 0
    for bank in banks:
        total += compute_joltage(bank, joltage_length)
        
    return total


def compute_total_joltages_r(banks: list[str], joltage_length: int):
    """
    Compute the total joltages (using the iterative implementation)
    """
    total = 0
    for bank in banks:
        total += int(compute_joltage_r(bank, joltage_length))
        
    return total


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/03.in", sep="\n")
    input = util.read_strs("input/03.in", sep="\n")

    print("TASK 1")
    util.call_and_print(compute_total_joltages, sample, 2)
    util.call_and_print(compute_total_joltages_r, sample, 2)
    util.call_and_print(compute_total_joltages, input, 2)
    util.call_and_print(compute_total_joltages_r, input, 2)

    print("\nTASK 2")
    util.call_and_print(compute_total_joltages, sample, 12)
    util.call_and_print(compute_total_joltages_r, sample, 12)
    util.call_and_print(compute_total_joltages, input, 12)
    util.call_and_print(compute_total_joltages_r, input, 12)

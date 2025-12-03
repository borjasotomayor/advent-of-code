"""
Day 2
https://adventofcode.com/2025/day/2

Followed a brute force approach which, to my surprise,
worked just fine.
"""

import util
import math
import sys
import re

from util import log


def is_invalid(product_id: int, super_invalid: bool):
    """
    Checks if a product ID is invalid. If super_invalid
    is True, it applies the Task 2 definition of an invalid ID.
    """
    str_id = str(product_id)
    len_id = len(str_id)

    # Given a number with len_id digits,
    # we check every possible divisor of len_id
    # (greater than one). If the number can be divided
    # into substrings of equal length (len_id // div),
    # we check if the first such substring, repeated 
    # div times, is equal to the original id.
    for div in range(2, len_id+1):
        if len_id % div == 0:
            len_substr = len_id // div
            
            substr = str_id[0:len_substr]
            if substr * div == str_id: 
                return True

        if not super_invalid:
            # If we're applying the Task 1 definition
            # of invalid, we can bail after checking
            # div=2
            break

    return False


def check_product_ids(product_ids: list[tuple[int, int]], super_invalid):
    """
    Checks ranges of product IDs.

    If super_invalid is True, we apply the Task 2 
    definition of an invalid ID.
    """
    sum_ids = 0
    for lb, ub in product_ids:
        for id in range(lb, ub+1):
            if is_invalid(id, super_invalid):
                log(f"Invalid ID found: {id}") 
                sum_ids += id

    return sum_ids


if __name__ == "__main__":
    util.set_debug(False)

    sample_lsts = util.read_ints("input/sample/02.in", sep=",", sep2="-")
    input_lsts = util.read_ints("input/02.in", sep=",", sep2="-")

    # Convert the ranges into tuples
    sample = [tuple(lst) for lst in sample_lsts]
    input = [tuple(lst) for lst in input_lsts]

    print("TASK 1")
    util.call_and_print(check_product_ids, sample, False)
    util.call_and_print(check_product_ids, input, False)

    print("\nTASK 2")
    util.call_and_print(check_product_ids, sample, True)
    util.call_and_print(check_product_ids, input, True)

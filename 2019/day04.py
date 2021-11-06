"""
Day 4
https://adventofcode.com/2019/day/4

1st star: 00:06:27
2nd star: 00:11:19

This is a much more polished version of the code I originally wrote,
which was slightly more convoluted by keeping track of a list of
"streak lengths", instead of the simpler approach below (using
two boolean variables to check whether we've encountered a
streak of consecutive digits meeting the stated requirements)
"""

import util


def is_valid(password, require_standalone_pair):
    """
    Checks whether a password is valid.

    If require_standalone_pair is True, then any pair of
    adjacent digits must be by themselves (not part of a longer
    sequence of matching digits)
    """

    # Convert the password to a list of integer d
    s = [int(c) for c in str(password)]

    # We artificially add a None at the end of the list,
    # to account for the corner case of a sequence of
    # adjacent digits appearing right at the end of
    # the password (this ensures that all our variables
    # are properly updated by the loop, instead of
    # having code after the loop that repeats the
    # checks to see if the last digit creates a valid
    # sequence)
    s.append(None)
    
    # When we encounter a streak of consecutive digits,
    # we use this variable to keep track of its length.
    streak_len = 0

    # We keep track of whether we've found a streak of
    # any length (greater than 1), and a streak of exactly
    # two digits
    has_streak = False
    has_2digit_streak = False

    # This keeps track of the previous digit as we iterate
    # over the digits
    prev = None

    for cur in s:
        # Digits have to be non-decreasing. If they're not,
        # the password isn't valid
        if prev is not None and cur is not None and cur < prev:
            return False

        # If the current digit matches the previous one,
        # we are in a streak of consecutive digits.
        if cur == prev:
            # Increment the length of the streak
            streak_len += 1

            if streak_len >= 2:
                # We've found a streak!
                has_streak = True
                           
        # If the current digit doesn't match the previous character,
        # then a streak may be ending
        if cur != prev:
            # If the streak that is ending has exactly two digits,
            # we update has_2digit_streak
            if streak_len == 2:
                has_2digit_streak = True

            # The current streak has a length of one
            streak_len = 1

        prev = cur

    # The loop was already checking whether the digits were non-decreasing
    # so the only thing left that could make the password invalid is the
    # lack of a valid sequence of adjacent digits.
    if require_standalone_pair and not has_2digit_streak:
        return False
    else:
        return has_streak


def count_valid_password(lb, ub, require_standalone_pair):
    """
    Count the number of valid passwords in a given range
    """

    n = 0
    for password in range(lb, ub+1):
        if is_valid(password, require_standalone_pair):
            n += 1

    return n


if __name__ == "__main__":
    min_value = 264360
    max_value = 746325

    print("TASK 1")
    util.call_and_print(is_valid, 111111, False)
    util.call_and_print(is_valid, 223450, False)
    util.call_and_print(is_valid, 123789, False)
    util.call_and_print(count_valid_password, min_value, max_value, False)

    print("\nTASK 2")
    util.call_and_print(is_valid, 112233, True)
    util.call_and_print(is_valid, 123444, True)
    util.call_and_print(is_valid, 111122, True)
    util.call_and_print(count_valid_password, min_value, max_value, True)

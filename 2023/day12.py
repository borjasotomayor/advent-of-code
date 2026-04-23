"""
Day 12
https://adventofcode.com/2023/day/12

One of those problems where, as you're writing Part 1,
you dread how your solution will be woefully inefficient
for Part 2. Sure enough, had to use a very different
(memoized) approach for Part 2 (where I may have gone
a bit overboard with the optimizing/pruning)
"""
import functools
import util

from util import log

def compute_groups(springs: list[str]) -> list[int]:
    """
    Compute the groups up to the first "?" in the row
    """
    cur_group = 0
    groups = []
    for c in springs:
        if c == "#":
            cur_group += 1
        elif c == ".":
            if cur_group > 0:
                groups.append(cur_group)
            cur_group = 0
        elif c == "?":
            if cur_group > 0:
                groups.append(cur_group)
            return groups
    if cur_group > 0:
        groups.append(cur_group)

    return groups

def count_arrangements(springs: list[str], target_groups: list[int]) -> int:
    """
    Recursively count the number of arrangements.
    Slightly brute force-ish, as all we're doing is replacing
    each ? with "." or "#" and then checking if the number
    of groups matches the expected number of groups.
    """

    # We start by finding the first unknown value
    # in the row
    try:
        next_unknown = springs.index("?")
    except ValueError:
        # However, if there are no unknown values,
        # all we have to do is compute the groups
        # for the springs, and check if they match
        # the expected groups.
        groups = compute_groups(springs)
        if groups == target_groups:
            return 1
        else:
            return 0

    # Compute the groups up to the first "?"
    groups = compute_groups(springs)
    # Quick check: if any of the groups is greater
    # that the target groups, this isn't a valid arrangement
    for g, tg in zip(groups, target_groups):
        if g > tg:
            return 0

    # Count the number of arrangements based on changing each "?"
    # to a "." or a "?"
    arrangements = 0
    springs[next_unknown] = "."
    arrangements += count_arrangements(springs, target_groups)
    springs[next_unknown] = "#"
    arrangements += count_arrangements(springs, target_groups)
    springs[next_unknown] = "?"

    return arrangements


def count_all_arrangements(input: list[tuple[str, str]]) -> int:
    """
    Part 1: Count all possible arrangements

    The heavy lifting is done in count_arrangements, which counts
    the arrangement for a specific row
    """
    sum = 0
    for springs_str, groups_str in input:
        springs = list(springs_str)
        groups = [int(x) for x in groups_str.split(",")]
        arr = count_arrangements(springs, groups)
        sum += arr
    return sum

@functools.cache
def count_arrangements_optimized(springs: str, groups: tuple[int]) -> int:
    """
    An optimized version of count_arrangements that uses memoization
    to avoid recomputing numbers of arrangements. Can be used as a
    drop-in replacement for count_arrangements
    """
    # Base case 1: If there are no groups of broken springs,
    # then the springs string cannot contain any "#" characters
    # (otherwise, groups would contain at least one value)
    if len(groups) == 0:
        if "#" in springs:
            return 0
        else:
            return 1

    # Base case 2: If the number of broken springs (with
    # at least one empty space between them) is greater than
    # the length of the row, then this is an invalid arrangement.
    if sum(groups) + len(groups) - 1 > len(springs):
        return 0

    # If the first character is a ".", it has no bearing
    # on the count. Skip ahead to the next non-"." character
    # (since Base Case 1 wasn't triggered, there must be at
    # least one such character)
    if springs[0] == '.':
        indices = []
        if next_broken := (springs.find("#") != -1):
            indices.append(next_broken)
        if next_unknown := (springs.find("?") != -1):
            indices.append(next_unknown)

        # Base case 3: If there are no "#" or "?" this can't
        # be a valid arrangement, since we know len(groups)
        # is at least 1
        if len(indices) == 0:
            return 0

        next_index = min(indices)

        return count_arrangements_optimized(springs[next_index:], groups)

    # If the first character is a "#", we need to check that the
    # first N characters contain non-"." characters (where N is
    # the size of the first group in the list of groups) AND
    # that those characters are not followed by a "#" (considering
    # the special case that the group could hit right up against
    # the end of the string)
    elif springs[0] == '#':
        expected_group_size = groups[0]

        # Base case 4: There are not enough characters for
        # the expected group size
        if len(springs) < expected_group_size:
            return 0

        candidate_block = springs[:expected_group_size]

        if "." in candidate_block:
            return 0

        if len(springs) > expected_group_size and springs[expected_group_size] == "#":
            return 0

        return count_arrangements_optimized(springs[expected_group_size+1:], groups[1:])

    else: # springs[0] == "?":
        count_if_operational = count_arrangements_optimized(springs[1:], groups)
        count_if_broken = count_arrangements_optimized("#" + springs[1:], groups)

        return count_if_operational + count_if_broken

def count_all_arrangements_optimized(input: list[tuple[str, str]], factor: int) -> int:
    """
    Part 2: Count all possible arrangements (optimized)

    The heavy lifting is done in count_arrangements_optimized, which counts
    the arrangement for a specific row
    """    
    sum = 0
    for springs_str, groups_str in input:
        springs = "?".join([springs_str] * factor)
        groups = tuple(int(x) for x in groups_str.split(",")) * factor
        arr = count_arrangements_optimized(springs, groups)
        sum += arr
    return sum



if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/12.in", sep="\n", sep2=" ")
    input = util.read_strs("input/12.in", sep="\n", sep2=" ")

    print("TASK 1")
    util.call_and_print(count_all_arrangements, sample)
    util.call_and_print(count_all_arrangements, input)

    print("TASK 1 (optimized)")
    util.call_and_print(count_all_arrangements_optimized, sample, 1)
    util.call_and_print(count_all_arrangements_optimized, input, 1)

    print("\nTASK 2")
    util.call_and_print(count_all_arrangements_optimized, sample, 5)
    util.call_and_print(count_all_arrangements_optimized, input, 5)

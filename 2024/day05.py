"""
Day 5
https://adventofcode.com/2024/day/5

This was a fun problem to figure out, although I suspect there
are fancier ways of solving it.

For me, the key insight was to iterate over the list of integers,
and keeping a set of pages that have already been checked as valid.
Then, for each page, we check whether any checked pages should appear
*after* the current page (which we can efficiently do with the
set of checked pages: just check if the intersection of the "must
appear after" pages and the checked pages is empty). This requires 
building a "reverse dependency" dictionary, mapping pages to the 
pages that should appear after it (instead of mapping them to 
"prerequisite" pages)

For Part 2, I fixed the updates simply by identifying the offending page,
and moving it back until the update was correct. This is where I wonder
if there is a fancier way of doing this, maybe relying on the graph structure
of the page dependencies.
"""

import util
import math
import sys
import re

from util import log

def build_deps_dict(deps: list[str]) -> dict[int, set[int]]:
    """
    Builds a "reverse dependency" dictionary. For each page,
    we have a set of pages that should appear *after* that page
    (if both pages are present in the list of integers)
    """
    deps_dict: dict[int, set[int]] = {}

    for dep in deps:
        req, page = (int(x) for x in dep.split("|"))

        deps_dict.setdefault(req, set()).add(page)

    return deps_dict


def is_correct_update(pages: list[int], deps_dict: dict[int, set[int]]) -> tuple[bool, int | None]:
    """
    Checks if an update is correct. If not, it returns False and
    the index of the offending page (which will come in handy
    for Part 2)
    """
    printed: set[int] = set()
    for i, page in enumerate(pages):
        # Given a page P, if any of the pages that
        # must appear after it have already been
        # printed, then this is an incorrect update.
        must_appear_after = deps_dict.get(page, set())
        if not must_appear_after.isdisjoint(printed):
            return False, i
        printed.add(page)

    return True, None


def add_correct(deps: list[str], updates: list[str]) -> int:
    """
    Part 1: Add the middle pages of the correct updates
    """
    deps_dict = build_deps_dict(deps)

    total = 0
    for update in updates:
        pages = [int(x) for x in update.split(",")]

        correct, _ = is_correct_update(pages, deps_dict)
        if correct:
            total += pages[len(pages) // 2]
    
    return total


def fix_update(pages: list[int], deps_dict: dict[int, set[int]]) -> list[int]:
    """
    Given an incorrect update, fix it by moving back the offending page(s)
    until we have a correct update.
    """
    update = pages[:]
    correct, idx = is_correct_update(update, deps_dict)
    assert not correct

    while not correct:
        assert idx is not None
        # Swap the offending page with the previous page
        update[idx-1], update[idx] = update[idx], update[idx-1]
        correct, idx = is_correct_update(update, deps_dict)

    return update
    

def add_fixed(deps: list[str], updates: list[str]) -> int:
    """
    Part 2: Add the middle pages of the (fixed) incorrect updates
    """

    deps_dict = build_deps_dict(deps)

    total = 0
    incorrect_updates = []
    for update in updates:
        pages = [int(x) for x in update.split(",")]

        correct, _ = is_correct_update(pages, deps_dict)

        if not correct:
            incorrect_updates.append(pages)

    for inc_update in incorrect_updates:
        fixed_update = fix_update(inc_update, deps_dict)
        total += fixed_update[len(fixed_update) // 2]
    
    return total


if __name__ == "__main__":
    util.set_debug(False)

    deps_sample, updates_sample = util.read_strs("input/sample/05.in", sep="\n\n", sep2="\n")
    deps, updates = util.read_strs("input/05.in", sep="\n\n", sep2="\n")

    print("TASK 1")
    util.call_and_print(add_correct, deps_sample, updates_sample)
    util.call_and_print(add_correct, deps, updates)

    print("\nTASK 2")
    util.call_and_print(add_fixed, deps_sample, updates_sample)
    util.call_and_print(add_fixed, deps, updates)

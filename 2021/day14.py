"""
Day 14
https://adventofcode.com/2021/day/14

1st star: 00:11:34	
2nd star: 00:42:04

Ok, not going to lie: for Part 2 I basically took the approach of
"let's throw stuff at the wall and see what sticks". I knew I
couldn't generate all the strings, and instead needed to count up
*something* and figured I'd start with the pairs to see if that would
work, even though I knew I was over-counting and wasn't compensating
for it in any way. Lo and behold, when I saw the result, I realized
I was specifically *double*-counting, which was easy to compensate for
at the very end.
"""

import util
import operator

from util import log


def step(pairs, rules):
    """
    Do a step (see count_polymer for more details)
    """
    new_pairs = {}
    for pair, v in pairs.items():
        p1 = pair[0] + rules[pair]
        p2 = rules[pair] + pair[1]
        new_pairs[p1] = new_pairs.get(p1, 0) + v
        new_pairs[p2] = new_pairs.get(p2, 0) + v
    return new_pairs


def count_polymer(template, rules, steps):
    """
    Counts the number of elements in a polymer starting from the
    given template, and applying the rules for the given number of steps.

    Instead of producing the polymers themselves, we use a dictionary
    to count up how many time each pair appears in the polymer. In each
    step, each pair spawns two new pairs. For example, if we know we
    have 10 CH pairs, this then produces 10 CB pairs and 10 BH pairs
    (applying the CH -> B rule). This double-counts each letter, but
    we compensate for that later on.

    Returns the difference between the most common and least common element.
    """

    # Compute the initial pairs
    pairs = {}
    for i in range(len(template)-1):
        pair = template[i:i+2]
        pairs[pair] = pairs.get(pair, 0) + 1

    # Do the steps
    cur = pairs
    for i in range(steps):
        cur = step(cur, rules)

    # Count the elements
    elements = {}
    for (e1,e2), v in cur.items():
        elements[e1] = elements.get(e1, 0) + v
        elements[e2] = elements.get(e2, 0) + v

    # When generating the pairs, we double-counted every
    # element *except* the first and last one. Before
    # we divide everything by two, we need to increment
    # those elements by one (as if we had double-counted them)
    elements[template[0]] += 1
    elements[template[-1]] += 1

    for e, n in elements.items():
        elements[e] = n // 2

    # We get the most common and least common by sorting the
    # element counts
    sorted_elems = sorted(elements.items(), key = operator.itemgetter(1))
    
    most_common = sorted_elems[-1][1]
    least_common = sorted_elems[0][1]

    return most_common - least_common


def read_input(input):
    """
    Reads the input and returns a string with the template,
    and a dictionary with the rules.
    """
    template, rules_lines = input

    rules = {}
    for rule in rules_lines.split("\n"):
        rule_from, rule_to = rule.split(" -> ")
        rules[rule_from] = rule_to

    return template, rules


def task1(input):
    """
    Task 1: Do 10 steps
    """
    template, rules = read_input(input)
    return count_polymer(template, rules, 10)


def task2(input):
    """
    Task 2: Do 40 steps
    """
    template, rules = read_input(input)
    return count_polymer(template, rules, 40)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/14.in", sep="\n\n")
    input = util.read_strs("input/14.in", sep="\n\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)

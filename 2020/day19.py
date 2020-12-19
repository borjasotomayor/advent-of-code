"""
Day 19
https://adventofcode.com/2020/day/19

1st star: 00:30:04
2nd star: 00:34:22

OH GOD I FEEL LIKE SUCH A CHEAT. After struggling to recall how to write
a parsing algorithm, and toying with the idea of simply generating
all possible strings starting from the provided grammar, I just took the
grammar, converted it to a format that would work with Lark
(https://github.com/lark-parser/lark) and let Lark handle all the parsing.

To be fair, while this is not good problem solving, it's good software
engineering: if there's a library that already does exactly what you
need, just use that library.
"""

import util
import math
import sys
import re

from util import log
import lark


def aoc2lark(rules_txt):
    """
    Converts an AoC grammar to a Lark grammar
    """

    grammar = ""
    for line in rules_txt:
        rule_num, subrules_txt = line.split(": ")
        rule_num = int(rule_num)
        if rule_num == 0:
            rule_name = "start"
        else:
            rule_name = f"rule{rule_num}"

        if "|" in subrules_txt:
            subrule1, subrule2 = subrules_txt.split(" | ")

            subrule1 = " ".join("rule" + x for x in subrule1.split())
            subrule2 = " ".join("rule" + x for x in subrule2.split())

            subrules = f"{subrule1} | {subrule2}"

        elif subrules_txt[0] == '"':
            subrules = subrules_txt
        else:
            subrules = " ".join("rule" + x for x in subrules_txt.split())

        grammar += f"{rule_name}: {subrules}\n"

    return grammar


def count_correct(input, replace=False):
    """
    Count the number of correct strings, given the provided grammar.
    """
    rules_txt = input[0].split("\n")

    if replace:
        new_rules_txt = []
        for line in rules_txt:
            if line == "8: 42":
                line = "8: 42 | 42 8"
            elif line == "11: 42 31":
                line = "11: 42 31 | 42 11 31"
            new_rules_txt.append(line)
        rules_txt = new_rules_txt

    grammar = aoc2lark(rules_txt)

    parser = lark.Lark(grammar)

    messages = input[1].split("\n")
    correct = 0
    for message in messages:
        try:
            parser.parse(message.strip())
            correct += 1
        except lark.exceptions.LarkError:
            pass

    return correct


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/19-1.in", sep="\n\n")
    sample2 = util.read_strs("input/sample/19-2.in", sep="\n\n")
    input = util.read_strs("input/19.in", sep="\n\n")

    print("TASK 1")
    util.call_and_print(count_correct, sample1)
    util.call_and_print(count_correct, input)

    print("\nTASK 2")
    util.call_and_print(count_correct, sample2)
    util.call_and_print(count_correct, sample2, True)
    util.call_and_print(count_correct, input, True)

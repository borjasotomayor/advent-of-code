"""
Day 11
https://adventofcode.com/2022/day/11

1st star: 00:22:51
2nd star: 00:57:19

Well, I think I did a pretty decent job in Part 1 (once I got past 
the input parsing), and then Part 2 came along... 

Not gonna lie, folks, this was one where I followed the Cave Johnson 
methodoloy of throwing science at the wall and seeing what stuck. 
I did notice that all the divisors were prime numbers, and 
suspected some sort of modular tomfoolery, so I tried various 
combinationsof dividing the numbers by the divisor before passing
them to the other monkey, keeping only the remainder, etc. until I 
tried dividing by the product of all the divisors... and that worked. 
Still not 100% sure why, but I'll take it.
"""

import util
import math
import sys
import re
import parse

from util import log


class Monkey:
    """
    Simple class for storing information about each monkey
    """

    def __init__(self, id, starting, op, op2, divisible, if_true, if_false):
        self.id = id
        self.items = starting
        self.op = op
        self.op2 = op2
        self.divisible = divisible
        self.if_true = if_true
        self.if_false = if_false
        self.inspected = 0

    @classmethod
    def from_str(cls, monkey_str):
        """
        Parse the input using the parse library
        """
        id = parse.parse("Monkey {:d}:", monkey_str[0])[0]
        starting = parse.parse("  Starting items: {}", monkey_str[1])[0]
        op, op2  = parse.parse("  Operation: new = old {} {}", monkey_str[2])
        divisible = parse.parse("  Test: divisible by {:d}", monkey_str[3])[0]
        if_true = parse.parse("    If true: throw to monkey {:d}", monkey_str[4])[0]
        if_false = parse.parse("    If false: throw to monkey {:d}", monkey_str[5])[0]

        starting = [int(x) for x in starting.split(", ")]
        
        return cls(id, starting, op, op2, divisible, if_true, if_false)

    def __str__(self):
        return f"{self.id}: {self.items}"
             

def monkey_business(monkeys, rounds, ridiculous):
    """
    Runs several rounds of monkey business.
    If ridiculous is True, our worry levels are ridiculous
    and we need to use fancy modular arithmetic to
    bring them down (Part 2)
    """

    # Secret sauce: product of all the divisors
    all_mods = math.prod(m.divisible for m in monkeys)

    for _ in range(rounds):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                item = monkey.items.pop(0)

                monkey.inspected += 1

                op2 = item if monkey.op2 == "old" else monkey.op2

                # Why write an arithmetic parser when you can just eval()?
                new_item = eval(f"{item} {monkey.op} {op2}")

                if ridiculous:
                    new_item %= all_mods
                else:
                    new_item //= 3

                # Pass the updated item to the appropriate monkey
                if new_item % monkey.divisible == 0:
                    monkeys[monkey.if_true].items.append(new_item)
                else:
                    monkeys[monkey.if_false].items.append(new_item)


    inspected = sorted([m.inspected for m in monkeys])

    return inspected[-1] * inspected[-2]
    

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/11.in", sep="\n\n", sep2="\n")
    input = util.read_strs("input/11.in", sep="\n\n", sep2="\n")

    sample_monkeys = [Monkey.from_str(s) for s in sample]
    monkeys = [Monkey.from_str(s) for s in input]

    print("TASK 1")
    util.call_and_print(monkey_business, sample_monkeys, 20, False)
    util.call_and_print(monkey_business, monkeys, 20, False)

    sample_monkeys = [Monkey.from_str(s) for s in sample]
    monkeys = [Monkey.from_str(s) for s in input]

    print("\nTASK 2")
    util.call_and_print(monkey_business, sample_monkeys, 10000, True)
    util.call_and_print(monkey_business, monkeys, 10000, True)

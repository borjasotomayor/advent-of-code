"""
Day 4
https://adventofcode.com/2023/day/4

1st star: 00:07:25
2nd star: 00:15:43

This was a fun little problem, and my intuition to implement
a ScratchCard class from the get-go paid of as far as making
the code easy to write and follow. The main change I made
when polishing up the code was to use a regex for parsing
the input, instead of a bunch of .split()s.
"""

import re
from collections.abc import Iterable

import util


class ScratchCard:
    """
    Simple class for representing a scratch card
    """

    number: int
    winning_numbers: set[int]
    your_numbers: set[int]

    def __init__(self, number: int, winning_numbers: Iterable[int], your_numbers: Iterable[int]):
        """ Constructor """
        self.number = number
        self.winning_numbers = set(winning_numbers)
        self.your_numbers = set(your_numbers)

    @property
    def num_matches(self) -> int:
        """ Get the number of matching numbers in the card"""
        return len(self.winning_numbers.intersection(self.your_numbers))

    @property
    def value(self) -> int:
        """ Get the point value of the scratchcard """
        if self.num_matches == 0:
            return 0
        else:
            return 2**(self.num_matches-1)


CARD_RE = re.compile(r"Card\s+(?P<card_num>[0-9]+): (?P<win_nums>[0-9 ]+) \| (?P<your_nums>[0-9 ]+)")


def read_input(input: list[str]) -> list[ScratchCard]:
    """
    Read the scratchcards from the input
    """
    cards = []
    for line in input:
        match = CARD_RE.match(line)
        assert match is not None
        card_num = int(match.group("card_num"))
        win_nums = [int(n) for n in match.group("win_nums").split()]
        your_nums = [int(n) for n in match.group("your_nums").split()]

        cards.append(ScratchCard(card_num, win_nums, your_nums))

    return cards


def add_points(cards: list[ScratchCard]) -> int:
    """
    Task 1: Add up the points of all the cards
    """
    return sum(card.value for card in cards)


def count_card_copies(cards: list[ScratchCard]) -> int:
    """
    Task 2: Count up the number of copies
    """

    # We will use a dictionary to keep track of
    # the number of copies of each scratchcard.
    # Initially, we have one copy of each card
    ncopies = {card.number: 1 for card in cards}

    # For each copy of each card...
    for card in cards:
        for _ in range(ncopies[card.number]):
            # We increase the number of copies for
            # the cards following the current card
            for i in range(card.num_matches):
                card_num = card.number + 1 + i
                # Make sure we don't go over the end
                # of the table
                if card_num <= len(cards):
                    ncopies[card_num] += 1

    return sum(ncopies.values())


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/04.in", sep="\n")
    input = util.read_strs("input/04.in", sep="\n")

    sample_cards = read_input(sample)
    cards = read_input(input)

    print("TASK 1")
    util.call_and_print(add_points, sample_cards)
    util.call_and_print(add_points, cards)

    print("\nTASK 2")
    util.call_and_print(count_card_copies, sample_cards)
    util.call_and_print(count_card_copies, cards)

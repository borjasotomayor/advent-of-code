"""
Day 7
https://adventofcode.com/2023/day/7

1st star: 00:19:39
2nd star: 00:45:01

This was a really fun problem to code up. I went with
an object-oriented solution, defining a Hand class that
overrides __lt__ and __eq__ so it can be sorted, which
paid off in terms of making the code simple to write.
It similarly made it easy to add support for jokers,
although I lost a bunch of time chasing down some
corner cases (but, again, the OO approach made it
easier to debug)
"""

from collections import Counter

import util

# Maps cards to numerical values
MAP = {"A": 14,
       "K": 13,
       "Q": 12,
       "T": 10}


class Hand:
    """
    Class for representing a hand of cards
    """

    hand_str: str
    bid: int
    cards: list[int]
    jokers: bool
    rank: int

    def __init__(self, hand_str: str, bid: int, jokers: bool = False):
        """ Constructor """
        self.hand_str = hand_str
        self.bid = bid
        self.cards = []
        self.jokers = jokers

        # Convert the string representation into a list of integers
        # This way, comparing hands of the same rank will just involve
        # list comparison (which is done in lexicographical order in
        # Python)
        for char in hand_str:
            if char.isdigit():
                self.cards.append(int(char))
            elif char == "J":
                self.cards.append(1 if self.jokers else 11)
            else:
                self.cards.append(MAP[char])

        # Compute the rank of the hand
        # (this is what the problem calls the "type" of the hand)
        self.rank = self._rank()

    def __str__(self):
        """ Return a string representation """
        return self.hand_str

    def __repr__(self):
        """ Return a string representation for debugging """
        return f"Hand('{self.hand_str}', {self.bid})"

    def _rank(self) -> int:
        """
        Computes the rank of the hand (what the problem refers to as
        the "type"). We return the following:

        7: Five of a kind
        6: Four of a kind
        5: Full house
        4: Three of a kind
        3: Two pair
        2: One pair
        1: High card
        """
        # Count how many cards of each kind are in the hand
        counter = Counter(self.cards)

        # If we allow jokers (and there are jokers in the hand)
        # we find the most common kind in the hand, and replace
        # the jokers with that same kind (just for the purposes
        # of counting the cards; we don't modify the hand itself)
        if self.jokers and 1 in counter:
            non_jokers = [v for k, v in counter.items() if k != 1]

            if len(non_jokers) > 0:
                # Find the most common card
                max_value = max(non_jokers)
                most_common = max([k for k, v in counter.items() if v == max_value and k!=1])

                # And replace the jokers with it
                jokers = counter[1]
                del counter[1]
                counter[most_common] += jokers

        # Finally, determine the rank of the hand


        if 5 in counter.values():
            # 5 cards of the same kind: Five of a kind
            return 7
        elif 4 in counter.values():
            # 4 cards of the same kind: Four of a kind
            return 6
        elif 3 in counter.values():
            # 3 cards of the same value...
            if 2 in counter.values():
                # ... with two other cards of the same kind: Full House
                return 5
            else:
                # ... otherwise: Three of a kind
                return 4
        elif 2 in counter.values():
            # 2 cards of the same value...
            if len(counter) == 3:
                # ... if there are three distinct kinds, then two of
                # them must be pairs: Two pair
                return 3
            else:
                # ... otherwise: One pair
                return 2
        else:
            # If none of the above applies, we just have "High card".
            return 1

    # The following methods allow us to use the sort() method
    # on lists of Hand objects

    def __lt__(self, other):
        """ Is self less than other? """
        if self.rank == other.rank:
            # If the rank is the same in both hands,
            # we can just do a lexicographical comparison
            # of the list of cards in each hand.
            return self.cards < other.cards
        else:
            return self.rank < other.rank

    def __eq__(self, other):
        """ Is self equal to other? """
        if self.rank == other.rank:
            return self.cards == other.cards
        else:
            return False


def read_input(input: list[str], jokers: bool) -> list[Hand]:
    """ Reads the input into a list of Hand objects """
    hands = []
    for line in input:
        hand_str, bid = line.split()
        hands.append(Hand(hand_str, int(bid), jokers))

    return hands


def compute_winnings(hands: list[Hand]) -> int:
    """
    Compute the winnings of a list of hands
    """

    # Having defined the rank in the Hand object
    # and a __lt__ and __eq__ method, we can sort
    # the hands just by calling .sort()
    hands.sort()

    winnings = 0
    for i, hand in enumerate(hands):
        winnings += (i+1) * hand.bid

    return winnings


def task1(input: list[str]) -> int:
    """
    Task 1: Compute winning without jokers
    """
    hands = read_input(input, jokers=False)
    return compute_winnings(hands)


def task2(input: list[str]) -> int:
    """
    Task 2: Computer winnings with jokers
    """
    hands = read_input(input, jokers=True)
    return compute_winnings(hands)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/07.in", sep="\n")
    input = util.read_strs("input/07.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)

"""
Day 22
https://adventofcode.com/2020/day/22

1st star: 00:10:07
2nd star: 01:02:51

Remember, kids: it's important to always carefully read the problem statement
so you understand exactly what the problem is asking you to do. I arrived
at a correct part 2 solution fairly quickly, and then spent a bunch of time
tracking down a bug that stemmed from not having read the problem statement
fully.
"""

import util
import math
import sys
import re

from util import log


def read_input(input_txt):
    """
    Reads in the input
    """
    player1 = input_txt[0].split("\n")
    player1 = [int(x) for x in player1[1:]]

    player2 = input_txt[1].split("\n")
    player2 = [int(x) for x in player2[1:]]

    decks = {1: player1, 2: player2}

    return decks


def hash_decks(decks):
    """
    Creates a hash of a game configuration, so we can keep track of
    the set of game configurations we've already seen.
    """
    all_cards = tuple(decks[1] + [-1] + decks[2])
    return all_cards


def play_game_r(decks, game_num=1, recursive=False):
    """
    Plays a game of Combat or Recursive Combat

    Returns a tuple (winner, loser)
    """

    log(f"=== Game {game_num} ===")
    round = 1
    configurations = set()

    while len(decks[1]) > 0 and len(decks[2]) > 0:
        log(f"-- Round {round} (Game {game_num})--")
        log("Player 1's deck:", ", ".join([str(x) for x in decks[1]]))
        log("Player 2's deck:", ", ".join([str(x) for x in decks[2]]))

        if hash_decks(decks) in configurations:
            return 1, 2
        else:
            configurations.add(hash_decks(decks))

            cards = {1: decks[1].pop(0), 2: decks[2].pop(0)}
            log("Player 1 plays:", cards[1])
            log("Player 2 plays:", cards[2])

            if recursive and len(decks[1]) >= cards[1] and len(decks[2]) >= cards[2]:
                log("Playing a sub-game to determine the winner...\n")
                decks_copy = {}
                decks_copy[1] = decks[1][:cards[1]]
                decks_copy[2] = decks[2][:cards[2]]
                winner, loser = play_game_r(decks_copy, game_num+1, True)
            elif cards[1] > cards[2]:
                winner = 1
                loser = 2
            elif cards[2] > cards[1]:
                winner = 2
                loser = 1
            log(f"Player {winner} wins round {round} of game {game_num}!")

            decks[winner].append(cards[winner])
            decks[winner].append(cards[loser])

        round += 1
        log()

    if len(decks[1]) == 0:
        winner = 2
        loser = 1
    elif len(decks[2]) == 0:
        winner = 1
        loser = 2

    log(f"The winner of game {game_num} is player {winner}!\n")
    
    if game_num > 1:
        log(f"...anyway, back to game {game_num-1}.")

    return winner, loser


def play_game(input_txt, recursive):
    decks = read_input(input_txt)

    winner, _ = play_game_r(decks, 1, recursive)

    log("== Post-game results ==")
    log("Player 1's deck:", ", ".join([str(x) for x in decks[1]]))
    log("Player 2's deck:", ", ".join([str(x) for x in decks[2]]))

    score = 0
    for card, n in zip(decks[winner], range(len(decks[winner]), 0, -1)):
        score += card * n

    return score    


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/22-1.in", sep="\n\n")
    sample2 = util.read_strs("input/sample/22-2.in", sep="\n\n")
    input = util.read_strs("input/22.in", sep="\n\n")

    print("TASK 1")
    util.call_and_print(play_game, sample1, False)
    util.call_and_print(play_game, input, False)

    print("\nTASK 2")
    util.call_and_print(play_game, sample1, True)
    util.call_and_print(play_game, sample2, True)
    util.call_and_print(play_game, input, True)


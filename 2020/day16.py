"""
Day 16
https://adventofcode.com/2020/day/16

1st star: 00:14:13
2nd star: 00:41:26

This was a satisfying problem to solve because I had an intuition
about how to narrow down the fields, thinking it would not work because
maybe it involved much fancier combinatorics, and then it worked!

My original code for this was a huge mess, so the code below
has been cleaned up a lot relative to what I actually used to
solve the problem.
"""

import util
import math
import sys

from util import log


def parse_notes(notes_str):
    """
    Parse the provided notes and return a dictionary of fields,
    your ticket, and the nearby tickets.
    
    """
    fields = {}
    
    fields_str = notes_str[0].split("\n")
    for line in fields_str:
        name, ranges = line.split(":")

        ranges = ranges.split(" or ")

        range_1 = [int(x) for x in ranges[0].split("-")]
        range_2 = [int(x) for x in ranges[1].split("-")]

        fields[name] = (range_1, range_2)

    my_ticket = [int(x) for x in notes_str[1].split("\n")[1].split(",")]

    nearby_ticket_str = notes_str[2].split("\n")
    nearby_ticket_str.pop(0)
    nearby_tickets = []
    for line in nearby_ticket_str:
        nearby_tickets.append([int(x) for x in line.split(",")])
    
    return fields, my_ticket, nearby_tickets


def is_valid(value, range_1, range_2):
    """
    Validates that a value is in one of the two ranges
    """

    range_1_valid = range_1[0] <= value <= range_1[1]
    range_2_valid = range_2[0] <= value <= range_2[1]

    return range_1_valid or range_2_valid


def task1(notes):
    fields, _, nearby_tickets = parse_notes(notes)

    invalid_values = []
    for ticket in nearby_tickets:
        for value in ticket:
            # Check whether the value is valid for, at least,
            # one field
            valid_for_some_field = False
            for _, (range_1, range_2) in fields.items():
                if is_valid(value, range_1, range_2):
                    valid_for_some_field = True
                    break
                    
            if not valid_for_some_field:
                invalid_values.append(value)
    
    return sum(invalid_values)


def get_valid_tickets(tickets, fields):
    """
    Gets the valid tickets (those where each value is valid for,
    at least, one field)
    """
    valid_tickets = []
    for ticket in tickets:
        # Check that all values are valid for, at least, one field
        all_values_valid = True
        for value in ticket:
            valid_for_some_field = False
            for _, (range_1, range_2) in fields.items():
                if is_valid(value, range_1, range_2):
                    valid_for_some_field = True
                    break
                    
            if not valid_for_some_field:
                all_values_valid = False
                break
    
        if all_values_valid:
            valid_tickets.append(ticket)
    return valid_tickets


def test_get_valid_tickets(notes):
    """
    For testing purposes only. Simple wrapper around 
    get_valid_tickets that we can call from __main__
    """
    fields, _, nearby_tickets = parse_notes(notes)

    return get_valid_tickets(nearby_tickets, fields)


def task2(notes):
    fields, my_ticket, nearby_tickets = parse_notes(notes)

    # Find out what tickets are valid
    valid_tickets = get_valid_tickets(nearby_tickets, fields)
    
    # Find out the candidate fields for each position
    # For each position, we start with a set containing all fields,
    # then check all values in that position (across all tickets,
    # including my ticket), and remove fields that won't work for
    # that position
    n_fields = len(my_ticket)
    candidate_fields = {i: set(fields.keys()) for i in range(n_fields)}

    for ticket in [my_ticket] + valid_tickets:
        for i, value in enumerate(ticket):
            for field, (range_1, range_2) in fields.items():
                range_1_valid = range_1[0] <= value <= range_1[1]
                range_2_valid = range_2[0] <= value <= range_2[1]

                if not (range_1_valid or range_2_valid):
                    candidate_fields[i].discard(field)

    # We're not done yet! Some positions will have multiple 
    # candidate fields. We sort the positions in ascending order
    # of number of candidate fields. Whenever we encounter a
    # position that has only one possible candidate field, we
    # remove that field from consideration in all the other positions.
    candidate_fields = list(candidate_fields.items())
    candidate_fields.sort(key=lambda x: len(x[1]))

    for i, (_, choices) in enumerate(candidate_fields):
        if len(choices) == 1:
            for j in range(i+1, len(candidate_fields)):
                candidate_fields[j][1].difference_update(choices)
    
    # Finally, find the fields that start with "departure"
    # and get their respective values in my ticket
    values = []
    for position, choices in candidate_fields:
        assert len(choices) == 1
        field_name = choices.pop()

        if field_name.startswith("departure"):
            values.append(my_ticket[position])

    return math.prod(values)



if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/16-1.in", sep="\n\n")
    sample2 = util.read_strs("input/sample/16-2.in", sep="\n\n")
    notes = util.read_strs("input/16.in", sep="\n\n")

    print("TASK 1")
    util.call_and_print(task1, sample1)
    util.call_and_print(task1, notes)

    print("\nTASK 2")
    util.call_and_print(test_get_valid_tickets, sample1)
    util.call_and_print(test_get_valid_tickets, sample2)
    util.call_and_print(task2, notes)

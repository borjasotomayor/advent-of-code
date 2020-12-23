"""
Day 23
https://adventofcode.com/2020/day/23

1st star: 00:49:27
2nd star: 01:53:52

I spent waaay too much time on this problem because of some unfortunate
early design decisions. I started off trying to avoid implementing
a circular array/buffer by concatenating the list of cups with itself,
and working on that instead, but that ended up involving having to
be very careful about lots of operations. 

And, once that was done, I had to scrap it entirely and do what I 
should've done from the get-go: use a linked list. I implemented 
it myself, WHICH I KNOW I ALWAYS SAY YOU SHOULD NEVER DO but I thought 
it would be fun, except for the solid 45 minutes I spent debugging 
linked list operations.

Anyway, the moral of the story is that you should always use existing linked
list implementations.
"""

import util
import math
import sys
import re

from util import log


class LinkedList:
    """
    A simple circular, doubly-linked list.
    """

    def __init__(self, value):
        self.value = value
        self.next = self
        self.prev = self


    def to_str(self, highlight=None, sep=" "):
        head = self
        cur = head
        values = []
        while True:
            if cur.value == highlight:
                values.append(f"({cur.value})")
            else:
                values.append(f"{cur.value}")
            
            cur = cur.next

            if cur == head:
                break

        return sep.join(values)


    def to_dict(self):
        head = self
        cur = head
        d = {}
        while True:
            d[cur.value] = cur
            
            cur = cur.next

            if cur == head:
                break

        return d


    def __str__(self):
        return self.to_str()


    def excise(self, n):
        """
        Excise the n nodes after the current node,
        and return them as a valid linked list.
        """
        first = self.next
        last = self
        values = []
        for _ in range(n):
            last = last.next
            values.append(last.value)

        self.next = last.next
        last.next.prev = self

        first.prev = last
        last.next = first    

        return first, values


    def stitch_after(self, lst):
        """
        Take a linked list and "stitch" it after the current node
        """
        last = lst.prev
        
        last.next = self.next
        last.next.prev = last

        self.next = lst
        lst.prev = self


    @classmethod
    def from_python_list(cls, lst):
        head = cls(lst[0])
        prev_node = head
        for x in lst[1:]:
            node = cls(x)
            prev_node.next = node
            node.prev = prev_node
            prev_node = node
        
        # Make it a circular list
        node.next = head
        head.prev = node

        return head


def play_game(cups, moves):
    ll = LinkedList.from_python_list(cups)
    min_cup = min(cups)
    max_cup = max(cups)

    current = ll

    nodes = ll.to_dict()

    for _ in range(moves):
        cup = current.value

        three_cups_lst, three_cups = current.excise(3)
        
        destination_cup = cup - 1
        while destination_cup in three_cups or destination_cup not in nodes:
            destination_cup -= 1
            if destination_cup < min_cup:
                destination_cup = max_cup

        destination_node = nodes[destination_cup]
        assert destination_node.value == destination_cup

        destination_node.stitch_after(three_cups_lst)

        current = current.next

    return nodes[1]


def task1(cups_txt, moves):
    cups = [int(x) for x in cups_txt]

    one_node = play_game(cups, moves)
    assert one_node.value == 1

    return one_node.to_str(sep="")[1:]


def task2(cups_txt, moves):
    cups = [int(x) for x in cups_txt]
    cups += list(range(max(cups)+1, 1000001))

    one_node = play_game(cups, moves)
    assert one_node.value == 1

    return one_node.next.value * one_node.next.next.value   


if __name__ == "__main__":
    util.set_debug(False)

    print("TASK 1")
    util.call_and_print(task1, "389125467", 10)
    util.call_and_print(task1, "389125467", 100)
    util.call_and_print(task1, "952316487", 100)

    print("\nTASK 2")
    util.call_and_print(task2, "389125467", 10000000)
    util.call_and_print(task2, "952316487", 10000000)


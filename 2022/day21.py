"""
Day 21
https://adventofcode.com/2022/day/21

1st star: 00:06:14
2nd star: 00:59:10

Part I just involved building an expression tree and evaluating it.
For Part II, I initially came up with a solution that was way more
complicated than it needed to be: I ran BFS to find the path from the
root to the "humn" node, and then passed that path to a recursive function
that would explore the tree in that order, figuring out the intermediate
values in each node so we could finally compute the value of "humn".

This took a while to write, and the intuition behind the approach
wasn't wrong: I needed a mechanism to distinguish "branches that
can be fully evaluated" from "branches that have the humn node
somewhere down the branch". I ended up rewriting my code almost
entirely so that the evaluation function (eval() below) would
save the evaluated value of a node, unless it was impossible
to do so (because there was a missing value). This then made it
much easier to start at the root and figure out which branch
contained the "humn" node and which one didn't.
"""

import util

from util import log


class Node:
    """
    Class for representing a node in the expression tree.
    Can be either a value node (directly containing a literal
    value) or an operation node (with two subtrees, one per
    operand)
    """

    VALUE_NODE = 1
    OP_NODE = 2

    def __init__(self, name, node_type):
        self.name = name
        self.type = node_type

        # If the type is VALUE_NODE, the value attribute
        # contains the literal value
        self.value = None

        # If the type is OP_NODE, the op attribute contains
        # the operation, and the op1 and op2 attributes
        # contain Node objects representing the subtrees of
        # this node
        self.op = None
        self.op1 = None
        self.op2 = None

        # When we evaluate the tree, we'll fill in this value.
        # If a node can be fully evaluated (because there are
        # no missing values somewhere in the subtrees), it
        # will contain the evaluated value of the tree. Otherwise,
        # it will remain None. This will allow us to easily
        # distinguish subtrees that contain a missing value somewhere.        
        self.eval_value = None

    def __repr__(self):
        """
        Simple __repr__ method
        """
        return f"Node('{self.name}')"

    def to_equation_str(self):
        """
        Returns a string representation of the entire expression
        """
        if self.type == Node.VALUE_NODE:
            return str(self.value)        
        elif self.type == Node.OP_NODE:
            op1s = self.op1.to_equation_str()
            op2s = self.op2.to_equation_str()
            return f"({op1s}{self.op}{op2s})"

    def eval(self):
        """
        Recursively evaluate the expression tree, updating
        the eval_value attributes as we go along.
        """
        if self.type == Node.VALUE_NODE:
            self.eval_value = self.value
            return self.eval_value
        elif self.type == Node.OP_NODE:
            op1 = self.op1.eval()
            op2 = self.op2.eval()
            
            if op1 is None or op2 is None:
                self.eval_value = None
                return None
            if self.op == "+":
                self.eval_value = op1 + op2
            elif self.op == "-":
                self.eval_value = op1 - op2
                return self.eval_value
            elif self.op == "*":
                self.eval_value = op1 * op2
                return self.eval_value
            elif self.op == "/":
                self.eval_value = op1 // op2
            return self.eval_value

    def compute_human_value(self, target=None):
        """
        Recursively compute the value of the 'humn' node.
        This depends on the tree having been evaluated,
        and eval_value being set to None if a Node has
        a missing value (the 'humn' node) somewhere in
        its subtrees.
        """

        # Distinguish between the branch that contains the "humn" node
        # and the branch that has been fully evaluated.
        humn_branch = self.op1 if self.op1.eval_value is None else self.op2
        done_branch = self.op1 if self.op1.eval_value is not None else self.op2

        # Since we know the value of one of the branches, we can
        # figure out what the value of the other branch should be
        # (our "new target"). 
        if self.op == "==":
            new_target = done_branch.eval_value
        elif self.op == "+":
            new_target = target - done_branch.eval_value
        elif self.op == "-":
            if humn_branch == self.op1:
                new_target = target + done_branch.eval_value
            elif humn_branch == self.op2:
                new_target = done_branch.eval_value - target
        elif self.op == "*":
            new_target = target // done_branch.eval_value
        elif self.op == "/":
            if humn_branch == self.op1:
                new_target = target * done_branch.eval_value
            elif humn_branch == self.op2:
                new_target = done_branch.eval_value // target

        # If the humn branch is the humn Node itself,
        # then we've found our target.
        if humn_branch.name == "humn":
            return new_target
        else:
            # Otherwise, we recursively explore the humn branch
            # with the new target.
            return humn_branch.compute_human_value(new_target)


def read_input(input):
    """
    Read input into a dictionary of Node objects
    """
    nodes = {}
    for name, contents in input:
        if len(contents) == 11:
            node = Node(name, Node.OP_NODE)
            node.op1, node.op, node.op2 = contents.split()
        else:
            node = Node(name, Node.VALUE_NODE)
            node.value = int(contents)
        nodes[name] = node

    for node in nodes.values():
        if node.op1 is not None and node.op2 is not None:
            node.op1 = nodes[node.op1]
            node.op2 = nodes[node.op2]

    return nodes


def task1(input):
    """
    Task 1: Evaluate the expression tree
    """
    nodes = read_input(input)

    return nodes["root"].eval()

def task2(input):
    """
    Task 2: Find the value of the "humn node"
    """
    nodes = read_input(input)

    # Set the "humn" node's value to None and evaluate 
    # the expression tree. Any node that depends on "humn"
    # will have its eval_value set to None
    nodes["humn"].value = None
    nodes["root"].eval()

    # Change the root operation
    nodes["root"].op = "=="

    # Compute and return the "humn" value
    return nodes["root"].compute_human_value()


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/21.in", sep="\n", sep2=": ")
    input = util.read_strs("input/21.in", sep="\n", sep2=": ")


    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)

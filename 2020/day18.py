"""
Day 18
https://adventofcode.com/2020/day/18

1st star: 00:32:42
2nd star: 00:39:23

This was a trip down memory lane; I haven't parsed arithmetic expressions
like this since I was in grad school. Once I brushed up on how to
evaluate arithmetic expressions, it was mostly just a question of
implementing a textbook infix evaluator (using the shunting-yard
algorithm)
"""

import util
import math
import sys
import re

from util import log


### Precedence functions

def equal_precedence(oper):
    """
    All operators have equal precedence
    """
    return 0


def addition_precedence(oper):
    """
    Addition has greater precedence than multiplication
    """
    if oper == "+":
        return 2
    elif oper == "*":
        return 1
    else:
        return 0
    

def eval_expression(expr, precedence=equal_precedence):
    """
    Evaluate an expression using the provided precedence function
    """

    # Easy left-to-right evaluation: just turn the expression around!
    expr = expr[::-1].translate({ord("("):ord(")"),
                                 ord(")"):ord("(")})

    # Convert the expression to a postfix expression
    postfix_expr = []
    stack = []
    for char in expr:
        if char.isdigit():
            postfix_expr.append(int(char))
        elif char == "(":
            stack.append(char)
        elif char == ")":
            while len(stack) != 0 and stack[-1] != "(":
                postfix_expr.append(stack.pop())
            stack.pop()
        elif char in ("+", "*"):
            if len(stack) == 0 or precedence(char) >= precedence(stack[-1]):
                stack.append(char)
            else:
                while len(stack) != 0  and precedence(char) <= precedence(stack[-1]):
                    postfix_expr.append(stack.pop())
                stack.append(char)

    while len(stack) != 0:
        postfix_expr += stack.pop()
    
    # Evaluate the postfix expression
    for x in postfix_expr:
        if isinstance(x, int):
            stack.append(x)
        elif x in ("+", "*"):
            op1 = stack.pop()
            op2 = stack.pop()

            if x == "+":
                stack.append(op1 + op2)
            elif x == "*":
                stack.append(op1 * op2)

    return(stack[0])
            

def sum_expressions(exprs, precedence=equal_precedence):
    """
    Evaluate a list of expressions and return the sum
    """

    v = 0
    for expr in exprs:
        v += eval_expression(expr, precedence)
    return v


if __name__ == "__main__":
    util.set_debug(False)

    expressions = util.read_strs("input/18.in", sep="\n")

    print("TASK 1")
    
    util.call_and_print(eval_expression, "1 + 2 * 3 + 4 * 5 + 6")
    util.call_and_print(eval_expression, "1 + (2 * 3) + (4 * (5 + 6))")
    util.call_and_print(eval_expression, "2 * 3 + (4 * 5)")
    util.call_and_print(eval_expression, "5 + (8 * 3 + 9 + 3 * 4 * 3)")
    util.call_and_print(eval_expression, "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))")
    util.call_and_print(eval_expression, "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
    util.call_and_print(sum_expressions, expressions)

    print("\nTASK 2")
    util.call_and_print(eval_expression, "1 + 2 * 3 + 4 * 5 + 6", addition_precedence)
    util.call_and_print(eval_expression, "1 + (2 * 3) + (4 * (5 + 6))", addition_precedence)
    util.call_and_print(eval_expression, "2 * 3 + (4 * 5)", addition_precedence)
    util.call_and_print(eval_expression, "5 + (8 * 3 + 9 + 3 * 4 * 3)", addition_precedence)
    util.call_and_print(eval_expression, "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", addition_precedence)
    util.call_and_print(eval_expression, "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", addition_precedence)
    util.call_and_print(sum_expressions, expressions, addition_precedence)


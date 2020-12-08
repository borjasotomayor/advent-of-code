"""
This module provides a Console class for running console programs
(so far, only on day 8)
"""

from util import read_strs

class ConsoleException(Exception):
    pass

class Console:
    OP_NOP = "nop"
    OP_ACC = "acc"
    OP_JMP = "jmp"


    def __init__(self, prog):
        self.orig_prog = prog[:]
        self.reset()


    @classmethod
    def from_file(cls, filename):
        lines = read_strs(filename, sep="\n")

        program = []
        for line in lines:
            op, param = line.strip().split()
            program.append((op, int(param)))

        return cls(program)


    def reset(self):
        self.prog = self.orig_prog[:]
        self.pc = 0
        self.acc = 0
        self.pc_set = set()


    def clone(self):
        new_vm = Console(self.prog)
        new_vm.orig_prog = self.orig_prog[:]
        new_vm.pc = self.pc
        new_vm.acc = self.acc

        return new_vm


    def run(self, expect_outputs = 1):

        while True:
            if self.pc in self.pc_set:
                break
            
            self.pc_set.add(self.pc)
            op, param = self.prog[self.pc]
            next_pc = self.pc + 1

            if op == Console.OP_NOP:
                pass
            elif op == Console.OP_ACC:
                self.acc += param
            elif op == Console.OP_JMP:
                next_pc = self.pc + param

            self.pc = next_pc

            if self.pc == len(self.prog):
                break


    def normal_termination(self):
        return self.pc == len(self.prog)


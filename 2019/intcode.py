class IntCodeException(Exception):
    pass

class IntCode:
    """
    IntCode virtual machine
    """

    # Opcodes
    OP_ADD=1
    OP_MUL=2
    OP_IN=3
    OP_OUT=4
    OP_JMPT=5
    OP_JMPF=6
    OP_LT=7
    OP_EQ=8
    OP_RELBASE=9
    OP_HALT=99

    # Addressing
    MODE_POSITION=0
    MODE_IMMEDIATE=1
    MODE_RELATIVE=2

    # Parameter specifications
    READ=0
    WRITE=1

    OPCODES = {
        OP_ADD: [READ, READ, WRITE],
        OP_MUL: [READ, READ, WRITE],
        OP_IN: [WRITE],
        OP_OUT: [READ],
        OP_JMPT: [READ, READ],
        OP_JMPF: [READ, READ],
        OP_LT: [READ, READ, WRITE],
        OP_EQ: [READ, READ, WRITE],
        OP_RELBASE: [READ],
        OP_HALT: []
    }

    BREAK_INPUT_REQUIRED = 0
    BREAK_INPUT_DONE = 1
    BREAK_OUTPUT_AVAILABLE = 2
    HALT = 3

    def __init__(self, prog):
        """
        Creates an IntCode machine with the given program
        """
        self.orig_prog = prog[:]
        self.reset()

    def reset(self):
        """
        Resets the machine
        """
        self.memory = self.orig_prog[:]
        self.pc = 0
        self._input = None
        self.outputs = []
        self.relative_base = 0
        self.last_break = None

    def clone(self):
        """
        Creates a clone of the machine
        """
        new_vm = IntCode(self.memory)
        new_vm.orig_prog = self.orig_prog[:]
        new_vm.pc = self.pc
        new_vm.relative_base = self.relative_base
        new_vm._input = self._input
        new_vm.outputs = self.outputs[:]
        new_vm.last_break = self.last_break

        return new_vm

    def __extend_memory(self, address):
        """
        Extends the size of the memory (with 0's) up to
        the given address
        """
        extra_positions = address - len(self.memory) + 1
        self.memory.extend([0] * extra_positions)

    def __check_address(self, address):
        """
        Checks if the given memory address is valid
        """
        if address >= len(self.memory):
            return False
        else:
            return True

    def write(self, address, value):
        """
        Writes a value into an address, extending
        the memory if necessary
        """
        if not self.__check_address(address):
            self.__extend_memory(address)
        self.memory[address] = value
        
    def read(self, address):
        """
        Reads a value from an address.
        Note that, if the memory has to be extended to
        the given address, that new address will be
        initialized to a zero by default.
        """
        if not self.__check_address(address):
            self.__extend_memory(address)
        return self.memory[address]

    def parse_operation(self):
        """
        Parses the operation starting at the Program Counter.

        Returns a tuple with the opcode, a list of parameters,
        and the next value of the Program Counter after running
        this operation.
        """
        p = self.memory
        i = self.pc

        op = p[i]
        strop = str(op)
        if op <= 99:
            opcode = op
        else:
            opcode = int(strop[-2:])

        assert opcode in IntCode.OPCODES

        params = []
        param_types = IntCode.OPCODES[opcode]
        for n, ptype in enumerate(param_types):
            if op <= 99:
                mode = IntCode.MODE_POSITION            
            else:
                offset = 3 + n
                if len(strop) < offset:
                    mode = IntCode.MODE_POSITION
                else:
                    mode = int(strop[-offset])

            assert mode in (IntCode.MODE_POSITION, IntCode.MODE_IMMEDIATE, IntCode.MODE_RELATIVE)

            x = p[i+(n+1)]
            if mode in (IntCode.MODE_POSITION, IntCode.MODE_RELATIVE):
                if mode == IntCode.MODE_POSITION:
                    address = x
                elif mode == IntCode.MODE_RELATIVE:
                    address = self.relative_base + x
                if ptype == IntCode.READ:
                    params.append(self.read(address))
                elif ptype == IntCode.WRITE:
                    params.append(address)
            elif mode == IntCode.MODE_IMMEDIATE:
                params.append(x)

        return opcode, params, i+1+len(params)

    def run(self, expect_outputs = 1):
        self.outputs = []
        while True:
            op, params, next_pc = self.parse_operation()
            if op == IntCode.OP_ADD:
                self.write(params[2], params[0] + params[1])
            elif op == IntCode.OP_MUL:
                self.write(params[2], params[0] * params[1])
            elif op == IntCode.OP_IN:
                if self._input is not None:
                    v = self._input
                    self._input = None
                else:
                    self.last_break = IntCode.BREAK_INPUT_REQUIRED
                    return IntCode.BREAK_INPUT_REQUIRED
                self.write(params[0], v)
                self.pc = next_pc
                self.last_break = IntCode.BREAK_INPUT_DONE
                return IntCode.BREAK_INPUT_DONE
            elif op == IntCode.OP_OUT:
                self.outputs.append(params[0])
                self.pc = next_pc
                expect_outputs -= 1
                if expect_outputs == 0:
                    self.last_break = IntCode.BREAK_OUTPUT_AVAILABLE
                    return IntCode.BREAK_OUTPUT_AVAILABLE
            elif op == IntCode.OP_JMPT:
                if params[0] != 0:
                    self.pc = params[1]
                    continue
            elif op == IntCode.OP_JMPF:
                if params[0] == 0:
                    self.pc = params[1]
                    continue
            elif op == IntCode.OP_LT:
                if params[0] < params[1]:
                    self.write(params[2], 1)
                else:
                    self.write(params[2], 0)
            elif op == IntCode.OP_EQ:
                if params[0] == params[1]:
                    self.write(params[2], 1)
                else:
                    self.write(params[2], 0)
            elif op == IntCode.OP_RELBASE:
                self.relative_base += params[0]

            elif op == 99:
                self.last_break = IntCode.HALT
                return IntCode.HALT

            self.pc = next_pc

    def run_interactive(self, ascii=False):
        rv = None

        while rv != IntCode.HALT:
            rv = self.run()
            if rv == IntCode.BREAK_OUTPUT_AVAILABLE:
                if ascii:
                    self.print_output()
                else:
                    print(self.get_output())
            elif rv == IntCode.BREAK_INPUT_REQUIRED:
                if ascii:
                    inp = input()
                    self.input_string(inp, add_newline=True)
                else:
                    inp = input("Enter the input: ")
                    self.set_input(int(inp))

    def get_output(self):
        assert len(self.outputs) == 1
        return self.outputs[0]

    def print_output(self, printable_limit = 255):
        while True:
            rv = self.run(expect_outputs=1)

            if rv != IntCode.BREAK_OUTPUT_AVAILABLE:
                return None

            n = self.get_output()
            if n < printable_limit:
                print(chr(n), end='')
            else:
                return n

    def output(self):
        if len(self.outputs) > 0:
            return self.outputs.pop()
        else:
            rv = self.run(expect_outputs=1)
            if rv != IntCode.BREAK_OUTPUT_AVAILABLE:
                raise IntCodeException("Asked for an output but none happened")
            return self.get_output()

    def set_input(self, input):
        self._input = input

    def input(self, input):
        self.set_input(input)
        rv = self.run()
        if rv != IntCode.BREAK_INPUT_DONE:
            raise IntCodeException("Requested an input but the program did not read it")

    def input_string(self, s, add_newline=False, echo=True):
        if add_newline:
            s = s + chr(10)
        for x in s:
            if echo:
                print(x, end='')
            self.set_input(ord(x))
            rv = self.run()
            if rv != IntCode.BREAK_INPUT_DONE:
                break

        return rv



"""CPU functionality."""
from dispatch_table import DispatchTable
import sys
from ast import literal_eval
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = False
        self.pc = 0
        self.program_file = None
        self.dispatch_table = DispatchTable(self)

    def increment(self, num=1):
        for i in range(num):
            self.pc += 1
    
    def decrement(self, num=1):
        for i in range(num):
            self.pc -= 1

    def load(self, file=None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        if file is None:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]
        else:
            program = []
            file_text = open(file, "r")
            for f in file_text:
                if f[0] == '#':
                    continue
                elif f[0] == '\n':
                    continue
                elif " " in f:
                    f = f[:f.find(" ")]
                program.append(literal_eval('0b'+f))
            #     print(f"INSTRUCTION: {program[:-1]}")
            # print(f"PROGRAM:\n{program}")

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            operand_a = self.ram_read(reg_a)
            operand_b = self.ram_read(reg_b)
            self.ram_write(operand_a+operand_b, reg_a)
        elif op == "SUB":
            operand_a = self.ram_read(reg_a)
            operand_b = self.ram_read(reg_b)
            self.ram_write(operand_a-operand_b, reg_a)
        elif op == "MUL":
            operand_a = self.ram_read(reg_a)
            operand_b = self.ram_read(reg_b)
            self.ram_write(operand_a*operand_b, reg_a)
        elif op == "DIV":
            operand_a = self.ram_read(reg_a)
            operand_b = self.ram_read(reg_b)
            self.ram_write(operand_a/operand_b, reg_a)
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # Translate binary instructions to text
        instruction_map = {
            # Other
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b00000001: 'HLT',
            0b00000000: 0,

            # ALU Operations
            0b10100000: 'ADD',
            0b10100001: 'SUB',
            0b10100010: 'MUL',
            0b10100011: 'DIV',
        }

        # List of operations to be handled by ALU
        alu_ops = [
            'ADD',
            'SUB',
            'MUL',
            'DIV'
        ]

        self.running = True
        self.pc = 0

        while self.running:
            cmd = self.ram_read(self.pc)
            self.dispatch_table.execute(cmd)
            # instruction = instruction_map[cmd]

            # if instruction == 'HLT':
            #     self.running = False
            #     self.pc += 1
            # elif instruction == 'PRN':
            #     reg = self.ram_read(self.pc + 1)
            #     data = self.ram_read(reg)
            #     print(data)
            #     self.pc += 2
            # elif instruction == 'LDI':
            #     reg = self.ram_read(self.pc + 1)
            #     data = self.ram_read(self.pc + 2)
            #     self.ram_write(data, reg)
            #     self.pc += 3
            # elif instruction in alu_ops:
            #     reg_a = self.ram_read(self.pc + 1)
            #     reg_b = self.ram_read(self.pc + 2)
            #     self.alu(instruction, reg_a, reg_b)
            #     self.pc += 3
            # elif instruction == 0:
            #     self.pc += 1

    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, data, addr):
        self.ram[addr] = data

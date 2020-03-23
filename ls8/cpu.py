"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.running = False
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    # TODO
    def run(self):
        """Run the CPU."""

        instruction_map = {
            0b10000010: 'LDI',
            0b01000111: 'PRN',
            0b00000001: 'HLT',
            0b00000000: 0
        }

        self.running = True
        pc = 0
        while self.running:
            cmd = self.ram_read(pc)
            # print(f"CMD: {cmd}")
            instruction = instruction_map[cmd]
            if instruction == 'HLT':
                self.running = False
                pc += 1
            elif instruction == 'PRN':
                reg = self.ram_read(pc + 1)
                data = self.ram_read(reg)
                print(data)
                pc += 2
            elif instruction == 'LDI':
                reg = self.ram_read(pc + 1)
                data = self.ram_read(pc + 2)
                self.ram_write(data, reg)
                pc += 3
            elif instruction == 0:
                pc += 1
                
            
            # if cmd == 0b01000111:

            # elif cmd == 0b00000001:
            #     self.running = False
            #     pc += 1
            

    # TODO
    def ram_read(self, addr):
        return self.ram[addr]

    # TODO
    def ram_write(self, data, addr):
        self.ram[addr] = data
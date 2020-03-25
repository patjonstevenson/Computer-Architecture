class DispatchTable:
    '''
    Contains a mapping of binary instructions to functions
    Initialized with a CPU instance
    '''
    def __init__(self, cpu):
        self.cpu = cpu
        self.table = {
            # ALU Operations
            0b10100000: self.add,
            0b10100001: self.sub,
            0b10100010: self.mul,
            0b10100011: self.div,

            # Other
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000001: self.hlt,
        }

    def execute(self, cmd):
        if cmd not in self.table:
            raise Exception(f"Unsupported Operation: {cmd}")
        else:
            instruction = self.table[cmd]
            instruction()

    def ldi(self):
        reg = self.cpu.ram_read(self.cpu.pc + 1)
        data = self.cpu.ram_read(self.cpu.pc + 2)
        self.cpu.ram_write(data, reg)
        self.cpu.increment(3)
    
    def prn(self):
        reg = self.cpu.ram_read(self.cpu.pc + 1)
        data = self.cpu.ram_read(reg)
        print(data)
        self.cpu.increment(2)
    
    def hlt(self):
        self.cpu.running = False
        self.cpu.increment()

    # ALU Operations
    def add(self):
        reg_a = self.cpu.ram_read(self.cpu.pc + 1)
        reg_b = self.cpu.ram_read(self.cpu.pc + 2)
        operand_a = self.cpu.ram_read(reg_a)
        operand_b = self.cpu.ram_read(reg_b)
        self.cpu.ram_write(operand_a + operand_b, reg_a)
        self.cpu.increment(3)

    def sub(self):
        reg_a = self.cpu.ram_read(self.cpu.pc + 1)
        reg_b = self.cpu.ram_read(self.cpu.pc + 2)
        operand_a = self.cpu.ram_read(reg_a)
        operand_b = self.cpu.ram_read(reg_b)
        self.cpu.ram_write(operand_a - operand_b, reg_a)
        self.cpu.increment(3)

    def mul(self):
        reg_a = self.cpu.ram_read(self.cpu.pc + 1)
        reg_b = self.cpu.ram_read(self.cpu.pc + 2)
        operand_a = self.cpu.ram_read(reg_a)
        operand_b = self.cpu.ram_read(reg_b)
        self.cpu.ram_write(operand_a * operand_b, reg_a)
        self.cpu.increment(3)

    def div(self):
        reg_a = self.cpu.ram_read(self.cpu.pc + 1)
        reg_b = self.cpu.ram_read(self.cpu.pc + 2)
        operand_a = self.cpu.ram_read(reg_a)
        operand_b = self.cpu.ram_read(reg_b)
        self.cpu.ram_write(operand_a/operand_b, reg_a)
        self.cpu.increment(3)
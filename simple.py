import sys

# OP CODES
PRINT_BEEJ     = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4 # Save value to a register 
PRINT_REGISTER = 5 # 
ADD            = 6 # 


memory = [
    PRINT_BEEJ,
    SAVE,
    65,
    2,
    SAVE,
    20,
    3,
    ADD,
    2,
    3,
    PRINT_REGISTER,
    2,
    HALT
]

register = [0] * 8

pc = 0
running = True

while running:
    command = memory[pc]
    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    elif command == HALT:
        running = False
        pc += 1
    elif command == PRINT_NUM:
        r = memory[pc + 1]
        print(r)
        pc += 1
    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3
    elif command == PRINT_REGISTER:
        reg  = memory[pc + 1]
        print(register[reg])
        pc += 2
    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3
    else:
        print(f"Instruction Unknown: {command}")
        pc += 1

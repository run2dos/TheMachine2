#!py -3
# -*- coding: utf-8 -*-
# @author: ResolaQQ
# @version: 201502042014
# @english blog: http://resolaqqen.blogspot.tw/2015/01/my-chip-8-emulator-written-in-python.html
# @chinese blog: http://resolaqq.blogspot.tw/2014/10/my-chip-8-emulator-written-in-python.html
import collections
import mmap
import numpy
import queue
import random
import string
import sys
import time




#==============================================================================
# hardware
#==============================================================================

# ********** IMPORTANT ********** #
# ********** IMPORTANT ********** #
# ********** IMPORTANT ********** #
# If you are not familiar with Python, you'd better declare global every time before you access global variables like DT, ST, I, OPCODE, etc.
# example:
# def change_dt():
#     global I
#     I = 9999
#
# In the above case, if you didn't declare I as a global variable, It will become a local variable, which means that you did nothing to the true I variable at all.
# The emulator will probably run normally, execute opcode like everything is ok, but the screen you wish will never appear.
# ********** IMPORTANT ********** #
# ********** IMPORTANT ********** #
# ********** IMPORTANT ********** #




# Memory
# 4096 (0x1000) memory locations, all of which are 8 bits (a byte) 
# Use MEMORY[0x1234] to access
MEMORY = numpy.zeros([0x1000], numpy.uint8)




# Registers
# 16 8-bit data registers named from V0 to VF. The VF register doubles as a carry flag
# The address register, which is named I, is 16 bits wide and is used with several opcodes that involve memory operations
# Use I and V[0] to V[15] or V[0x0] to V[0xF] to access
V = numpy.zeros([0xF+1], numpy.uint8) 
I = numpy.uint16(0)




# The stack
# The stack is only used to store return addresses, modern implementations normally have at least 16 levels
# It's usually implemeted by an array and a pointer, In python we can direct use a list instead
STACK = []




# Timers
# CHIP-8 has two timers. They both count down at 60 hertz, until they reach 0.
# Delay timer: This timer is intended to be used for timing the events of games. Its value can be set and read.
# Sound timer: This timer is used for sound effects. When its value is nonzero, a beeping sound is made.
# Use 2 integer to save its value and decrease its value in every emulate cycle
DT = 0
ST = 0




# Input
# Input is done with a hex keyboard that has 16 keys which range from 0 to F. The '8', '4', '6', and '2' keys are typically used for directional input. 
# Save key state as a list. For example, if button down is pressed then KEYBOARD[2] will be set to 1.
KEYBOARD = [0] * 16




# Graphics
# Display resolution is 64×32 pixels, and color is monochrome. 
# Use a 2 dimensions array to emulate it.
# The coordinate of the graphics looks like
# +--------------------------+
# |(0, 0)             (63, 0)|
# |                          |
# |                          |
# |(0, 31)           (63, 31)|
# +--------------------------+
# You can type SCREEN[y, x] = 1 if you want to output a pixel on the position (x, y)
SCREEN = numpy.ndarray((32, 64), numpy.bool)




# Sound
# Use print('\a') will make a sound. 
def beep():
    print('\a', end='')
    sys.stdout.flush()




# Opcode table
# Opcode is the instruction to be executed, which is stored in memory.
# CHIP-8 has 35 opcodes, which are all two bytes long. While memory is one byte long, It means that you need to read 2 bytes from memory to get one opcode
OPCODE = 0




# Program counter
# Point to the memory address of next executed opcode 
# Most programs written for the original system begin at memory location 512 (0x200) 
PC = 0x200




#==============================================================================
# global
#==============================================================================

# used to save time slice which less than 1/60 second
time_slice = 0




# used to print the variable change after execute an opcode
traces = collections.OrderedDict()




#==============================================================================
# instruction
#==============================================================================
def instruction_00EE():
    print('00EE     Return from subroutine')
    global PC
    trace_stack()
    trace_pc()
    PC = STACK.pop()
    PC += 2




def instruction_1NNN():
    print('1NNN     Jump to NNN')
    global PC
    NNN = OPCODE & 0X0FFF
    print_nnn(NNN)
    trace_pc()
    PC = NNN




def instruction_2NNN():
    print('2NNN     Call subroutine at NNN')
    global PC
    NNN = OPCODE & 0x0FFF
    print_nnn(NNN)
    trace_stack()
    STACK.append(PC)
    trace_pc()
    PC = NNN 




def instruction_3XKK():
    print('3XKK     Skip next instruction if VX == KK')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    KK = OPCODE & 0x00FF
    print_kk(KK)
    print_v(X)
    trace_pc()
    if V[X] == KK:
        PC += 4
    else:
        PC += 2




def instruction_4XKK():
    print('4XKK     Skip next instruction if VX <> KK')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    KK = OPCODE & 0x00FF
    print_kk(KK)
    print_v(X)
    trace_pc()
    if V[X] != KK:
        PC += 4
    else:
        PC += 2




def instruction_6XKK():
    print('6XKK     VX := KK')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    KK = OPCODE & 0x00FF
    print_kk(KK)
    trace_v(X)
    V[X] = KK 
    trace_pc()
    PC += 2




def instruction_7XKK():
    print('7XKK     VX := VX + KK')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    KK = OPCODE & 0x00FF
    print_kk(KK)
    trace_v(X)
    V[X] += KK 
    trace_pc()
    PC += 2




def instruction_8XY0():
    print('8XY0     VX := VY, VF may change')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    Y = get_byte(OPCODE, 1)
    print_y(Y)
    print_v(Y)
    trace_v(X)
#   VF may change? How?
#    trace_v(0xF)    
    V[X] = V[Y]
    trace_pc()
    PC += 2
    



def instruction_8XY2():
    print('8XY2     VX := VX and VY, VF may change') 
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    Y = get_byte(OPCODE, 1)
    print_y(Y)
    print_v(Y)
    trace_v(X)
#   VF may change? How?
#    trace_v(0xF)
    V[X] &= V[Y]
    trace_pc()
    PC += 2



def instruction_8XY4():
    print('8XY4     VX := VX + VY, VF := carry')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    Y = get_byte(OPCODE, 1)
    print_y(Y)
    print_v(Y)
    trace_v(X)
    vx = int(V[X])
    vy = int(V[Y])
    vz = vx + vy
    V[X] = vz % 0x100
    trace_v(0xF)
    if vz > 0xFF:
        V[0xF] = 1
    else:
        V[0xF] = 0
    trace_pc()
    PC += 2
    



def instruction_8XY5():
    print('8XY5     VX := VX - VY, VF := not borrow')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    Y = get_byte(OPCODE, 1)
    print_y(Y)
    print_v(Y)
    trace_v(X)
    vx = int(V[X])
    vy = int(V[Y])
    vz = vx - vy
    if vz < 0:
        V[X] = vz + 0x100
    else:
        V[X] = vz
    trace_v(0xF)
    if vz < 0:
        V[0xF] = 0
    else:
        V[0xF] = 1
    trace_pc()
    PC += 2




def instruction_ANNN():
    print('ANNN     I := NNN')
    global PC, I
    NNN = OPCODE & 0x0FFF
    print_nnn(NNN)
    trace_i()
    I = NNN
    trace_pc()
    PC += 2




def instruction_CXKK():
    print('CXKK     VX := pseudorandom_number and KK')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    KK = OPCODE & 0x00FF
    print_kk(KK)
    trace_v(X)
    random_number = random.randint(0, 0xFF)
    print_random_number(random_number)
    V[X] = random_number & KK
    trace_pc()
    PC += 2




def instruction_DXYN():
    print('DXYN*    Show N-byte sprite from M(I) at coords (VX,VY), VF := collision. If N=0 and extended mode, show 16x16 sprite.')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    Y = get_byte(OPCODE, 1)
    print_y(Y)
    N = get_byte(OPCODE, 0)
    print_n(N)
    print_v(X)
    print_v(Y)
    # get sprite, which is saved the same as font
    print_i()
    print_memory(I, N)
    sprite_bytes = MEMORY[I:I+N]
    sprite = numpy.zeros((N, 8), numpy.bool) 
    for y in range(N):
        for x in range(8):
            # The bit of a byte indexed from 0 to 7 
            rx = 7 - x
            if get_bit(sprite_bytes[y], rx) == 1:
                sprite[y][x] = 1
    print_sprite(sprite)
    # output to screen
    trace_screen()
    trace_v(0xF)
    V[0xF] = 0
    for y in range(N):
        for x in range(8):
            if sprite[y][x] == 1:
                sy = V[Y] + y
                sx = V[X] + x
                # prevent the sprite output gets out of the screen
                sh, sw = SCREEN.shape
                if sy < sh and sx < sw:
                    # detect collision
                    if SCREEN[sy][sx] == 1:
                        V[0xF] = 1
                    # All drawing is XOR drawing
                    SCREEN[sy][sx] ^= 1 
    trace_pc()
    PC += 2
    



def instruction_EXA1():
    print('EXA1     Skip next instruction if key VX not pressed')
    global PC, KEYBOARD
    X = get_byte(OPCODE, 2)
    print_x(X)
    print_v(X)
    # translate data in shared memory to KEYBOARD
    m = mmap.mmap(-1, 16, 'KEYBOARD')
    data = m.read()
    m.close()
    for i in range(16):
        KEYBOARD[i] = data[i]
    print_keyboard()
    trace_pc()
    if KEYBOARD[V[X]] == 0:
        PC += 4
    else:
        PC += 2




def instruction_FX07():
    print('FX07     VX := delay_timer')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    print_dt()
    trace_v(X)
    V[X] = DT
    trace_pc()
    PC += 2




def instruction_FX15():
    print('FX15     delay_timer := VX')
    global PC, DT
    X = get_byte(OPCODE, 2)
    print_x(X)
    print_v(X)
    trace_dt()
    DT = V[X]
    trace_pc()
    PC += 2




def instruction_FX18():
    print('FX18     sound_timer := VX') 
    global PC, ST, st_set
    X = get_byte(OPCODE, 2)
    print_x(X)
    print_v(X)
    trace_st()
    ST = V[X]
    beep()
    trace_pc()
    PC += 2
    




def instruction_FX29():
    print('FX29     Point I to 5-byte font sprite for hex character VX')
    global PC, I
    X = get_byte(OPCODE, 2)
    print_x(X)
    print_v(X)
    trace_i()
    I = V[X] * 5
    trace_pc()
    PC += 2
    
    


def instruction_FX33():
    print('FX33     Store BCD representation of VX in M(I)..M(I+2)')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    print_v(X)
    trace_memory(I, 3)
    MEMORY[I] = V[X] // 100 % 10
    MEMORY[I+1] = V[X] // 10 % 10
    MEMORY[I+2] = V[X] % 10
    trace_pc()
    PC += 2




def instruction_FX65():
    print('FX65     Read V0..VX from memory starting at M(I)')
    global PC
    X = get_byte(OPCODE, 2)
    print_x(X)
    print_memory(I, X+1)
    for i in range(X+1):
        trace_v(i)
        V[i] = MEMORY[I+i]
    trace_pc()
    PC += 2




#==============================================================================
# debug print
#==============================================================================
def print_opcode():
    print('OPCODE: {0:04X}'.format(OPCODE))
    



def print_memory(index, count=1):
    first = True
    for i in range(count):
        if first:
            print('MEMORY[{0:04X}]: {1:04X}'.format(index+i, MEMORY[index+i]))
        else:
            print('      [{0:04X}]: {1:04X}'.format(index+i, MEMORY[index+i]))
        first = False




def print_v(index):
    print('V[{0:X}]: {1:02X}'.format(index, V[index]))




def print_i():
    print('I: {0:04X}'.format(I))





def print_keyboard():
    print('KEYBOARD: ', end='')
    for k in KEYBOARD:
        print(k, end='')
    print()




def print_dt():
    print('DT: {0:02X}'.format(DT))




def print_x(X):
    print('X: {0:X}'.format(X))




def print_y(Y):
    print('Y: {0:X}'.format(Y))
    



def print_n(N):
    print('N: {0:X}'.format(N))
    



def print_kk(KK):
    print('KK: {0:02X}'.format(KK))




def print_nnn(NNN):
    print('NNN: {0:03X}'.format(NNN))




def print_random_number(random_number):
    print('RANDOM_NUMBER: {0:02X}'.format(random_number))
    



def print_sprite(sprite):
    h, w = sprite.shape
    first_line = True
    for y in range(h):
        if first_line:
            print('SPRITE: ', end='')
        else:
            print('        ', end='')
        first_line = False
        for x in range(w):
            print('{0:d} '.format(sprite[y][x]), end='')
        print()




def trace_pc():
    traces['PC'] = eval('PC')




def trace_memory(index, count):
    traces[('MEMORY', index, count)] = MEMORY[index:index+count] 




def trace_i():
    traces['I'] = eval('I')




def trace_v(index):
    traces[('V', index)] = eval('V[{0}]'.format(index))




def trace_stack():
    traces['STACK'] = STACK.copy()




def trace_dt():
    traces['DT'] = DT




def trace_st():
    traces['ST'] = ST




def trace_screen():
    traces['SCREEN'] = SCREEN.copy()




def print_trace():
    global traces
    for variable_data, old_variable in traces.items():
        if type(variable_data) is str:
            if variable_data == 'I':
                print('I: {0:04X} > {1:04X}'.format(old_variable, I))
            elif variable_data == 'STACK':
                print('STACK: ', end='')
                if not old_variable:
                    print('None', end='')
                else:
                    for v in old_variable:
                        print('{0:04X} '.format(v), end='')
                print()
                print('       >')
                print('       ', end='')
                if not STACK:
                    print('None', end='')
                else:
                    for v in STACK:
                        print('{0:04X} '.format(v), end='')
                print()
            elif variable_data == 'DT':
                print('DT: {0:02X} > {1:02X}'.format(old_variable, DT))
            elif variable_data == 'ST':
                print('ST: {0:02X} > {1:02X}'.format(old_variable, ST))                
            elif variable_data == 'SCREEN':
                h, w = old_variable.shape
                first_line = True
                for y in range(h):
                    if first_line:
                        print('SCREEN: ', end='')
                    else:
                        print('        ', end='')
                    first_line = False
                    for x in range(w):
                        print('{0:d} '.format(old_variable[y][x]), end='')
                    print()
                print('        >')
                h, w = SCREEN.shape
                for y in range(h):
                    print('        ', end='')
                    for x in range(w):
                        print('{0:d} '.format(SCREEN[y][x]), end='')
                    print()
            elif variable_data == 'PC':
                print('PC: {0:04X} > {1:04X}'.format(old_variable, PC))
            else:
                raise NotImplementedError('can\'t display {0}'.format(variable_data))
        else:
            if variable_data[0] == 'V':
                index = variable_data[1]
                print('V[{0:X}]: {1:02X} > {2:02X}'.format(index, old_variable, V[index]))
            elif variable_data[0] == 'MEMORY':
                first = True
                for i in range(variable_data[2]):
                    if first:
                        print('MEMORY[{0:04X}]: {1:04X}'.format(variable_data[1]+i, old_variable[i]))
                    else:
                        print('      [{0:04X}]: {1:04X}'.format(variable_data[1]+i, old_variable[i]))
                    first = False
                print('       >')
                for i in range(variable_data[2]):
                    print('      [{0:04X}]: {1:04X}'.format(variable_data[1]+i, MEMORY[variable_data[1]+i]))
            else:
                raise NotImplementedError('can\'t display {0}'.format(variable_data))
            
    # clear traces
    traces = collections.OrderedDict()




#==============================================================================
# function
#==============================================================================
def initialize():
    # clear program counter and opcode
    PC = 0x200      
    OPCODE = 0    

    # clear register
    I = 0
    for i in range(16):
        V[i] = 0

    # clear stack
    STACK = []

    # reset timer
    DT = 0
    ST = 0

    # clear keyboard
    for i in range(16):
        KEYBOARD[i] = 0

    # clear screen
    for y in range(32):
        for x in range(64):
            SCREEN[y][x] = 0

    m = mmap.mmap(-1, 64*32, 'SCREEN')
    for y in range(32):
        for x in range(64):
            m.write(b'\x00')
    m.close()

    # load font sprites to memory address 0x0000
    # font sprites contains value 0 to F
    # take font 3 as an example
    # ------------------------------
    #             Binary         Hex
    # ------------------------------
    # ****      11110000        0xF0
    #    *      00010000        0x10
    # ****      11110000        0xF0
    #    *      10010000        0x10
    # ****      11110000        0xF0
    font_sprites = [0xF0, 0x90, 0x90, 0x90, 0xF0, #0
                    0x20, 0x60, 0x20, 0x20, 0x70, #1
                    0xF0, 0x10, 0xF0, 0x80, 0xF0, #2
                    0xF0, 0x10, 0xF0, 0x10, 0xF0, #3
                    0x90, 0x90, 0xF0, 0x10, 0x10, #4
                    0xF0, 0x80, 0xF0, 0x10, 0xF0, #5
                    0xF0, 0x80, 0xF0, 0x90, 0xF0, #6
                    0xF0, 0x10, 0x20, 0x40, 0x40, #7
                    0xF0, 0x90, 0xF0, 0x90, 0xF0, #8
                    0xF0, 0x90, 0xF0, 0x10, 0xF0, #9
                    0xF0, 0x90, 0xF0, 0x90, 0x90, #A
                    0xE0, 0x90, 0xE0, 0x90, 0xE0, #B
                    0xF0, 0x80, 0x80, 0x80, 0xF0, #C
                    0xE0, 0x90, 0x90, 0x90, 0xE0, #D
                    0xF0, 0x80, 0xF0, 0x80, 0xF0, #E
                    0xF0, 0x80, 0xF0, 0x80, 0x80  #F
                   ]
    for i in range(len(font_sprites)):
        MEMORY[i] = font_sprites[i]



    
def load_game():
    # load game into memory
    game_filepath = sys.argv[1]
    with open(game_filepath, 'rb') as f:
        data = f.read()
        for i, byte in enumerate(data):
            # Because PC was reset to 0x200, we had to load game to memory address 0x200
            MEMORY[0x200+i] = byte




def emulate():
    initialize()
    load_game()
    while True:
        emulate_cycle()






def emulate_cycle():
    # record time
    emulate_cycle_begin_time = time.clock()

    # fetch opcode
    # The opcode is 2 bytes long while memory is 1 byte long, so we have to take 2 bytes from memory
    global OPCODE
    OPCODE = MEMORY[PC]<<8 | MEMORY[PC+1]

    # decode opcode
    instruction = decode_opcode()

    # execute opcode
    execute_opcode(instruction)

    # move SCREEN to a shared memory
    m = mmap.mmap(-1, 64*32, 'SCREEN')
    for y in range(32):
        for x in range(64):
            if SCREEN[y][x] == 0:
                m.write(b'\x00')
            else:
                m.write(b'\x01')
    m.flush()
    m.close()

    # prevent from emulating too fast
    # According to google, Chip8 doesn't have an actual clock speed, but something around 512KHz or higher should be far more than sufficient.
    # Well, since this emulator runs only 50 HZ on my computer and i can still see the item move, i think 512 HZ is enough.
    clock_rate = 512
    passed_time = time.clock() - emulate_cycle_begin_time
    if passed_time < 1/clock_rate:
        time.sleep(1/clock_rate - passed_time)

    # decrease DT and ST if needed(60HZ)
    global DT, ST, time_slice
    passed_time = time.clock() - emulate_cycle_begin_time + time_slice
    passed_hz = int(passed_time // (1/60))
    time_slice = passed_time % (1/60)
    if passed_hz >= 1:
        DT = DT - passed_hz if DT > passed_hz else 0
        ST = ST - passed_hz if ST > passed_hz else 0

    # To see how slow the emulator is
#    print('CLOCK_RATE: {0} HZ'.format(int(1/passed_time)))




def decode_opcode():
    # This function will try to find the function that can execute the opcode  

    # The order of the instruction_set need to be set carefully.
    # For example, if 0NNN stands before 00EE in instruction set, opcode 00EE will be decoded to instruction 0NNN since it doesn't violate the rule.
    # The instruction set is a little different in words in each website. I choose the website that has the shortest explanation.
    # By the way, if you can't understand the explanation of an instruction, just try another website that has CHIP-8 instruction set.
    # I can't figure out how to accomplish the instruction DXYN from WIKI for a while until i visit another website.
    instruction_set = ['00E0', '00EE', '0NNN', 
                       '1NNN', 
                       '2NNN',
                       '3XKK', 
                       '4XKK', 
                       '5XY0', 
                       '6XKK', 
                       '7XKK', 
                       '8XY0', '8XY1', '8XY2', '8XY3', '8XY4', '8XY5', '8XY6', '8XY7', '8XYE', 
                       '9XY0', 
                       'ANNN', 
                       'BNNN', 
                       'CXKK', 
                       'DXYN', 
                       'EX9E', 'EXA1', 
                       'FX07', 'FX0A', 'FX15', 'FX18', 'FX1E', 'FX29', 'FX33', 'FX55', 'FX65']

    # match instruction byte by byte
    for instruction in instruction_set:
        match = True
        # Match If instruction and opcode has identical hex digit parts(0123456789ABCDEF) 
        # example:
        # Instruction 6XKK has only one 6 that is hex digit, so every opcode that starts with 6 would match instruction 6XKK
        # Instruction FX29 has three hex digits F, 2, 9, so opcode F029, F129, FF29 would match instruction FX29, while opcode F020, F021, F022 would not.

        # match order from left to right
        if instruction[0] in string.hexdigits: 
            if instruction[0] != format(get_byte(OPCODE, 3), 'X'):
                match = False
        if instruction[1] in string.hexdigits: 
            if instruction[1] != format(get_byte(OPCODE, 2), 'X'):
                match = False
        if instruction[2] in string.hexdigits: 
            if instruction[2] != format(get_byte(OPCODE, 1), 'X'):
                match = False
        if instruction[3] in string.hexdigits: 
            if instruction[3] != format(get_byte(OPCODE, 0), 'X'):
                match = False

        if match:
            return instruction

    # no match
    raise NotImplementedError('unknown opcode {0:04X}'.format(OPCODE))




def execute_opcode(instruction):
    instruction_function_name = 'instruction_{0}'.format(instruction)
    if instruction_function_name in globals():
        instruction_function = globals()[instruction_function_name]

        # print debug information
        print('-'*80)
        print_opcode()
        print('INSTRUCTION: ', end='')

        # execute instruction
        instruction_function()

        # print trace information
        print_trace()
    else:
        raise NotImplementedError('function {0}() is not coded yet'.format(instruction_function_name))




def get_byte(source, reverse_index):
    # Get one byte from the source by reverse_index. For example, get_byte(0x5678, 2) will return 0x6
    # The reverse_index starts at 0 and is ordered from right to left. I don't use index because the source is not ensured with fixed size
    mask = 0xF << reverse_index*4
    return (source & mask) >> reverse_index*4




def get_bit(source, reverse_index):
    mask = 0x1 << reverse_index
    return (source & mask) >> reverse_index




#==============================================================================
# main
#==============================================================================
if __name__ == '__main__':
    emulate()



from model import *

"""
Decoder

    Opcode Table:

    FXYXYV00

    F = Function to call
    X = Row
    Y = Col
    V = Value

    AXY00000 - Shifts value at XY to the top of the list
    BXYXY000 - Adds value of first XY to the value of the second XY sets the value to the second XY
    CXYXY000 - Subs value of first XY to the value of the second XY sets the value to the second XY
    DXY00VV0 - Adds value of V to the value at XY
    EXY00VV0 - Subs value at XY by the value of V and sets it to the value at XY
    FXY00000 - Keeps the value at XY 

    1XY00000 - Swaps value 10s and 1s place

"""
instruction_set = ['AXY00000', 'BXYXY000']

OPCODE = 0
OPFUNCTION = 0
OPCOORDINATE_ONE = 0
OPCOORDINATE_TWO = 0
OPVALUE = 0

def clear_opcode(opcode):
    global OPCODE
    OPCODE = 0

def set_opcode(opcode):
    global OPCODE
    OPCODE = opcode
    print('Set OPCODE to:    {0}'.format(hex(opcode)))

def set_function_code():
    global OPFUNCTION
    OPFUNCTION = (OPCODE & 0xF0000000) >> 28

def set_coordinate_one():
    global OPCOORDINATE_ONE
    OPCOORDINATE_ONE = (OPCODE & 0x0FF00000) >> 20

def set_coordinate_two():
    global OPCOORDINATE_TWO
    OPCOORDINATE_TWO = (OPCODE & 0x000FF000) >> 12

def set_value():
    global OPVALUE
    OPVALUE = (OPCODE & 0x00000FF0) >> 4

def instruction_AXY00000():
    pass

def instruction_BXYXY000():
    pass

def decode_opcode():
    # print(hex(op_func), hex(op_coordinate_1), hex(value))
    set_function_code()
    set_coordinate_one()
    set_coordinate_two()
    set_value()
        # if op_func == 0xA0000000:
        #     pass

def display_op_status():
    print()
    print('OPCODE:          ', hex(OPCODE))
    print('OPFUNCTION:      ', hex(OPFUNCTION))
    print('OPCOORDINATE_ONE:', hex(OPCOORDINATE_ONE))
    print('OPCOORDINATE_TWO:', hex(OPCOORDINATE_TWO))
    print('OPVALUE:         ', hex(OPVALUE))
    print()

set_opcode(0xa1234567)
decode_opcode()
display_op_status()
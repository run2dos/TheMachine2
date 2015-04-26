# -*- coding: utf-8 -*-

"""
Encoder

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
temp_instruction = ['shift', 'A', '9', 'B', '7']

encoded_opcode = 0x00000000

instruction_set = {'shift' : 0xA0000000, 'addv' : 0xB0000000}

instruction_with_second_XY = [0xB0000000, 0xC0000000]

hex_set = {'A' : 10, 'B' : 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19}



def encode_func_to_opcode(list_args):
    function = list_args[0]

    if function in instruction_set:
        function_opcode = instruction_set[function]
        return instruction_set[function]
    else:
        raise NotImplementedError('unknown instruction {0}'.format(function))

def encode_first_XY(list_args, opcode_): # must add exception for numbers outside of min and max
    x = int(hex_set[list_args[1]] - 10) << (6 * 4)
    y = int(list_args[2]) << (5 * 4)
    return opcode_ | (x | y)


def encode_second_XY(list_args, opcode_):
    x = int(hex_set[list_args[3]] - 10) << (4 * 4)
    y = int(list_args[4]) << (3 * 4)
    return opcode_ | (x | y)


def encode(list_args, takes_second_XY = False):
    opcode = encode_func_to_opcode(list_args)
    opcode = encode_first_XY(list_args, opcode)

    if opcode & 0xF0000000 in instruction_with_second_XY:
        # takes_second_XY = True
        print('takes second XY')
        try:
            opcode = encode_second_XY(list_args, opcode)
        except IndexError as e:
            print(e)

    # print(hex(opcode))
    return opcode
    
def main():
    # encoded_opcode = encode_func_to_opcode(temp_instruction)
    # encode_first_XY(temp_instruction)
    print(hex(encode(temp_instruction)))

    # print(hex(encoded_opcode))
if __name__ == '__main__':
    main()
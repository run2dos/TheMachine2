# -*- coding: utf-8 -*-
from encoder import encode

user_arg = ''

user_arg1 = 'shift'
user_arg2 = 'A'
user_arg3 = '9'

def parse(*args):
    arg_list = []
    for _, arg in enumerate(args[0]):
        arg_list.append(arg)
    return arg_list

# l = parse(user_arg1, user_arg2, user_arg3)
print('shift X Y, addv X1 Y1 X2 Y2')
usr_in = input('Make a move! ')
l = parse(usr_in.split())
encoded_arg = encode(l)



print(hex(encoded_arg))
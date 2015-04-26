#!py -3
# -*- coding: utf-8 -*-
# @author: ResolaQQ
# @version: 201502042014
# @english blog: http://resolaqqen.blogspot.tw/2015/01/my-chip-8-emulator-written-in-python.html
# @chinese blog: http://resolaqq.blogspot.tw/2014/10/my-chip-8-emulator-written-in-python.html
import mmap
import time
import os
import tkinter




#==============================================================================
# global
#==============================================================================
m = mmap.mmap(-1, 16, 'KEYBOARD')




# Most chip-8 programs are written for a 16-key hex keyboard with  
# following layout: 
# 
#  1 2 3 C                                               7 8 9 / 
#  4 5 6 D    This keyboard is emulated on the HP48SX    4 5 6 * 
#  7 8 9 E    using the following keys:                  1 2 3 - 
#  A 0 B F                                               0 . _ + 
translation_table = {'1': 0x1,
                     '2': 0x2,
                     '3': 0x3,
                     '4': 0xC,
                     'q': 0x4,
                     'w': 0x5,
                     'e': 0x6,
                     'r': 0xD,
                     'a': 0x7,
                     's': 0x8,
                     'd': 0x9,
                     'f': 0xE,
                     'z': 0xA,
                     'x': 0x0,
                     'c': 0xB,
                     'v': 0XF}


    

#==============================================================================
# function
#==============================================================================
def on_key_press(event):
    m.seek(0)
    data = bytearray(m.read())
    data[translation_table[event.keysym]] = 1
    m.seek(0)
    m.write(bytes(data))
    m.flush()
    os.system('cls')
    for i in range(16):
        print(data[i], end='')
    print()




def on_key_release(event):
    m.seek(0)
    data = bytearray(m.read())
    data[translation_table[event.keysym]] = 0
    m.seek(0)
    m.write(bytes(data))
    m.flush()
    os.system('cls')
    for i in range(16):
        print(data[i], end='')
    print()




#==============================================================================
# main
#==============================================================================
if __name__ == '__main__':

    root = tkinter.Tk()
    root.bind('<KeyPress>', on_key_press)    
    root.bind('<KeyRelease>', on_key_release)

    root.mainloop()


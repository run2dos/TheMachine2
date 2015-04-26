#!py -3
# -*- coding: utf-8 -*-
# @author: ResolaQQ
# @version: 201502042014
# @english blog: http://resolaqqen.blogspot.tw/2015/01/my-chip-8-emulator-written-in-python.html
# @chinese blog: http://resolaqq.blogspot.tw/2014/10/my-chip-8-emulator-written-in-python.html
import mmap
import time
import os




if __name__ == '__main__':
    # open shared memory
    m = mmap.mmap(-1, 64*32, 'SCREEN')
    while True:
        # reset shared memory pointer 
        m.seek(0)

        # read screen data
        data = m.read(64*32)

        # clear screen
        os.system('cls')

        # output screen
        for y in range(32):
            for x in range(64):
                if data[y*64+x] == 0:
                    print(' ', end='')
                else:
                    print('#', end='')
            # change line
            print()

        # 24 fps
        time.sleep(1/24)


# -*- coding: utf-8 -*-

Target = [0 for x in range(5)]
#Target = [17,2,3,4,6]
Matrix = [[0 for x in range(5)] for x in range(10)]
Line = ['A','B','C','D','E','F','G','H','I','J']


def display_matrix(clear_screen = False):
    """Displays the current status of the Matrix"""
    global Matrix
    if clear_screen:
        print("\n" * 100)
    print('T {:02d} {:02d} {:02d} {:02d} {:02d}'.format(Target[0], Target[1], Target[2], Target[3], Target[4]))
    print('   1  2  3  4  5')
    for i, tile in enumerate(Matrix):
        print('{:s} {:02d} {:02d} {:02d} {:02d} {:02d}'.format(Line[i], tile[0], tile[1], tile[2], tile[3], tile[4]))
    print()

def get_tile_value(row, col):
    return Matrix[row][col-1]

def set_tile_value(row, col, value):
    Matrix[row][col-1] = value

def shift_number_to_top(row, col):
    value = get_tile_value(row, col)
    set_tile_value(0, col, value)

def main():
    display_matrix()
    set_tile_value(9, 1, 9)
    display_matrix()
    shift_number_to_top(9, 1)
    display_matrix()

if __name__ == '__main__':
    main()
from globalss.colors import *
from player.character import *
from globalss.globals import *

def divide_line():
    print(f'{CYAN}--------------------------------------------------------------------------------------------{RESET}')

def print_map_2D():
    # Print col number
    print("   ", end="")
    for col in range(Stats.MAP_SIZE.x):
        print(col+1, end="")
        if col < 9:
            print('  ', end="")
        else:
            print(' ', end="")
    print()
    
    for row in range(Stats.MAP_SIZE.y):
        # print row number
        print(row+1, end="")
        if row < 9:
            print('  ', end="")
        else:
            print(' ', end="")
        
        # print map 
        for col in range(Stats.MAP_SIZE.x):
            if (Stats.MAP[row][col] == '.'):
                print('.', end="")
            elif (col, row) in Stats.COLOR_COORD:
                print(f"{Stats.COLOR_COORD[(col, row)]}{Stats.MAP[row][col]}{RESET}", end="")
            else:
                print(f"{Stats.MAP[row][col]}", end="")
            print("  ", end="")
        print()
    
def check_bounds(pos):
    if (pos.x >= Stats.MAP_SIZE.x) or (pos.x < 0) or (pos.y >= Stats.MAP_SIZE.y) or (pos.y < 0):
        return False
    else:
        return True

def dump_info():
    for str in Stats.DUMPS:
        print(str)

def clear_dump():
    Stats.DUMPS.clear()
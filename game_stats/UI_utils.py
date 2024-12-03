from globalss.colors import *
from player.character import *
from globalss.globals import *

def divide_line():
    print(f'{CYAN}--------------------------------------------------------------------------------------------{RESET}')

def print_map_2D():
    for row in range(Stats.MAP_SIZE.y):
        for col in range(Stats.MAP_SIZE.x):
            if (Stats.MAP[row][col] == '.'):
                print('.', end="")
            elif (col, row) in Stats.COLOR_COORD:
                print(f"{Stats.COLOR_COORD[(col, row)]}{Stats.MAP[row][col]}{RESET}", end="")
            else:
                print(f"{Stats.MAP[row][col]}", end="")
        print("\n",end="")
        
from globalss.colors import *
from player.character import *
from globalss.globals import *

def divide_line():
    print(f'{CYAN}--------------------------------------------------------------------------------------------{RESET}')

def print_map_2D(map=None, color_coord=None):
    if map is None:
        map = Stats.MAP
    if not color_coord:
        color_coord = Stats.COLOR_COORD
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

            if (col, row) in color_coord:
                print(f"{color_coord[(col, row)]}{map[row][col]}{RESET}", end="")
            else:
                print(f"{map[row][col]}", end="")
            print("  ", end="")
        print()

def print_range_map(character):
    range_map = [["." for _ in range(Stats.MAP_SIZE.x)] for _ in range(Stats.MAP_SIZE.y)]
    range_map[character.pos.y][character.pos.x] = character.symbol
    color_coord = {}
    color_coord[(character.pos.x, character.pos.y)] = character.color
    for row in range(Stats.MAP_SIZE.y):
        for col in range(Stats.MAP_SIZE.x):
            if Position(col, row) != character.pos and abs(col - character.pos.x) + abs(row - character.pos.y) <= character.range:
                color_coord[(col, row)] = GREEN
                range_map[row][col] = '-'
    
    print_map_2D(map=range_map, color_coord=color_coord)

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
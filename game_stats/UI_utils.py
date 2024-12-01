from globalss.colors import *
from player.character import *
from globalss.globals import *

def divide_line():
    print(f'{CYAN}--------------------------------------------------------------------------------------------{RESET}')

def print_map():
    """
    Currently only supports 2 players
    """
    left_player = Stats.PLAYER_LIST[0]
    right_player = Stats.PLAYER_LIST[1]

    for player in Stats.PLAYER_LIST:
        if player.pos < left_player.pos:
            right_player = left_player
            left_player = player
        elif player.pos > left_player.pos:
            right_player = player

    left_lines = int(((Stats.MAP_SIZE - 1) / 2) + left_player.pos)
    center_lines = int(abs(left_player.pos - right_player.pos) - 1)
    right_lines = int(((Stats.MAP_SIZE - 1) / 2) - right_player.pos)
    
    print(f'_'*left_lines + f'{left_player.color}{left_player.name}{RESET}' + f'_'*center_lines + f'{right_player.color}{right_player.name}{RESET}' + f'_'*right_lines)

def print_map_2D():
    for row in range(Stats.MAP_SIZE.y):
        for col in range(Stats.MAP_SIZE.x):
            print(Stats.MAP[row][col], end="")
        print("\n",end="")
        
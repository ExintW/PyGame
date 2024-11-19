from player.player import *
from globals.globals import *
from globals.colors import *

def check_end():
    """
    Returns 1 if game has ended
    """
    for player in PLAYER_LIST:
        if player.health <= 0:
            print(f'{RED}{player.name} has been defeated!{RESET}')
            return 1
    
    return 0

def print_players_stats():
    for player in PLAYER_LIST:
        player.print_stat()
from player.character import *
from globalss.globals import *
from globalss.colors import *

def check_end():
    """
    Returns 1 if game has ended
    """
    for player in Stats.PLAYER_LIST:
        if len(player.avail_characters) == 0:
            print(f'{RED}{player.name} has been defeated!{RESET}')
            return 1
    
    return 0

def print_players_stats():
    for player in Stats.PLAYER_LIST:
        player.print_char_stat()

def init_map():
    Stats.MAP = [["." for _ in range(Stats.MAP_SIZE.x)] for _ in range(Stats.MAP_SIZE.y)]
    for p in Stats.PLAYER_LIST:
        for c in p.avail_characters:
            Stats.MAP[c.pos.y][c.pos.x] = c.symbol

def check_characters():
    for p in Stats.PLAYER_LIST:
        for c in p.avail_characters.copy():
            if c.health <= 0:
                p.avail_characters.remove(c)
                del p.sym_to_char_map[c.symbol]

def init_lists_and_maps(p1, p2):
    Stats.PLAYER_LIST.append(p1)
    Stats.PLAYER_LIST.append(p2)
    Stats.NAME_TO_PLAYER_MAP[p1.name] = p1
    Stats.NAME_TO_PLAYER_MAP[p2.name] = p2
    
    p1_map = {}
    p2_map = {}
    for c in p1.characters:
        p1_map[c.symbol] = c
    for c in p2.characters:
        p2_map[c.symbol] = c
    p1.sym_to_char_map = p1_map
    p2.sym_to_char_map = p2_map
    
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
    Stats.CHAR_MAP = [[None for _ in range(Stats.MAP_SIZE.x)] for _ in range(Stats.MAP_SIZE.y)]
    Stats.COLOR_COORD = {}
    for effect in Stats.MAP_EFFECT_LIST:
        Stats.MAP[effect.pos.y][effect.pos.x] = effect.symbol
        if effect not in Stats.EFFECT_MAP[effect.pos.y][effect.pos.x]:
            Stats.EFFECT_MAP[effect.pos.y][effect.pos.x].append(effect)
        if effect.from_player is not None:
            Stats.COLOR_COORD[(effect.pos.x, effect.pos.y)] = effect.from_player.color
    
    for p in Stats.PLAYER_LIST:
        for c in p.avail_characters:
            Stats.MAP[c.pos.y][c.pos.x] = c.symbol
            Stats.COLOR_COORD[(c.pos.x, c.pos.y)] = p.color
            Stats.CHAR_MAP[c.pos.y][c.pos.x] = c
            if Stats.EFFECT_MAP[c.pos.y][c.pos.x] is not None:
                for eff in Stats.EFFECT_MAP[c.pos.y][c.pos.x]:
                    if eff.duration > 0:
                        c.map_effects.add(eff)
    
def apply_map_effects():
    for p in Stats.PLAYER_LIST:
        for c in p.avail_characters:
            if Stats.EFFECT_MAP[c.pos.y][c.pos.x] != None:
                for eff in Stats.EFFECT_MAP[c.pos.y][c.pos.x].copy():
                    if not eff.apply(c):
                        c.map_effects.remove(eff)
                        
    for eff in Stats.MAP_EFFECT_LIST.copy():
        eff.duration -= 1
        if eff.duration <= 0:
            Stats.MAP_EFFECT_LIST.remove(eff)
            Stats.EFFECT_MAP[eff.pos.y][eff.pos.x].remove(eff)
        

def check_characters():
    for p in Stats.PLAYER_LIST:
        for c in p.avail_characters.copy():
            if c.health <= 0:
                p.avail_characters.remove(c)
                del p.sym_to_char_map[c.symbol]
                Stats.DUMPS.append(f'{RED}{c.name} has been defeated!{RESET}')

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
    
    Stats.EFFECT_MAP = [[[None for _ in range(0)] for _ in range(Stats.MAP_SIZE.x)] for _ in range(Stats.MAP_SIZE.y)]
   
from player.character import *
from globalss.globals import *
from globalss.colors import *
from mechanics.projectiles import *
from mechanics.buffs import *

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
    Stats.PROJ_MAP = [[[None for _ in range(0)] for _ in range(Stats.MAP_SIZE.x)] for _ in range(Stats.MAP_SIZE.y)]
    Stats.COLOR_COORD = {}
    for effect in Stats.MAP_EFFECT_LIST:
        Stats.MAP[effect.pos.y][effect.pos.x] = effect.symbol
        if effect not in Stats.EFFECT_MAP[effect.pos.y][effect.pos.x]:
            Stats.EFFECT_MAP[effect.pos.y][effect.pos.x].append(effect)
        if effect.from_player is not None:
            Stats.COLOR_COORD[(effect.pos.x, effect.pos.y)] = effect.from_player.color
    
    for proj in Stats.PROJECTILE_LIST:
        Stats.MAP[proj.pos.y][proj.pos.x] = proj.symbol
        if proj not in Stats.PROJ_MAP[proj.pos.y][proj.pos.x]:
            Stats.PROJ_MAP[proj.pos.y][proj.pos.x].append(proj)
        if proj.from_character is not None:
            Stats.COLOR_COORD[(proj.pos.x, proj.pos.y)] = proj.from_character.color
            
    for p in Stats.PLAYER_LIST:
        for c in p.avail_characters:
            Stats.MAP[c.pos.y][c.pos.x] = c.symbol
            Stats.COLOR_COORD[(c.pos.x, c.pos.y)] = p.color
            Stats.CHAR_MAP[c.pos.y][c.pos.x] = c
            if Stats.EFFECT_MAP[c.pos.y][c.pos.x] is not None:
                for eff in Stats.EFFECT_MAP[c.pos.y][c.pos.x]:
                    if eff.duration > 0:
                        c.map_effects.add(eff)
            check_mov_pen(c)

def check_mov_pen(character):
    for p in Stats.PLAYER_LIST:
        if p == character.player:
            continue
        flag = False
        for c in p.avail_characters:
            if abs(character.pos.x - c.pos.x) + abs(character.pos.y - c.pos.y) == 1:
                character.mov_penalty = True
                flag = True
        if not flag:
            character.mov_penalty = False
                
    
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

def update_projectiles():
    for proj in Stats.PROJECTILE_LIST.copy():
        if proj.move():
            Stats.PROJECTILE_LIST.remove(proj)
            

def check_characters():
    for p in Stats.PLAYER_LIST:
        for c in p.avail_characters.copy():
            if c.health <= 0:
                p.avail_characters.remove(c)
                del p.sym_to_char_map[c.symbol]
                Stats.DUMPS.append(f'{RED}{c.name} has been defeated!{RESET}')

def check_special_mechanics(character):
    # check sheath
    if hasattr(character, 'sheathed'):
        if character.sheath_counter > 0:
            character.sheath_counter -= 1

def check_init_rage():
    Stats.CHAR_COPY_LIST_FOR_RAGE.clear()
    for p in Stats.PLAYER_LIST:
        for c in p.avail_characters:
            if c.rage is None:
                continue
            
            # append copy of init character stat into global list
            Stats.CHAR_COPY_LIST_FOR_RAGE.append(copy.deepcopy(c))
                
            # check if rage def buff exists
            buff_exist = False
            for buff in c.buff[Buff_Type.DEF_BUFF].copy():
                if buff.name == RAGE_DEF_BUFF_NAME:
                    buff_exist = True
                    if c.rage < int(c.max_rage/2):
                        c.buff[Buff_Type.DEF_BUFF].remove(buff)
                    
            # if buff does not exist and rage > int(c.max_rage/2): add buff
            rage_buff = Buff(name=RAGE_DEF_BUFF_NAME, value=c.rage_def_buff_value, type=Buff_Type.DEF_BUFF, duration=99)
            if not buff_exist and c.rage >= int(c.max_rage/2):
                c.buff[Buff_Type.DEF_BUFF].append(rage_buff)
            
            # remove max rage buffs if not in max rage
            if c.in_max_rage == False:
                for type, list in c.buff.items():
                    for b in list.copy():
                        if b.name == MAX_RAGE_BUFF_NAME:
                            list.remove(b)
            
            if c.rage == c.max_rage:
                if c.in_max_rage == False:
                    c.in_max_rage = True
                    c.max_rage_counter = c.max_rage_duration
                    c.buff[Buff_Type.DEF_BUFF].append(Buff(MAX_RAGE_BUFF_NAME, c.rage_def_buff_value, type=Buff_Type.DEF_BUFF, duration=99))
                    c.buff[Buff_Type.ATK_BUFF].append(Buff(MAX_RAGE_BUFF_NAME, c.rage_atk_buff_value, type=Buff_Type.ATK_BUFF, duration=99))
                    c.buff[Buff_Type.RANGE_BUFF].append(Buff(MAX_RAGE_BUFF_NAME, c.rage_range_buff_value, type=Buff_Type.RANGE_BUFF, duration=99))
                    c.buff[Buff_Type.BOOST_BUFF].append(Buff(MAX_RAGE_BUFF_NAME, c.rage_boost_buff_value, type=Buff_Type.BOOST_BUFF, duration=99))
                    c.health += int((c.max_health - c.health) / 2)
                    Stats.DUMPS.append(f'{CYAN}MAX Rage: {c.name} health + {int((c.max_health - c.health) / 2)}{RESET}')
                    if c.health > c.max_health:
                        c.health = c.max_health
                else:
                    if c.max_rage_counter == 1:
                        c.in_max_rage = False
                        c.max_rage_counter = 0
                        c.rage = 0
                        for type, list in c.buff.items():
                            for b in list.copy():
                                if b.name == MAX_RAGE_BUFF_NAME:
                                    list.remove(b)
                        for buff in c.buff[Buff_Type.DEF_BUFF].copy():
                            if buff.name == RAGE_DEF_BUFF_NAME:
                                if c.rage < int(c.max_rage/2):
                                    c.buff[Buff_Type.DEF_BUFF].remove(buff)
                        continue
                    else:
                        c.max_rage_counter -= 1
                
                
def check_end_rage():   # decrements the rage if no attack or damage taken
    for p in Stats.PLAYER_LIST:
        for c in p.avail_characters:
            if c.rage is None:
                continue
            c_init = None
            for cc in Stats.CHAR_COPY_LIST_FOR_RAGE:
                if cc.name == c.name:
                    c_init = cc
            if c_init.rage == c.rage and c.rage > 0 and not c.in_max_rage:       # rage has changed: no decrement needed
                c.rage -= 1
                Stats.DUMPS.append(f"{CYAN}{c.name}: rage - 1{RESET}")  
                
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
    
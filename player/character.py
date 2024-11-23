from globals.globals import *
from globals.colors import *

class Character:
    def __init__(self, player=None, name=None, profession=None, pos=None, abilities=None):
        self.player = player
        self.name = name
        self.profession = profession
        self.pos = pos
        self.color = player.color
        self.abilities = abilities
        self.buff = {
            Buff_Type.ATK_BUFF : [],    # affects atk dmg
            Buff_Type.ATK_DEBUFF : [],
            Buff_Type.DEF_BUFF : [],    # affects dmg received
            Buff_Type.DEF_DEBUFF : [],
            Buff_Type.BOOST_BUFF : [],  # affects movements
            Buff_Type.BOOST_DEBUFF : [],
            Buff_Type.RANGE_BUFF : [],  # affects attack and ability range
            Buff_Type.RANGE_DEBUFF : [],
        }
        
        self.range = 0
        self.damage = 0
        self.health = 0
        self.max_health = 0
        self.mobility = 0
        self.mana = 0
        self.max_mana = 0    
    
    def print_stat(self):
        print(f'{PURPLE}Character: {self.profession}{RESET}')
        print(f'\t{GREEN}health: {self.health}{RESET}', f'{BG_GREEN} {RESET}'*self.health + f'{BG_DARK_GREEN} {RESET}'*(self.max_health - self.health))
        print(f'\t{BLUE}mana: {self.mana}{RESET}', f'{BG_BLUE} {RESET}'*self.mana + f'{BG_DARK_BLUE} {RESET}'*(self.max_mana - self.mana))
        print('\trange:', self.range)
        print(f'\t{YELLOW}mobility: {self.mobility}{RESET}')
        print(f'\t{RED}damage: {self.damage}{RESET}')
        print(f'\t{PURPLE}abilities: {(lambda lst : [abil.name for abil in lst])(self.abilities)}{RESET}')
        self.print_buffs()
        print('\tpos:', self.pos)
        
    def attack(self, target, dmg_f=0):     
        if target == self:
            print(f'{CYAN}Cannot attack self!{RESET}')
            return False
        elif abs(self.pos.x - target.pos.x) + abs(self.pos.y - target.pos.y) <= self.range + buff_range(self):
            dmg = apply_dmg_buff(self, target, dmg_f)
            apply_range_buff(self)
            target.health -= dmg
            print(f'{CYAN}Attack is successful: {target.name}: health - {dmg}{RESET}')
            return True
        else:
            print(f'{CYAN}Not enough range!{RESET}')
            return False
    
    def move(self, dist, forced=False):
        cur_mobil = self.mobility
        if not forced:
            cur_mobil += calculate_move(self)
        if abs(self.pos + dist) > (MAP_SIZE - 1) / 2:
            print(f'{RED}Invalid move distance: Out of bound!{RESET}')
            return False
        elif (abs(dist) <= cur_mobil and dist != 0) or forced:
            if not forced:
                apply_boost_buff(self)
            self.pos += dist
            flag = True
            while (flag):
                # for bouncing effect
                for p in PLAYER_LIST:
                    if p != self and self.pos == p.pos:
                        self.pos += dist
                        flag = True
                        break
                    else:
                        flag = False
                        
            print(f'{CYAN}{self.name} moved to {self.pos}{RESET}')
            return True
        else:
            print(f'{RED}Invalid move distance!{RESET}')
            return False
    
    def print_buffs(self):
        for buff_type, list in self.buff.items():
            if len(list) > 0:
                print(f'\t{GREEN}{buff_type.name}: {(lambda lst : [buff.name for buff in lst])(list)}{RESET}')

    
def apply_dmg_buff(source, target, dmg=0):
    if dmg == 0:
        damage = source.damage
    else:
        damage = dmg
    
    for buff in source.buff[Buff_Type.ATK_BUFF].copy():
        damage += buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.ATK_BUFF].remove(buff)
    for buff in source.buff[Buff_Type.ATK_DEBUFF].copy():
        damage -= buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.ATK_DEBUFF].remove(buff)
    for buff in target.buff[Buff_Type.DEF_BUFF].copy():
        damage -= buff.apply()
        if buff.duration < 1:
            target.buff[Buff_Type.DEF_BUFF].remove(buff)
    for buff in target.buff[Buff_Type.DEF_DEBUFF].copy():
        damage += buff.apply()
        if buff.duration < 1:
            target.buff[Buff_Type.DEF_DEBUFF].remove(buff)
    
    return damage

def calculate_move(source):
    dist = 0
    for buff in source.buff[Buff_Type.BOOST_BUFF].copy():
        dist += buff.value
    for buff in source.buff[Buff_Type.BOOST_DEBUFF].copy():
        dist -= buff.value
    return dist

def apply_boost_buff(source):
    for buff in source.buff[Buff_Type.BOOST_BUFF].copy():
        buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.BOOST_BUFF].remove(buff)
    for buff in source.buff[Buff_Type.BOOST_DEBUFF].copy():
        buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.BOOST_DEBUFF].remove(buff)
            
def buff_range(source):
    range = 0
    for buff in source.buff[Buff_Type.RANGE_BUFF].copy():
        range += buff.value
    for buff in source.buff[Buff_Type.RANGE_DEBUFF].copy():
        range -= buff.value
    return range

def apply_range_buff(source):
    for buff in source.buff[Buff_Type.RANGE_BUFF].copy():
        buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.RANGE_BUFF].remove(buff)
    for buff in source.buff[Buff_Type.RANGE_DEBUFF].copy():
        buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.RANGE_DEBUFF].remove(buff)
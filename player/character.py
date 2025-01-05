from globalss.globals import *
from globalss.colors import *
from game_stats.UI_utils import check_bounds

class Character:
    def __init__(self, player=None, name=None, profession=None, pos=None, abilities=None, sig_ability=None, range=0, damage=0, max_health=0, mobility=0, max_mana=0, symbol='/', max_rage=None, max_rage_duration=None):
        self.player = player
        self.name = name
        self.profession = profession
        self.pos = pos                  # Position(x, y) @dataclass
        self.color = player.color
        self.abilities = abilities
        self.sig_ability = sig_ability
        self.abnormalities = []
        self.map_effects = set()
        self.channeling = -1
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
        
        self.range = range
        self.damage = damage
        self.health = max_health
        self.max_health = max_health
        self.mobility = mobility
        self.mana = max_mana
        self.max_mana = max_mana   
        self.max_rage = max_rage 
        if max_rage is not None:
            self.rage = 0
            self.max_rage_duration = max_rage_duration
            self.max_rage_counter = 0
            self.in_max_rage = False
        else:
            self.rage = None
            self.max_rage_duration = None
            self.max_rage_counter = None
            self.in_max_rage = None
        
        self.symbol = symbol 
    
    def print_stat(self):
        print(f'{PURPLE}Character: {self.profession}{RESET} ', end='')
        if self.channeling > 0:
            print(f'{YELLOW}CHANNELING ({self.channeling} Rounds left)', end = ' ')
        if hasattr(self, 'sheathed') and self.sheathed:
            if self.sheath_counter > 0:
                print(f'{YELLOW}SHEATHED{RESET}', end=' ')
            else:
                print(f'{YELLOW}SHEATHED (READY){RESET}')
        print()
        print(f'\t{GREEN}health: {self.health}{RESET}', f'{BG_GREEN} {RESET}'*self.health + f'{BG_DARK_GREEN} {RESET}'*(self.max_health - self.health))
        print(f'\t{BLUE}mana: {self.mana}{RESET}', f'{BG_BLUE} {RESET}'*self.mana + f'{BG_DARK_BLUE} {RESET}'*(self.max_mana - self.mana))
        if self.rage is not None:
            print(f'\t{RED}rage: {self.rage}{RESET}', f'{BG_RED} {RESET}'*self.rage + f'{BG_DARK_RED} {RESET}'*(self.max_rage - self.rage))
        if self.in_max_rage is not None and self.in_max_rage:
            print(f'\t{RED}max rage duration: {self.max_rage_counter}{RESET}')
        print('\trange:', self.range)
        print(f'\t{YELLOW}mobility: {self.mobility}{RESET}')
        print(f'\t{RED}damage: {self.damage}{RESET}')
        print(f'\t{BLUE}abilities: {(lambda lst : [abil.name for abil in lst])(self.abilities)}{RESET}')
        if self.sig_ability is not None:
            print(f'\t{YELLOW}signiture ability: {self.sig_ability.name}{RESET}')
        self.print_buffs()
        self.print_abnormalities()
        self.print_map_effects()
        print('\tpos:', self.pos)
        
    def attack(self, target, dmg_f=0):     
        if target == self:
            print(f'{CYAN}Cannot attack self!{RESET}')
            return False
        elif pos_diff(self, target) <= self.range + buff_range(self):
            dmg = apply_dmg_def_buff(self, target, dmg_f)
            apply_range_buff(self)
            if dmg >= 0:
                target.health -= dmg
            if self.rage is not None and self.rage != self.max_rage:
                self.rage += 1
                Stats.DUMPS.append(f'{CYAN}{self.name} rage + 1{RESET}')
            if target.rage is not None and target.rage != target.max_rage:
                target.rage += 1
                Stats.DUMPS.append(f'{CYAN}{target.name} rage + 1{RESET}')
            if self.in_max_rage is not None and self.in_max_rage:
                self.health += int(dmg/2)
                if self.health > self.max_health:
                    self.health = self.max_health
                Stats.DUMPS.append(f'{CYAN}{self.name} life steel: health + {int(dmg/2)}{RESET}')
            Stats.DUMPS.append(f'{CYAN}Attack is successful: {target.name}: health - {dmg}{RESET}')
            return True
        else:
            print(f'{CYAN}Not enough range!{RESET}')
            return False
    
    def move(self, del_x, del_y, forced=False):
        cur_mobil = self.mobility
        if not forced:
            cur_mobil += calculate_move(self)
        if (self.pos.x + del_x >= Stats.MAP_SIZE.x) or (self.pos.x + del_x < 0) or (self.pos.y + del_y >= Stats.MAP_SIZE.y) or (self.pos.y + del_y < 0):
            print(f'{RED}Invalid move distance: Out of bound!{RESET}')
            return False
        elif (abs(del_x) + abs(del_y) <= cur_mobil and abs(del_x) + abs(del_y) != 0) or forced:
            if not forced:
                apply_boost_buff(self)
            previous_pos = Position(self.pos.x, self.pos.y)
            self.pos.x += del_x
            self.pos.y += del_y
            
            while (Stats.CHAR_MAP[self.pos.y][self.pos.x] is not None):
                # for bouncing effect
                self.pos.x += del_x
                self.pos.y += del_y
                if not check_bounds(self.pos):
                    self.pos = previous_pos
                    print(f'{RED}Invalid move: out of bounds after bouncing!{RESET}')
                    return False   
            
            Stats.DUMPS.append(f'{CYAN}{self.name} moved to {self.pos}{RESET}')
            self.map_effects.clear()
            return True
        else:
            print(f'{RED}Invalid move distance!{RESET}')
            return False
    
    def print_buffs(self):
        for buff_type, list in self.buff.items():
            if len(list) > 0:
                print(f'\t{GREEN}{buff_type.name}: {(lambda lst : [buff.name for buff in lst])(list)}{RESET}')
    
    def print_abnormalities(self):
        if len(self.abnormalities) == 0:
            return
        print(f"\t{RED}Abnormalities: {RESET}", end="")
        for ab in self.abnormalities:
            print(f"{RED}{ab.name}({ab.duration} Rounds) ", end="")
        print(f"{RESET}")
        
    def print_map_effects(self):
        if len(self.map_effects) == 0:
            return
        print(f"\t{PURPLE}Map Effects: {RESET}", end="")
        for eff in self.map_effects:
            if eff.from_player == None:
                print(f"{RESET}{eff.name}({eff.duration} Rounds) {PURPLE}", end="")
            else:
                print(f"{eff.from_player.color}{eff.name}({eff.duration} Rounds) {RESET}{PURPLE}", end="")
        print(f"{RESET}")
    
    def apply_abnormalities(self, ab_type): # returns true if applied successfully
        if len(self.abnormalities) == 0:
            return False
        flag = False
        for ab in self.abnormalities.copy():
            if ab.type == ab_type:
                if ab.duration > 0:
                    flag = True
                if not ab.apply():  # decrement ab, returns false if duration becomes 0
                    self.abnormalities.remove(ab)
        return flag
    
    def apply_def_buff(self, target, dmg=0):    # for samurai aoe atk
        if dmg == 0:
            damage = self.damage
        else:
            damage = dmg
        
        for buff in target.buff[Buff_Type.DEF_BUFF].copy():
            damage -= buff.apply()
            if buff.duration < 1:
                target.buff[Buff_Type.DEF_BUFF].remove(buff)
        for buff in target.buff[Buff_Type.DEF_DEBUFF].copy():
            damage += buff.apply()
            if buff.duration < 1:
                target.buff[Buff_Type.DEF_DEBUFF].remove(buff)
        
        return damage
    
    def apply_dmg_buff(self, dmg=0):
        if dmg == 0:
            damage = self.damage
        else:
            damage = dmg
        
        for buff in self.buff[Buff_Type.ATK_BUFF].copy():
            damage += buff.apply()
            if buff.duration < 1:
                self.buff[Buff_Type.ATK_BUFF].remove(buff)
        for buff in self.buff[Buff_Type.ATK_DEBUFF].copy():
            damage -= buff.apply()
            if buff.duration < 1:
                self.buff[Buff_Type.ATK_DEBUFF].remove(buff)
        return damage
    
def apply_dmg_def_buff(source, target, dmg=0):
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

def pos_diff(source, target):
    return max(abs(source.pos.x - target.pos.x), abs(source.pos.y - target.pos.y))
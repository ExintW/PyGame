from globalss.globals import *
from globalss.colors import *
from game_stats.UI_utils import check_bounds
from mechanics.abilities import *
from player.player_utils import *

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
        self.channel_counter = -1       # -1 means not channeling
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
        self.mov_penalty = False
        self.symbol = symbol 
    
    def print_stat(self):
        print(f'{PURPLE}Character: {self.profession}{RESET} ', end='')
        if self.channel_counter > 0:
            print(f'{YELLOW}CHANNELING ({self.channel_counter} Rounds left){RESET}', end = ' ')
        if self.sig_ability is not None and self.sig_ability.using:
            print(f'{YELLOW}CASTING ({self.sig_ability.rounds_used} Rounds){RESET}', end = ' ')
        if hasattr(self, 'sheathed') and self.sheathed:
            if self.sheath_counter > 0:
                print(f'{YELLOW}SHEATHED{RESET}', end=' ')
            else:
                print(f'{YELLOW}SHEATHED (READY){RESET}', end=' ')
        if self.mov_penalty:
            print(f'{YELLOW}MOV-PENALTY{RESET}', end=' ')
        print()
        
        # Special count mechanics
        if hasattr(self, 'range_shot_count'):
            print(f'{YELLOW}range shot count: {self.range_shot_count}{RESET}')
        if hasattr(self, 'charges'):
            self.print_special_count(f'{GREEN}✚{RESET}', self.max_charge, self.charges, 1)
        if hasattr(self, 'souls'):
            self.print_special_count(f'🔥', self.max_souls, self.souls)
        if hasattr(self, 'phantom_aegis_count'):
            self.print_special_count(f'{BLUE}⛨{RESET}', self.phantom_aegis_max_count, self.phantom_aegis_count, 1)
            if self.phantom_aegis:
                print(f'\t{YELLOW}PHANTOM AEGIS {RESET}{GREEN}ACTIVE{RESET}{BLUE}⛨{RESET} ')
                
        print(f'\t{GREEN}health: {self.health}{RESET}', f'{BG_GREEN} {RESET}'*int(self.health/10) + f'{BG_DARK_GREEN} {RESET}'*int((self.max_health - self.health)/10))
        print(f'\t{BLUE}mana: {self.mana}{RESET}', f'{BG_BLUE} {RESET}'*self.mana + f'{BG_DARK_BLUE} {RESET}'*(self.max_mana - self.mana))
       
        if self.rage is not None:
            print(f'\t{RED}rage: {self.rage}{RESET}', f'{BG_RED} {RESET}'*self.rage + f'{BG_DARK_RED} {RESET}'*(self.max_rage - self.rage))
        if self.in_max_rage is not None and self.in_max_rage:
            print(f'\t{RED}max rage duration: {self.max_rage_counter}{RESET}')
        
        print('\trange:', self.range, end='')
        if hasattr(self, 'range_shot') and self.range_shot:
            print(f'{YELLOW} RANGE SHOT{RESET}', end='')
        print()
        
        print(f'\t{YELLOW}mobility: {self.mobility}{RESET}')
        print(f'\t{RED}damage: {self.damage}{RESET}')
        
        self.print_abilities()
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
            if hasattr(self, 'range_shot_count'):
                if self.range_shot_count >= 3:
                    self.range_shot = True
                    self.range_shot_count = 0
                else:
                    self.range_shot_count += 1
            if hasattr(target, 'phantom_aegis') and target.phantom_aegis == True:
                if dmg > 0:
                    dmg = 10
                    target.phantom_aegis = False
            if dmg >= 0:
                target.health -= dmg
            if hasattr(self, 'charges'):    # for healer only
                if self.charges < self.max_charge:
                    self.charges += 1
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
        penalty = False
        if self.mov_penalty:
            cur_mobil = 1
            penalty = True
        if not forced and not penalty:
            cur_mobil += calculate_move(self)
        if (self.pos.x + del_x >= Stats.MAP_SIZE.x) or (self.pos.x + del_x < 0) or (self.pos.y + del_y >= Stats.MAP_SIZE.y) or (self.pos.y + del_y < 0):
            print(f'{RED}Invalid move distance: Out of bound!{RESET}')
            return False
        elif (abs(del_x) + abs(del_y) <= cur_mobil and abs(del_x) + abs(del_y) != 0) or forced:
            if not forced and not penalty:
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

    def print_abilities(self):
        print(f"\t{BLUE}abilities: {RESET}", end='')
        for i in range(len(self.abilities)):
            print(f"{BLUE}{self.abilities[i].name}{RESET}", end='')
            if self.abilities[i].cd_count > 0:
                print(f'{RED}(cd = {self.abilities[i].cd_count}){RESET}', end='')
            if i != len(self.abilities) - 1:
                print(', ', end='')
        print()
        if self.sig_ability is not None:
            print(f'\t{YELLOW}signiture ability: {self.sig_ability.name}{RESET}', end='')
            if self.sig_ability.cd_count > 0:
                print(f"{RED}(cd = {self.sig_ability.cd_count}){RESET}", end='')
            print()
    
    def print_charges(self):
        print('\t', end='')
        for _ in range(self.charges):
            print(f'{GREEN}✚{RESET}' + ' ', end='')
            
        print(f'•'*(self.max_charge - self.charges))
    
    def print_souls(self):
        print('\t', end='')
        for _ in range(self.souls):
            print(f'🔥', end='')
            
        print(f'•'*(self.max_souls - self.souls))
    
    def print_phantom(self):
        print('\t', end='')
        for _ in range(self.phantom_asegis_count):
            print(f'{BLUE}⛨{RESET}', end='')
            
        print(f'•'*(self.phantom_aegis_max_count - self.phantom_aegis_count))
    
    def print_special_count(self, symbol, max, count, num_spacing=0):
        print('\t', end='')
        for _ in range(count):
            print(f'{symbol}' + num_spacing*' ', end='')
            
        print(f'•'*(max - count))
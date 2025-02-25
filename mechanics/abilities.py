from mechanics.buffs import Buff
from mechanics.ability_types import *
from globalss.globals import *
from globalss.colors import *
from mechanics.abnormalities import *
from mechanics.map_effects import *
from mechanics.projectiles import *
from game_stats.UI_utils import *
from player.character import *
from player.player_utils import *

######################################  ATK ABILITIES  ######################################

class Power_Shot(Atk_Abilities):
    def __init__(self,
                 name='Power Shot', 
                 damage=20, 
                 mana_cost=6,
                 cd=1,
                 character=None):
        super().__init__(name=name, damage=damage, mana_cost=mana_cost, character=character, cd=cd)
        
        self.push_back_dist = 1

    def use(self, target):
        if self.cd_count > 0:
            print(f'{BLUE} Ability is not ready, {self.cd_count} rounds left')
            return False
        if target.player == self.character.player:
            print(f'{RED}Cannot attack teamates!{RESET}')
            return False
        if self.character.mana < self.mana_cost:
            print(f'{RED}Not enough mana!{RESET}')
            return False 
        before_health = target.health
        if not self.character.attack(target, dmg_f=self.damage):
            return False
        self.cd_count = self.cd + 1
        x_diff = self.character.pos.x - target.pos.x    # Negative = source is left of target
        y_diff = self.character.pos.y - target.pos.y    # Negative = source is below target
        del_x = 0
        del_y = 0
        if x_diff < 0:   
            del_x = self.push_back_dist
        elif x_diff > 0:
            del_x = -self.push_back_dist
        if y_diff < 0:   
            del_y = self.push_back_dist
        elif y_diff > 0:
            del_y = -self.push_back_dist
            
        if not target.move(del_x, del_y, forced=True):
            target.health = before_health
            return False
        
        self.character.range_shot = True
        self.character.range_shot_count = 0
        self.character.mana -= self.mana_cost
        return True

######################################  BUFF ABILITIES  ######################################

class Charge(Buff_Abilities): 
    def __init__(self,
                 range_buff=[Buff(name='Charge: range+1', value=1, type=Buff_Type.RANGE_BUFF, duration=1)],
                 boost_buff=[Buff(name='Charge: mobil+1', value=1, type=Buff_Type.BOOST_BUFF, duration=1)],
                 name='Charge',
                 mana_cost=4,
                 add_rage=1,
                 cd=1,
                 character=None):
        
        self.add_rage = add_rage
        super().__init__(range_buff=range_buff, boost_buff=boost_buff, name=name, mana_cost=mana_cost, character=character, cd=cd)

    def use(self, target):
        if self.cd_count > 0:
            print(f'{BLUE} Ability is not ready, {self.cd_count} rounds left')
            return False
        if self.character.mana < self.mana_cost:
            print(f'{RED}Not enough mana!{RESET}')
            return False
        if pos_diff(self.character, target) > self.range:
            print(f'{CYAN}Not enough range!{RESET}')
            return False
        for buff_type, list in self.buff.items():
            if len(list) > 0:
                target.buff[buff_type].extend(list)
        self.character.mana -= self.mana_cost
        self.cd_count = self.cd + 1
        if self.character.rage < self.character.max_rage:
            self.character.rage += self.add_rage
            Stats.DUMPS.append(f'{CYAN}{self.name}: rage + {self.add_rage}{RESET}')
        Stats.DUMPS.append(f'{CYAN}Buff {self.name} applied to character: {target.name}!{RESET}')
        return True
    
class Precision(Buff_Abilities):
    def __init__(self,
                 range_buff=[Buff(name='Precision: range+1', value=1, type=Buff_Type.RANGE_BUFF, duration=2)],
                 name = 'Precision',
                 mana_cost=4,
                 cd=1,
                 character=None):
        super().__init__(range_buff=range_buff, name = name, mana_cost= mana_cost, character= character, cd=cd)

class Fortify(Buff_Abilities):
    def __init__(self,
                 def_buff=[Buff(name='Fortify: def+10', value=10, type=Buff_Type.DEF_BUFF, duration=2)],
                 name = 'Fortify',
                 mana_cost=4,
                 cd=1,
                 character=None):
        super().__init__(def_buff=def_buff, name = name, mana_cost= mana_cost, character= character, cd=cd)

class Extend(Buff_Abilities):
    def __init__(self,
                 range_buff=[Buff(name='Extend: range+1', value=1, type=Buff_Type.RANGE_BUFF, duration=1)],
                 name = 'Extend',
                 mana_cost=4,
                 cd=1,
                 character=None,
                 range=0):
        super().__init__(range_buff=range_buff, name=name, mana_cost=mana_cost, character=character, range=range, cd=cd)


######################################  AB ABILITIES  ######################################

class Ignite(Abnormality_Abilities):
    def __init__(self,
                 name='Ignite',
                 abnormalities=[Burn(duration=2, damage=10)],
                 mana_cost=5,
                 cd=1,
                 character=None):
        super().__init__(name=name, abnormalities=abnormalities, mana_cost=mana_cost, character=character, cd=cd)

class Bash(Abnormality_Abilities):
    def __init__(self,
                 name='Bash',
                 abnormalities=[Stun(duration=1)],
                 mana_cost=5,
                 cd=2,
                 character=None):
        super().__init__(name=name, abnormalities=abnormalities, mana_cost=mana_cost, character=character, cd=cd)


######################################  SIG ABILITIES  ######################################

class Blaze(Signiture_Abilities):
    def __init__(self,
                 character=None,
                 name='Blaze',
                 channel_round=2,
                 damage=10,
                 cd=1,
                 duration=3):
        super().__init__(name=name, channel_round=channel_round, character=character, sig_type=Sig_Type.SINGLE_USE, cd=cd)
        
        self.damage = damage
        self.duration = duration
        
    
    def use(self):
        print_range_map(self.character)
        text = input(f'{GREEN}Enter the position to apply {YELLOW}{self.name}{RESET}{GREEN} (x, y): {RESET}').split()
        try: 
            pos = Position(int(text[0]) - 1, int(text[1]) - 1)
            if not check_bounds(pos):
                print(f'{RED}Error: Position out of bound!{RESET}')
                return False
                
            elif max(abs(pos.x - self.character.pos.x), abs(pos.y - self.character.pos.y)) > self.character.range + buff_range(self.character):
                print(f'{RED}Error: Position out of range!{RESET}')
                return False
            else:
                apply_range_buff(self.character)
                for row in range(pos.y-1, pos.y+2):
                    for col in range(pos.x-1, pos.x+2):
                        if check_bounds(Position(col, row)):
                            Stats.MAP_EFFECT_LIST.append(Map_Burn(duration=self.duration, pos=Position(col, row), damage=self.damage, from_player=self.character.player))
                return True
        except:
            print(f'{RED}Error in position!{RESET}')
            return False

class Ashe_Arrow(Signiture_Abilities):
    def __init__(self, 
                 character=None,
                 name='Ashe Arrow',
                 channel_round=1,
                 cd=1,
                 damage=0,      # initial dmg
                 duration=0,    # initial stun duration
                 speed=1,
                 dmg_growth=10,  
                 stun_growth=0.5):
        super().__init__(name=name, channel_round=channel_round, character=character, sig_type=Sig_Type.SINGLE_USE, cd=cd)
        self.damage = damage
        self.stun_duration = duration
        self.speed = speed
        self.dmg_growth = dmg_growth
        self.stun_growth = stun_growth

    def use(self):
        text = input(f'{GREEN}Enter the direction of the Arrow for {self.character.color}{self.character.name}{GREEN} (e.g. 1 0 for ->): {RESET}').split()
        try:
            if len(text) != 2:
                print(f"{RED}Error in direction: Please only enter 2 numbers!{RESET}")
                return False
            direction = Position(int(text[0]), int(text[1]))
            if direction.x > 1 or direction.x < -1 or direction.y > 1 or direction.y < -1:
                print(f"{RED}Error in direction: Please only enter -1, 0, or 1!{RESET}")   
                return False
            position = Position((self.character.pos.x + direction.x), (self.character.pos.y - direction.y))
            arr = Arrow(pos=position, direction=direction, from_character=self.character, speed=self.speed, damage=self.damage, stun_duration=self.stun_duration,
                        dmg_growth=self.dmg_growth,
                        stun_growth=self.stun_growth)
            
            Stats.PROJECTILE_LIST.append(arr)
            return True
        except:
            print(f"{RED}Error in direction!{RESET}")
            return False

class Void_Slash(Signiture_Abilities):
    def __init__(self,
                 character=None,
                 name='Void Slash',
                 channel_round=0,
                 cd=1,
                 damage_growth=10,
                 range_growth=1,
                 max_charge=3,
                 burn_duration=2,
                 burn_dmg=10):
        super().__init__(name=name, channel_round=channel_round, character=character, sig_type=Sig_Type.CONTINUOUS, cd=cd)
        self.damage_growth = damage_growth
        self.range_growth = range_growth
        self.max_charge = max_charge
        self.burn_duration = burn_duration
        self.burn_dmg = burn_dmg
        
    def use(self):
        if self.rounds_used == 0 and self.character.souls == 0:
            return True
        
        charge = self.rounds_used + self.character.souls
        if charge > self.max_charge:
            charge = self.max_charge
            
        damage = self.damage_growth * charge
        atk_range = self.range_growth * charge
        
        print(f'{GREEN}Current Charge: {charge}{RESET}')
        print(f'{GREEN}\tdmg = {damage}{RESET}')
        print(f'{GREEN}\trange = {atk_range}')
        text = input(f'{GREEN}Enter the direction of the Void Slash for {self.character.color}{self.character.name}{GREEN} (e.g. 1 0 for ->): {RESET}').split()
        try:
            if len(text) != 2:
                print(f"{RED}Error in direction: Please only enter 2 numbers!{RESET}")
                return False
            direction = Position(int(text[0]), int(text[1]))
            if direction.x > 1 or direction.x < -1 or direction.y > 1 or direction.y < -1:
                print(f"{RED}Error in direction: Please only enter -1, 0, or 1!{RESET}")   
                return False
            position = Position(self.character.pos.x, self.character.pos.y)
            for _ in range(atk_range):
                position.x += direction.x
                position.y -= direction.y  
                if check_bounds(position):
                    self.check_hit(position, damage)
                    Stats.MAP_EFFECT_LIST.append(Map_Burn(duration=self.burn_duration, pos=copy.deepcopy(position), damage=self.burn_dmg, from_player=self.character.player))
            self.character.souls = 0
            return True
        except:
            print(f"{RED}Error in direction!{RESET}")
            return False
          
    def check_hit(self, position, damage):
        target_player = Stats.PLAYER_LIST[0]
        if target_player == self.character.player:
            target_player = Stats.PLAYER_LIST[1]
        for target in target_player.avail_characters:
            if target.pos == position:
                dmg = apply_def_buff(source=self.character, target=target, dmg=damage)
                if dmg >= 0:
                    target.health -= dmg
                if target.rage is not None and target.rage != target.max_rage:
                    target.rage += 1
                    Stats.DUMPS.append(f'{CYAN}{target.name} rage + 1{RESET}')
                Stats.DUMPS.append(f'{CYAN}Attack is successful: {target.name}: health - {dmg}{RESET}')
######################################  HEAL ABILITIES  ######################################

class Heal(Heal_Abilities):
    def __init__(self,
                 character=None,
                 name='Heal',
                 mana_cost=6,
                 cd=1,
                 heal_amount=20
                 ):
        super().__init__(name=name, mana_cost=mana_cost, heal_amount=heal_amount, character=character, cd=cd)
    
    def use(self, target):
        if self.cd_count > 0:
            print(f'{BLUE}Ability is not ready, {self.cd_count} rounds left')
            return False
        if target.health == target.max_health:
            print(f"{RED}Target health already at max!{RESET}")
            return False
        if self.character.mana < self.mana_cost and self.character.charges < self.character.max_charge:
            print(f"{RED}Not enough mana!{RESET}")
            return False
        if target.player != self.character.player:
            print(f'{RED}Cannot apply to enemy characters!{RESET}')
            return False
        if pos_diff(self.character, target) > self.character.range:
            print(f"{CYAN}Not enough range!{RESET}")
            return False
        health_restored = 0
        prev_health = target.health
        if target.health + self.heal_amount > target.max_health:
            target.health = target.max_health
        else:
            target.health += self.heal_amount
        if self.character.charges == self.character.max_charge:
            self.character.charges = 0
        else:
            self.character.mana -= self.mana_cost
        self.cd_count = self.cd + 1    
        health_restored = target.health - prev_health
        
        Stats.DUMPS.append(f'{GREEN}Heal applied to {target.name}! Health + {health_restored}{RESET}')
        return True
######################################  SPECIAL ABILITIES  ######################################

class Sheath:
    def __init__(self,
                 name = 'Sheath',
                 mana_cost=3,
                 cd=1,
                 character=None,
                 sheath_count=2,
                 range=0):
        self.name = name
        self.ability_type = Ability_Type.BUFF_ABIL
        self.mana_cost = mana_cost
        self.sheath_count = sheath_count
        self.range = range
        self.character = character
        self.cd = cd
        self.cd_count = 0
        
    def use(self, target):
        if self.character.mana < self.mana_cost:
            print(f'{RED}Not enough mana!{RESET}')
            return False
        if pos_diff(self.character, target) > self.range:
            print(f'{CYAN}Can only apply to self!{RESET}')
            return False
        if not self.character.sheathed:
            self.character.sheathed = True
            self.character.mana -= self.mana_cost
            self.character.sheath_counter = self.sheath_count
            Stats.DUMPS.append(f'{CYAN}{self.name} is sheathed!{RESET}')
            return True
        else:
            print(f'{CYAN}Already sheathed!{RESET}')
            return False
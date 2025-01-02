from mechanics.buffs import Buff
from mechanics.ability_types import *
from globalss.globals import *
from globalss.colors import *
from mechanics.abnormalities import *
from mechanics.map_effects import *
from mechanics.projectiles import *
from game_stats.UI_utils import *
from player.character import *

######################################  ATK ABILITIES  ######################################

class Power_Shot(Atk_Abilities):
    def __init__(self,
                 name='Power Shot', 
                 damage=2, 
                 mana_cost=6,
                 character=None):
        super().__init__(name=name, damage=damage, mana_cost=mana_cost, character=character)
        
        self.push_back_dist = 1
    
    def use(self, target):
        if target.player == self.character.player:
            print(f'{RED}Cannot attack teamates!{RESET}')
            return False
        if self.character.mana < self.mana_cost:
            print(f'{RED}Not enough mana!{RESET}')
            return False
        if not self.character.attack(target, dmg_f=self.damage):
            return False
        
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
            return False
        
        self.character.mana -= self.mana_cost
        return True

######################################  BUFF ABILITIES  ######################################

class Charge(Buff_Abilities): 
    def __init__(self,
                 atk_buff=[Buff(name='Charge: atk+1', value=1, type=Buff_Type.ATK_BUFF, duration=1)],
                 boost_buff=[Buff(name='Charge: mobil+1', value=1, type=Buff_Type.BOOST_BUFF, duration=1)],
                 name='Charge',
                 mana_cost=4,
                 character=None):
        
        super().__init__(atk_buff=atk_buff, boost_buff=boost_buff, name=name, mana_cost=mana_cost, character=character)

class Precision(Buff_Abilities):
    def __init__(self,
                 range_buff=[Buff(name='Precision: range+1', value=1, type=Buff_Type.RANGE_BUFF, duration=2)],
                 name = 'Precision',
                 mana_cost=4,
                 character=None):
        super().__init__(range_buff=range_buff, name = name, mana_cost= mana_cost, character= character)

class Fortify(Buff_Abilities):
    def __init__(self,
                 def_buff=[Buff(name='Fortify: def+1', value=1, type=Buff_Type.DEF_BUFF, duration=2)],
                 name = 'Fortify',
                 mana_cost=4,
                 character=None):
        super().__init__(def_buff=def_buff, name = name, mana_cost= mana_cost, character= character)

class Extend(Buff_Abilities):
    def __init__(self,
                 range_buff=[Buff(name='Extend: range+1', value=1, type=Buff_Type.RANGE_BUFF, duration=1)],
                 name = 'Extend',
                 mana_cost=4,
                 character=None,
                 range=0):
        super().__init__(range_buff=range_buff, name=name, mana_cost=mana_cost, character=character, range=range)

    
######################################  AB ABILITIES  ######################################

class Ignite(Abnormality_Abilities):
    def __init__(self,
                 name='Ignite',
                 abnormalities=[Burn(duration=3, damage=1)],
                 mana_cost=5,
                 character=None):
        super().__init__(name=name, abnormalities=abnormalities, mana_cost=mana_cost, character=character)

class Bash(Abnormality_Abilities):
    def __init__(self,
                 name='Bash',
                 abnormalities=[Stun(duration=1)],
                 mana_cost=5,
                 character=None):
        super().__init__(name=name, abnormalities=abnormalities, mana_cost=mana_cost, character=character)


######################################  SIG ABILITIES  ######################################

class Blaze(Signiture_Abilities):
    def __init__(self,
                 character=None,
                 name='Blaze',
                 channeling=1,
                 damage=1,
                 duration=3):
        super().__init__(name=name, channeling=channeling, character=character)
        
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
                 channeling=1,
                 damage=0,      # initial dmg
                 duration=0,    # initial stun duration
                 speed=1,
                 dmg_growth=1,  
                 stun_growth=0.5):
        super().__init__(name=name, channeling=channeling, character=character)
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
        
        
######################################  HEAL ABILITIES  ######################################

class Heal(Heal_Abilities):
    def __init__(self,
                 character=None,
                 name='Heal',
                 mana_cost=5,
                 heal_amount=2
                 ):
        super().__init__(name=name, mana_cost=mana_cost, heal_amount=heal_amount, character=character)


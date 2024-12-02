from mechanics.buffs import Buff
from globalss.globals import *
from globalss.colors import *
from player.character import *

import copy

class Atk_Abilities:   
    def __init__(self, name='Attack Ability', damage=0, mana_cost=0, range=0, mobility_cost=0):
        self.name = name
        self.ability_type = Ability_Type.ATK_ABIL
        self.damage = damage
        self.mana_cost = mana_cost
        self.range = range
        self.mobility_cost =mobility_cost

class Buff_Abilities:
    def __init__(self, atk_buff=[], atk_debuff=[], def_buff=[], def_debuff=[], boost_buff=[], boost_debuff=[], range_buff=[], range_debuff=[], name='Buff Ability', mana_cost=0, range=0, mobility_cost=0):
        self.buff = {
            Buff_Type.ATK_BUFF : atk_buff,    # affects atk dmg
            Buff_Type.ATK_DEBUFF : atk_debuff,
            Buff_Type.DEF_BUFF : def_buff,    # affects dmg received
            Buff_Type.DEF_DEBUFF : def_debuff,
            Buff_Type.BOOST_BUFF : boost_buff,  # affects movements
            Buff_Type.BOOST_DEBUFF : boost_debuff,
            Buff_Type.RANGE_BUFF : range_buff,  # affects attack and ability range
            Buff_Type.RANGE_DEBUFF : range_debuff,
        }
        self.name = name
        self.ability_type = Ability_Type.BUFF_ABIL
        self.mana_cost = mana_cost
        self.range = range
        self.mobility_cost = mobility_cost
    
    def use(self, source, target):
        if source.mana < self.mana_cost:
            print(f'{RED}Not enough mana!{RESET}')
            return False
        if pos_diff(source, target) > self.range:
            print(f'{CYAN}Not enough range!{RESET}')
            return False
        for buff_type, list in self.buff.items():
            if len(list) > 0:
                target.buff[buff_type].extend(list)
        source.mana -= self.mana_cost
        print(f'{CYAN}Buff {self.name} applied to character: {target.name}!{RESET}')
        return True

class Abnormality_Abilities:
    def __init__(self, name=None, abnormalities=None, mana_cost=0):
        self.name = name
        self.abnormalities = abnormalities
        self.mana_cost = mana_cost
    
    def use(self, source, target):
        if source.mana < self.mana_cost:
            print(f"{RED}Not enough mana!{RESET}")
            return False
        if pos_diff(source, target) > source.range:
            print(f"{CYAN}Not enough range!{RESET}")
            return False
        for ab in self.abnormalities:
            if len(target.abnormalities) > 0:
                name = ab.name
                for abnorm in target.abnormalities:
                    if abnorm.name == name:
                        abnorm.duration += ab.duration
            else:
                ab_copy = copy.deepcopy(ab)
                target.abnormalities.append(ab_copy)
                ab_copy.character = target
        source.mana -= self.mana_cost
        print(f"{CYAN}Abnormality: ", end="")
        for ab in self.abnormalities:
            print(f"{ab.name} ", end="")
        print(f"applied to character: {target.name}!{RESET}")

        return True
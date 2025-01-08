from mechanics.buffs import Buff
from globalss.globals import *
from globalss.colors import *
from player.character import *

import copy

class Atk_Abilities:   
    def __init__(self, name='Attack Ability', damage=0, mana_cost=0, range=0, mobility_cost=0, character=None):
        self.name = name
        self.ability_type = Ability_Type.ATK_ABIL
        self.damage = damage
        self.mana_cost = mana_cost
        self.range = range
        self.mobility_cost = mobility_cost
        self.character = character

class Buff_Abilities:
    def __init__(self, atk_buff=[], atk_debuff=[], def_buff=[], def_debuff=[], boost_buff=[], boost_debuff=[], range_buff=[], range_debuff=[], name='Buff Ability', mana_cost=0, range=0, mobility_cost=0, character=None):
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
        self.character = character
    
    def use(self, target):
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
        Stats.DUMPS.append(f'{CYAN}Buff {self.name} applied to character: {target.name}!{RESET}')
        return True

class Abnormality_Abilities:
    def __init__(self, name=None, abnormalities=None, mana_cost=0, character=None):
        self.name = name
        self.ability_type = Ability_Type.AB_ABIL
        self.abnormalities = abnormalities
        self.mana_cost = mana_cost
        self.character = character
    
    def use(self, target):
        if target.player == self.character.player:
            print(f"{RED}Cannot apply to player in same team!{RESET}")
            return False
        if self.character.mana < self.mana_cost:
            print(f"{RED}Not enough mana!{RESET}")
            return False
        if pos_diff(self.character, target) > self.character.range + buff_range(self.character):
            print(f"{CYAN}Not enough range!{RESET}")
            return False
        for ab in self.abnormalities:
            if len(target.abnormalities) > 0:
                name = ab.name
                found = False
                for abnorm in target.abnormalities:
                    if abnorm.name == name:
                        abnorm.duration += ab.duration
                        found = True
                        break
            if not found:
                ab_copy = copy.deepcopy(ab)
                target.abnormalities.append(ab_copy)
                ab_copy.character = target
        
        apply_range_buff(self.character)
        self.character.mana -= self.mana_cost
        dump = f"{CYAN}Abnormality: "
        for ab in self.abnormalities:
            dump += f"{ab.name} "
        Stats.DUMPS.append(dump + f"applied to character: {target.name}!{RESET}")

        return True

class Signiture_Abilities:
    def __init__(self, name='Sig Abil', channel_round=0, character=None, sig_type=None):
        self.name = name
        self.channel_round = channel_round
        self.character = character
        self.sig_type = sig_type
        
        # For continuous sig
        self.rounds_used = 0
        self.using = False
        
        self.ability_type = Ability_Type.SIG_ABIL
    
    def channel(self):
        if self.character.channel_counter > 0:
            self.character.channel_counter -= 1
            
        elif self.character.channel_counter == -1:
            self.character.channel_counter = self.channel_round
                  
        if self.character.channel_counter == 0:    # READY to use
            if self.sig_type == Sig_Type.SINGLE_USE:
                while not self.use():
                    pass
                self.character.channel_counter = -1
            elif self.sig_type == Sig_Type.CONTINUOUS:
                while not self.start():
                    pass
            
        return True
    
    def start(self):
        if self.using == False:     # First use after finishing channeling
            self.using = True
            return True
        
        # not first use
        text = input(f'{GREEN}Enter the action for {RESET}{self.character.color}{self.character.name}{RESET}{GREEN} (STOP, END): {RESET}').split()
        
        match text[0].upper():
            case 'END':
                print(f'{CYAN}Round Ended{RESET}')
                self.rounds_used += 1
                return True
            case 'STOP':
                while not self.use():
                    pass
                self.character.channel_counter = -1
                self.using = False
                self.rounds_used = 0
                self.character.channel_counter = -1
                return True
                
class Heal_Abilities:
    def __init__(self, name=None, mana_cost=0, heal_amount=0, character=None):
        self.name = name
        self.mana_cost = mana_cost
        self.heal_amount = heal_amount
        self.character = character
        
        self.ability_type = Ability_Type.HEAL_ABIL
    
    def use(self, target):
        if target.health == target.max_health:
            print(f"{RED}Target health already at max!{RESET}")
            return False
        if self.character.mana < self.mana_cost:
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
        self.character.mana -= self.mana_cost
        health_restored = target.health - prev_health
        
        Stats.DUMPS.append(f'{GREEN}Heal applied to {target.name}! Health + {health_restored}{RESET}')
        return True
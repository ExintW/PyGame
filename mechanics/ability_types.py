from mechanics.buffs import Buff
from globalss.globals import *
from globalss.colors import *
from player.character import *

class Atk_Abilities:
    name = 'Attack Ability'
    ability_type = Ability_Type.ATK_ABIL
    damage = 0
    mana_cost = 0
    range = 0
    mobility_cost = 0
    
    def __init__(self):
        pass

class Buff_Abilities:
    name = 'Buff Ability'
    ability_type = Ability_Type.BUFF_ABIL
    mana_cost = 0
    range = 0
    mobility_cost = 0
    
    def __init__(self, atk_buff=[], atk_debuff=[], def_buff=[], def_debuff=[], boost_buff=[], boost_debuff=[], range_buff=[], range_debuff=[]):
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
        print(f'{CYAN}Buff applied to player: {target.name}!{RESET}')
        return True

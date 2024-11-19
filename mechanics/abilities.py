from mechanics.buffs import Buff
from mechanics.ability_types import *
from globals.globals import *
from globals.colors import *
    
class Power_Shot(Atk_Abilities):
    name = 'Power Shot'
    damage = 2
    mana_cost = 6
    
    push_back_dist = 1
    
    def use(self, source, target):
        if source.mana < self.mana_cost:
            print(f'{RED}Not enough mana!{RESET}')
            return False
        if not source.attack(target, dmg_f=self.damage):
            return False
        if source.pos < target.pos:
            target.move(self.push_back_dist, forced=True)
        else:
            target.move(-self.push_back_dist, forced=True)
        source.mana -= self.mana_cost
        return True


class Charge(Buff_Abilities):
    name = 'Charge'
    mana_cost = 4
    
    def __init__(self):
        super().__init__(atk_buff=[Buff('Charge: atk+1', 1, Buff_Type.ATK_BUFF, 1)],
                         boost_buff=[Buff('Charge: mobil+1', 1, Buff_Type.BOOST_BUFF, 1)])

class Precision(Buff_Abilities):
    name = 'Precision'
    mana_cost = 4
    
    def __init__(self):
        super().__init__(range_buff=[Buff('Precision: range+1', 1, Buff_Type.RANGE_BUFF, 2)])
        
        
from mechanics.buffs import Buff
from mechanics.ability_types import *
from globalss.globals import *
from globalss.colors import *
from mechanics.abnormalities import *
    
class Power_Shot(Atk_Abilities):
    def __init__(self):
        super().__init__(name='Power Shot', damage=2, mana_cost=6)
        
        self.push_back_dist = 1
    
    def use(self, source, target):
        if target.player == source.player:
            print(f'{RED}Cannot attack teamates!{RESET}')
            return False
        if source.mana < self.mana_cost:
            print(f'{RED}Not enough mana!{RESET}')
            return False
        if not source.attack(target, dmg_f=self.damage):
            return False
        
        x_diff = source.pos.x - target.pos.x    # Negative = source is left of target
        y_diff = source.pos.y - target.pos.y    # Negative = source is below target
        if x_diff < 0:   
            target.move(self.push_back_dist, 0, forced=True)
        elif x_diff > 0:
            target.move(-self.push_back_dist, 0, forced=True)
        if y_diff < 0:   
            target.move(0, self.push_back_dist, forced=True)
        elif y_diff > 0:
            target.move(0, -self.push_back_dist, forced=True)
        source.mana -= self.mana_cost
        return True


class Charge(Buff_Abilities): 
    def __init__(self):
        super().__init__(atk_buff=[Buff('Charge: atk+1', 1, Buff_Type.ATK_BUFF, 1)],
                         boost_buff=[Buff('Charge: mobil+1', 1, Buff_Type.BOOST_BUFF, 1)],
                         name='Charge',
                         mana_cost=4)

class Precision(Buff_Abilities):
    def __init__(self):
        super().__init__(range_buff=[Buff('Precision: range+1', 1, Buff_Type.RANGE_BUFF, 2)],
                         name = 'Precision',
                         mana_cost=4)
        
class Ignite(Abnormality_Abilities):
    def __init__(self):
        super().__init__(name='Ignite',
                         abnormalities=[Burn(duration=3, damage=1)],
                         mana_cost=5)
        
from mechanics.buffs import Buff
from mechanics.ability_types import *
from globalss.globals import *
from globalss.colors import *
from mechanics.abnormalities import *
from mechanics.map_effects import *
    
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
        
        source.mana -= self.mana_cost
        return True


class Charge(Buff_Abilities): 
    def __init__(self):
        super().__init__(atk_buff=[Buff(name='Charge: atk+1', value=1, type=Buff_Type.ATK_BUFF, duration=1)],
                         boost_buff=[Buff(name='Charge: mobil+1', value=1, type=Buff_Type.BOOST_BUFF, duration=1)],
                         name='Charge',
                         mana_cost=4)

class Precision(Buff_Abilities):
    def __init__(self):
        super().__init__(range_buff=[Buff(name='Precision: range+1', value=1, type=Buff_Type.RANGE_BUFF, duration=2)],
                         name = 'Precision',
                         mana_cost=4)
        
class Ignite(Abnormality_Abilities):
    def __init__(self):
        super().__init__(name='Ignite',
                         abnormalities=[Burn(duration=3, damage=1)],
                         mana_cost=5)

class Blaze:
    def __init__(self,
                 name='Blaze',
                 damage=1,
                 duration=3):
        self.name = name
        self.damage = damage
        self.duration = duration
        
        self.ability_type = Ability_Type.SIG_ABIL
    
    def use(self, from_player):
        try:
            text = input(f'{GREEN}Enter the position to apply {YELLOW}{self.name}{RESET}{GREEN} (x, y): {RESET}').split()
            
            pos = Position(int(text[0]) - 1, Stats.MAP_SIZE.y - int(text[1]))
            if pos.x < 0 or pos.x >= Stats.MAP_SIZE.x or pos.y < 0 or pos.y >= Stats.MAP_SIZE.y:
                print(f'{RED}Error position!{RESET}')
                return False
            
            for row in range(pos.y-1, pos.y+2):
                for col in range(pos.x-1, pos.x+2):
                    if row < Stats.MAP_SIZE.y and row >= 0 and col < Stats.MAP_SIZE.x and col >= 0:
                        Stats.MAP_EFFECT_LIST.append(Map_Burn(duration=self.duration, pos=Position(col, row), damage=self.damage, from_player=from_player))
            return True
        except:
            print(f'{RED}Error position!{RESET}')
            return False
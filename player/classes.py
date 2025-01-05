from globalss.colors import RESET
from globalss.globals import *
from mechanics.buffs import Buff
from player.character import Character
from mechanics.abilities import *

class Archer(Character):
    def __init__(self, player=None, name=None, profession='ARCHER', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Power_Shot(character=self), Precision(character=self)],
                         sig_ability=Ashe_Arrow(character=self),
                         range=2,
                         damage=2,
                         max_health=5,
                         mobility=2,
                         max_mana=10,
                         symbol='A') # 🏹\uFE0E
        
        self.buff[Buff_Type.BOOST_BUFF].append(Buff('Passive: mobil+1', 1, Buff_Type.BOOST_BUFF, 1))

class Warrior(Character):
    def __init__(self, player=None, name=None, profession='WARRIOR', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Charge(character=self)],
                         range=1,
                         damage=2,
                         max_health=7,
                         mobility=2,
                         max_mana=10,
                         max_rage=7,
                         max_rage_duration=3,
                         symbol='W') # ⚔️\uFE0E
        self.rage_def_buff_value = 1
        self.rage_atk_buff_value = 1
        self.rage_range_buff_value = 1
        self.rage_boost_buff_value = 1
        self.buff[Buff_Type.ATK_BUFF].append(Buff('Passive: atk+1', 1, Buff_Type.ATK_BUFF, 1))
        

class Mage(Character):
    def __init__(self, player=None, name=None, profession='MAGE', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Ignite(character=self)],
                         sig_ability=Blaze(character=self),
                         range=2,
                         damage=1,
                         max_health=4,
                         mobility=1,
                         max_mana=15,
                         symbol='M') # 🧙‍♂️\uFE0E
        self.buff[Buff_Type.RANGE_BUFF].append(Buff('Passive: range+1', 1, Buff_Type.RANGE_BUFF, 1))
        
class Healer(Character):
    def __init__(self, player=None, name=None, profession='HEALER', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         range=3,
                         abilities=[Heal(character=self), Extend(character=self, range=3)],
                         damage=1,
                         max_health=4,
                         mobility=1,
                         max_mana=15,
                         symbol='H')

class Knight(Character):
    def __init__(self, player=None, name=None, profession='KNIGHT', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Fortify(character=self), Bash(character=self)],
                         range=1,
                         damage=1,
                         max_health=10,
                         mobility=1,
                         max_mana=10,
                         symbol='K') # 🛡️\uFE0E
        self.buff[Buff_Type.DEF_BUFF].append(Buff('Passive: def+1', 1, Buff_Type.DEF_BUFF, 99))

class Samurai(Character):
    def __init__(self, player=None, name=None, profession='SAMURAI', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Sheath(character=self)],
                         range=1,
                         damage=2,
                         max_health=7,
                         mobility=1,
                         max_mana=10,
                         symbol='S')
        self.sheathed = False   # 纳刀
        self.sheath_counter = 0
        self.buff[Buff_Type.BOOST_BUFF].append(Buff('Passive: mobil+1', 1, Buff_Type.BOOST_BUFF, 1))
        
    def attack(self, target, dmg_f=0):     
        if self.sheathed and self.sheath_counter > 0:
            print(f'{CYAN}Samurai cannot atk this round (Sheathed)!{RESET}')
            return False
        elif self.sheathed and self.sheath_counter == 0:
            self.buff[Buff_Type.RANGE_BUFF].append(Buff(name='Sheath: range+1', value=1, type=Buff_Type.RANGE_BUFF, duration=1))
            self.buff[Buff_Type.ATK_BUFF].append(Buff(name='Sheath: dmg+1', value=1, type=Buff_Type.ATK_BUFF, duration=1))
            self.sheathed = False
        
        atk_range = self.range + buff_range(self)
        
        if target == self:
            print(f'{CYAN}Cannot attack self!{RESET}')
            return False
        elif pos_diff(self, target) <= atk_range:
            dmg = self.apply_dmg_buff(dmg_f)
            apply_range_buff(self)
            
            for c in target.player.avail_characters:
                if c == target:
                    act_dmg = self.apply_def_buff(target=c, dmg=dmg)
                    if act_dmg > 0:
                        c.health -= act_dmg
                        Stats.DUMPS.append(f'{CYAN}Attack is successful: {c.name}: health - {act_dmg}{RESET}')
                elif pos_diff(self, c) <= atk_range:
                    half_dmg = self.apply_def_buff(target=c, dmg=int(dmg/2))
                    if half_dmg > 0:
                        c.health -= half_dmg
                        Stats.DUMPS.append(f'{CYAN}Attack is successful: {c.name}: health - {half_dmg}{RESET}')
                else:
                    continue
                
                if c.rage is not None and c.rage < c.max_rage:
                    c.rage += 1
                    Stats.DUMPS.append(f'{CYAN}{c.name} rage + 1{RESET}')  
            
            return True
        else:
            print(f'{CYAN}Not enough range!{RESET}')
            return False
    

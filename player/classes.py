from globalss.colors import RESET
from globalss.globals import *
from mechanics.buffs import Buff
from player.character import *
from mechanics.abilities import *

class Archer(Character):
    def __init__(self, player=None, name=None, profession='ARCHER', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Power_Shot(character=self), Precision(character=self)],
                         sig_ability=Ashe_Arrow(character=self),
                         range=2,
                         damage=20,
                         max_health=50,
                         mobility=2,
                         max_mana=10,
                         symbol='A') # 🏹\uFE0E
        self.range_shot = False
        self.range_shot_count = 1
        self.buff[Buff_Type.BOOST_BUFF].append(Buff('Passive: mobil+1', 1, Buff_Type.BOOST_BUFF, 1))

class Warrior(Character):
    def __init__(self, player=None, name=None, profession='WARRIOR', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Charge(character=self)],
                         range=1,
                         damage=20,
                         max_health=70,
                         mobility=2,
                         max_mana=10,
                         max_rage=7,
                         max_rage_duration=3,
                         symbol='W') # ⚔️\uFE0E
        self.rage_def_buff_value = 10
        self.rage_atk_buff_value = 10
        self.rage_range_buff_value = 1
        self.rage_boost_buff_value = 1
        self.buff[Buff_Type.ATK_BUFF].append(Buff('Passive: atk+10', 10, Buff_Type.ATK_BUFF, 1))
        

class Mage(Character):
    def __init__(self, player=None, name=None, profession='MAGE', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Ignite(character=self)],
                         sig_ability=Blaze(character=self),
                         range=2,
                         damage=10,
                         max_health=40,
                         mobility=1,
                         max_mana=10,
                         symbol='M') # 🧙‍♂️\uFE0E
        self.buff[Buff_Type.RANGE_BUFF].append(Buff('Passive: range+1', 1, Buff_Type.RANGE_BUFF, 1))
        
class Healer(Character):
    def __init__(self, player=None, name=None, profession='HEALER', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         range=3,
                         abilities=[Heal(character=self), Extend(character=self, range=3)],
                         damage=10,
                         max_health=40,
                         mobility=1,
                         max_mana=10,
                         symbol='H')
        self.max_charge = 2
        self.charges = 0

class Ghost_Knight(Character):
    def __init__(self, player=None, name=None, profession='GHOST_KNIGHT', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Fortify(character=self), Bash(character=self)],
                         range=1,
                         damage=10,
                         max_health=70,
                         mobility=2,
                         max_mana=10,
                         symbol='G') # 🛡️\uFE0E
        # self.buff[Buff_Type.DEF_BUFF].append(Buff('Passive: def+10', 10, Buff_Type.DEF_BUFF, 3))
        self.immune_mov_pen = True  # Unique Passive: immune to mov pen
        self.phantom_aegis = True
        self.phantom_aegis_count = 0
        self.phantom_aegis_max_count = 3

class Samurai(Character):
    def __init__(self, player=None, name=None, profession='SAMURAI', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Sheath(character=self)],
                         sig_ability=Void_Slash(character=self),
                         range=1,
                         damage=20,
                         max_health=70,
                         mobility=1,
                         max_mana=10,
                         symbol='S')
        self.sheathed = False   # 纳刀
        self.sheath_counter = 0
        self.souls = 0
        self.max_souls = 3
        self.buff[Buff_Type.BOOST_BUFF].append(Buff('Passive: mobil+1', 1, Buff_Type.BOOST_BUFF, 1))
        
    def attack(self, target, dmg_f=0):     
        before_range_buff = self.buff[Buff_Type.RANGE_BUFF].copy()
        before_atk_buff = self.buff[Buff_Type.ATK_BUFF].copy()
        before_sheathed = self.sheathed
        
        is_sheated_atk = False # for souls calculation
        
        if self.sheathed and self.sheath_counter > 0:
            print(f'{CYAN}Samurai cannot atk this round (Sheathed)!{RESET}')
            return False
        elif self.sheathed and self.sheath_counter == 0:
            self.buff[Buff_Type.RANGE_BUFF].append(Buff(name='Sheath: range+1', value=1, type=Buff_Type.RANGE_BUFF, duration=1))
            self.buff[Buff_Type.ATK_BUFF].append(Buff(name='Sheath: dmg+10', value=10, type=Buff_Type.ATK_BUFF, duration=1))
            self.sheathed = False
            is_sheated_atk = True
        
        atk_range = self.range + buff_range(self)
        
        if target == self:
            print(f'{CYAN}Cannot attack self!{RESET}')
            self.buff[Buff_Type.RANGE_BUFF] = before_range_buff
            self.buff[Buff_Type.ATK_BUFF] = before_atk_buff
            self.sheathed = before_sheathed
            return False
        elif pos_diff(self, target) <= atk_range:
            dmg = apply_dmg_buff(self, dmg_f)
            apply_range_buff(self)
            
            for c in target.player.avail_characters:
                if c == target:
                    act_dmg = apply_def_buff(source=self, target=c, dmg=dmg)
                    if act_dmg > 0:
                        c.health -= act_dmg
                        Stats.DUMPS.append(f'{CYAN}Attack is successful: {c.name}: health - {act_dmg}{RESET}')
                elif pos_diff(self, c) <= atk_range:
                    half_dmg = apply_def_buff(source=self, target=c, dmg=int(dmg/2))
                    if half_dmg > 0:
                        c.health -= half_dmg
                        Stats.DUMPS.append(f'{CYAN}Attack is successful: {c.name}: health - {half_dmg}{RESET}')
                        if self.souls < self.max_souls:
                            self.souls += 1
                        Stats.DUMPS.append(f'{CYAN}Slash atk: Souls + 1{RESET}')
                else:
                    continue
                
                if c.rage is not None and c.rage < c.max_rage:
                    c.rage += 1
                    Stats.DUMPS.append(f'{CYAN}{c.name} rage + 1{RESET}')  
            
            if is_sheated_atk and self.souls < self.max_souls:
                self.souls += 1
                Stats.DUMPS.append(f'{CYAN}Sheathed atk: Souls + 1{RESET}')
            
            return True
        else:
            print(f'{CYAN}Not enough range!{RESET}')
            self.buff[Buff_Type.RANGE_BUFF] = before_range_buff
            self.buff[Buff_Type.ATK_BUFF] = before_atk_buff
            self.sheathed = before_sheathed
            return False
    

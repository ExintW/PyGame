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
                         symbol='W') # ⚔️\uFE0E
        
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
    def __init__(self, player=None, name=None, profession='Knight', pos=None):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Fortify(character=self), Bash(character=self)],
                         range=1,
                         damage=1,
                         max_health=10,
                         mobility=1,
                         max_mana=10,
                         symbol='K') # 🛡️\uFE0E
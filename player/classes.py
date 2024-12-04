from globalss.colors import RESET
from globalss.globals import *
from mechanics.buffs import Buff
from player.character import Character
from mechanics.abilities import *

class Archer(Character):
    def __init__(self, player=None, name=None, profession='ARCHER', pos=0):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Power_Shot(character=self), Precision(character=self)],
                         range=2,
                         damage=1,
                         max_health=5,
                         mobility=2,
                         max_mana=10,
                         symbol='A')
        
        self.buff[Buff_Type.BOOST_BUFF].append(Buff('Passive: mobil+1', 1, Buff_Type.BOOST_BUFF, 1))

class Warrior(Character):
    def __init__(self, player=None, name=None, profession='WARRIOR', pos=0):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Charge(character=self)],
                         range=1,
                         damage=2,
                         max_health=7,
                         mobility=2,
                         max_mana=10,
                         symbol='W')

class Mage(Character):
    def __init__(self, player=None, name=None, profession='MAGE', pos=0):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Ignite(character=self)],
                         sig_ability=Blaze(character=self),
                         range=2,
                         damage=1,
                         max_health=5,
                         mobility=1,
                         max_mana=15,
                         symbol='M')
        
class Healer(Character):
    def __init__(self, player=None, name=None, profession='HEALER', pos=0):
        super().__init__(player=player, name=name, profession=profession, pos=pos,
                         abilities=[Heal(character=self)],
                         range=2,
                         damage=1,
                         max_health=5,
                         mobility=1,
                         max_mana=15,
                         symbol='H')
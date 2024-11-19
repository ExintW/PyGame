from globals.colors import RESET
from globals.globals import *
from mechanics.buffs import Buff
from player.player import Player

class Archer(Player):
    range = 2
    damage = 1
    health = 5
    max_health = 5
    mobility = 1
    mana = 10
    max_mana = 10
    
    def __init__(self, name='', profession='', pos=0, color=RESET, abilities=[]):
        super().__init__(name, profession, pos, color, abilities)
        self.buff[Buff_Type.BOOST_BUFF].append(Buff('Passive: mobil+1', 1, Buff_Type.BOOST_BUFF, 1))

class Warrior(Player):
    range = 1
    damage = 2
    health = 7
    max_health = 7
    mobility = 1
    mana = 10
    max_mana = 10
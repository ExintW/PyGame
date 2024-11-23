from globals.colors import RESET
from globals.globals import *
from mechanics.buffs import Buff
from player.character import Character
from mechanics.abilities import *

class Archer(Character):
    def __init__(self, player=None, name=None, profession=None, pos=0, abilities=None):
        super().__init__(player, name, profession, pos, abilities)
        self.buff[Buff_Type.BOOST_BUFF].append(Buff('Passive: mobil+1', 1, Buff_Type.BOOST_BUFF, 1))
        self.abilities = [Power_Shot(), Precision()]
        
        self.range = 2
        self.damage = 1
        self.health = 5
        self.max_health = 5
        self.mobility = 1
        self.mana = 10
        self.max_mana = 10
        self.symbol = 'A'

class Warrior(Character):
    def __init__(self, player=None, name=None, profession=None, pos=0, color=RESET, abilities=None):
        super().__init__(player, name, profession, pos, abilities)
        self.abilities = [Charge()]
        
        self.range = 1
        self.damage = 2
        self.health = 7
        self.max_health = 7
        self.mobility = 1
        self.mana = 10
        self.max_mana = 10
        self.symbol = 'W'
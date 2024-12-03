from globalss.globals import *
from globalss.colors import *

class Map_effect:
    def __init__(self, name='MAP EFFECT', duration=0, pos=Position(0, 0), from_player=None):
        self.name = name
        self.duration = duration
        self.pos = pos
        self.from_player = from_player

class Map_Burn(Map_effect):
    symbol = '#'
    
    def __init__(self, name='MAP BURN', duration=0, pos=Position(0,0), damage=0, from_player=None):
        super().__init__(name, duration, pos, from_player)
        self.damage = damage
        
    def apply(self, target):
        if self.duration == 0 or target.health <= 0:
            return False
        if target.player != self.from_player:  
            target.health -= self.damage
            print(f"{RED}Applied {self.name} to {target.name}: -{self.damage} health!{RESET}")
        
        if self.duration == 1 or target.health <= 0:
            return False
        return True
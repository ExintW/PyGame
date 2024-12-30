from globalss.globals import *
from globalss.colors import *

class Projectile:
    def __init__(self, symbol=None, pos=None, direction=None, from_character=None, speed=None):
        self.symbol=symbol
        self.pos = pos
        self.direction=direction
        self.from_character=from_character
        self.speed=speed
    
    def move(self):
        
        for i in range(self.speed):
            
    def check_hit(self):
        if Stats.CHAR_MAP[self.pos.y][self.pos.x] is not None:
            if Stats.CHAR_MAP[self.pos.y][self.pos.x].player != self.from_character.player:
                return True
        return False
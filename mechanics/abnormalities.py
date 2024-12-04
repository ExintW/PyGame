from globalss.colors import *
from globalss.globals import *

class Abnormality:
    def __init__(self, name=None, duration=0, character=None):
        self.name = name
        self.duration = duration
        self.character = character

class Burn(Abnormality):
    def __init__(self, name='Burn', duration=0, damage=0, character=None):
        super().__init__(name, duration, character)
        
        self.damage = damage
    
    def apply(self):
        if self.duration == 0 or self.character.health <= 0:
            return False
        
        self.character.health -= self.damage
        self.duration -= 1
        Stats.DUMPS.append(f"{RED}Applied {self.name} to {self.character.name}: -{self.damage} health!{RESET}")
        
        if self.duration == 0 or self.character.health <= 0:
            return False
        return True
from player.character import *
from globals.globals import Buff_Type

class Buff:
    def __init__(self, name=None, value=0, type=Buff_Type.ATK_BUFF, duration=1):
        self.name = name
        self.value = value
        self.type = type
        self.duration = duration
    
    def apply(self):
        self.duration -= 1
        return self.value

    
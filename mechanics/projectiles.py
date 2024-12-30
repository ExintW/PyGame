from globalss.globals import *
from globalss.colors import *
from game_stats.UI_utils import *
from mechanics.abnormalities import *

import copy

class Projectile:
    def __init__(self, symbol=None, pos=None, direction=None, from_character=None, speed=None):
        self.symbol = symbol
        self.pos = pos
        self.direction = direction
        self.from_character = from_character
        self.speed = speed     
    
    def move(self):     # Returns True if hit, also removes self if out of bound
        if self.check_hit():
            self.hit()
            return True
        for i in range(self.speed):
            self.pos.x += self.direction.x
            self.pos.y -= self.direction.y
            if not check_bounds(self.pos):
                return True
            if self.check_hit():
                self.hit()
                return True
        return False
    
    def check_hit(self):
        target_player = Stats.PLAYER_LIST[0]
        if target_player == self.from_character.player:
            target_player = Stats.PLAYER_LIST[1]
        for c in target_player.avail_characters:
            if c.pos == self.pos:
                return True
        return False

class Arrow(Projectile):
    def __init__(self, name='Arrow', pos=None, direction=None, from_character=None, speed=None, damage=0, stun_duration=0, dmg_growth=0, stun_growth=0):
        if direction == Position(1, 0):
            symbol = '→'
        elif direction == Position(1, 1):
            symbol = '↗'
        elif direction == Position(0, 1):
            symbol = '↑'
        elif direction == Position(-1, 1):
            symbol = '↖'
        elif direction == Position(-1, 0):
            symbol = '←'
        elif direction == Position(-1, -1):
            symbol = '↙'
        elif direction == Position(0, -1):
            symbol = '↓'
        elif direction == Position(1, -1):
            symbol = '↘'
        else:
            symbol = 'N'
        super().__init__(symbol=symbol, pos=pos, direction=direction, from_character=from_character, speed=speed)
        self.damage = damage
        self.stun_duration = stun_duration
        self.name = name
        self.init_pos = copy.deepcopy(pos)
        self.dmg_growth = dmg_growth
        self.stun_growth = stun_growth
    
    def hit(self):
        target = Stats.CHAR_MAP[self.pos.y][self.pos.x]
        if target is None:
            print(f"{RED}Error in Arrow: no character in this position!{RESET}")
            return False
        if target.health > 0:
            # Calculate dmg
            x_diff = abs(self.pos.x - self.init_pos.x)
            y_diff = abs(self.pos.y - self.init_pos.y)
            larger_diff = x_diff
            if y_diff > x_diff:
                larger_diff = y_diff
            self.damage += int(larger_diff * self.dmg_growth)
            self.stun_duration += int(larger_diff * self.stun_growth)
            
            target.health -= self.damage
            
            # Add stun to target
            stun = Stun(name='Arrow Stun', duration=self.stun_duration)
            exist = False
            if len(target.abnormalities) > 0:
                name = stun.name
                for abnorm in target.abnormalities:
                    if abnorm.name == name:
                        abnorm.duration += stun.duration
                        exist = True
            if not exist:
                ab_copy = copy.deepcopy(stun)
                target.abnormalities.append(ab_copy)
                ab_copy.character = target
            
            Stats.DUMPS.append(f"{CYAN}{self.damage} damage dealt to {target.name}{RESET}")
            Stats.DUMPS.append(f"{CYAN}{self.stun_duration} rounds of Stun applied to {target.name}{RESET}")
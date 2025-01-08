from enum import Enum, auto
from dataclasses import dataclass

RAGE_DEF_BUFF_NAME = 'Rage DEF Buff'
MAX_RAGE_BUFF_NAME = 'Max Rage Buff'

class Buff_Type(Enum):
    ATK_BUFF = 'Attack Buff'
    ATK_DEBUFF = 'Attack DeBuff'
    DEF_BUFF = 'Defence Buff'
    DEF_DEBUFF = 'Defence DeBuff'
    BOOST_BUFF = 'Boost Buff'
    BOOST_DEBUFF = 'Boost DeBuff'
    RANGE_BUFF = 'Range Buff'
    RANGE_DEBUFF = 'Range DeBuff'

class Sig_Type(Enum):
    SINGLE_USE = 'Single Use'
    CONTINUOUS = 'Continuous'

class Ability_Type(Enum):
    ATK_ABIL = 'Attack Ability'
    BUFF_ABIL = 'Buff Ability'
    AB_ABIL = 'Abnormality Ability'
    SIG_ABIL = 'Signiture Ability'
    HEAL_ABIL = 'Heal Ability'
    
class AB_Type(Enum):
    BURN = 'Burn'
    STUN = 'Stun'
    ROOT = 'Root'

@dataclass
class Position:
    x : int
    y : int

class Stats:
    ROUND = 1
    CUR_MOVE = 'p1'
    NAME_TO_PLAYER_MAP = {}
    PLAYER_LIST = []
    MAP_SIZE = Position(11, 9)
    MAP = [[]]
    COLOR_COORD = {}   # Used for coloring in 2D Map
    MAP_EFFECT_LIST = []
    EFFECT_MAP = [[[]]] # Need to clean up self for each effect (Not Refreshing every round)
    CHAR_MAP = [[]]
    PROJECTILE_LIST = []
    PROJ_MAP = [[[]]]   
    DUMPS = []
    CHAR_COPY_LIST_FOR_RAGE = []
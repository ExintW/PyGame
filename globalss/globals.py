from enum import Enum, auto
from dataclasses import dataclass

class Buff_Type(Enum):
    ATK_BUFF = 'Attack Buff'
    ATK_DEBUFF = 'Attack DeBuff'
    DEF_BUFF = 'Defence Buff'
    DEF_DEBUFF = 'Defence DeBuff'
    BOOST_BUFF = 'Boost Buff'
    BOOST_DEBUFF = 'Boost DeBuff'
    RANGE_BUFF = 'Range Buff'
    RANGE_DEBUFF = 'Range DeBuff'

class Ability_Type(Enum):
    ATK_ABIL = 'Attack Ability'
    BUFF_ABIL = 'Buff Ability'

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
    PLAYER_COORD = {}   # Used for coloring in 2D Map
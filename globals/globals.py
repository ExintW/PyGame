from enum import Enum, auto

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

ROUND = 1
CUR_MOVE = 'p1'
NAME_TO_PLAYER_MAP = {}
PLAYER_LIST = []
MAP_SIZE = 21 # -10 -> 10
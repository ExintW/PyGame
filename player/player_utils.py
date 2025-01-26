from globalss.globals import *

def apply_dmg_buff(source, dmg=0):
    if dmg == 0:
        damage = source.damage
    else:
        damage = dmg
    
    for buff in source.buff[Buff_Type.ATK_BUFF].copy():
        damage += buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.ATK_BUFF].remove(buff)
    for buff in source.buff[Buff_Type.ATK_DEBUFF].copy():
        damage -= buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.ATK_DEBUFF].remove(buff)
    return damage

def apply_def_buff(source, target, dmg=0):    # for samurai aoe atk
    if dmg == 0:
        damage = source.damage
    else:
        damage = dmg
    
    for buff in target.buff[Buff_Type.DEF_BUFF].copy():
        damage -= buff.apply()
        if buff.duration < 1:
            target.buff[Buff_Type.DEF_BUFF].remove(buff)
    for buff in target.buff[Buff_Type.DEF_DEBUFF].copy():
        damage += buff.apply()
        if buff.duration < 1:
            target.buff[Buff_Type.DEF_DEBUFF].remove(buff)
    
    return damage

def apply_dmg_def_buff(source, target, dmg=0):
    if dmg == 0:
        damage = source.damage
    else:
        damage = dmg
    
    for buff in source.buff[Buff_Type.ATK_BUFF].copy():
        damage += buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.ATK_BUFF].remove(buff)
    for buff in source.buff[Buff_Type.ATK_DEBUFF].copy():
        damage -= buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.ATK_DEBUFF].remove(buff)
    for buff in target.buff[Buff_Type.DEF_BUFF].copy():
        damage -= buff.apply()
        if buff.duration < 1:
            target.buff[Buff_Type.DEF_BUFF].remove(buff)
    for buff in target.buff[Buff_Type.DEF_DEBUFF].copy():
        damage += buff.apply()
        if buff.duration < 1:
            target.buff[Buff_Type.DEF_DEBUFF].remove(buff)
    
    return damage

def calculate_move(source):
    dist = 0
    for buff in source.buff[Buff_Type.BOOST_BUFF].copy():
        dist += buff.value
    for buff in source.buff[Buff_Type.BOOST_DEBUFF].copy():
        dist -= buff.value
    return dist

def apply_boost_buff(source):
    for buff in source.buff[Buff_Type.BOOST_BUFF].copy():
        buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.BOOST_BUFF].remove(buff)
    for buff in source.buff[Buff_Type.BOOST_DEBUFF].copy():
        buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.BOOST_DEBUFF].remove(buff)
            
def buff_range(source):
    range = 0
    if hasattr(source, 'range_shot') and source.range_shot:
        range += 1
    for buff in source.buff[Buff_Type.RANGE_BUFF].copy():
        range += buff.value
    for buff in source.buff[Buff_Type.RANGE_DEBUFF].copy():
        range -= buff.value
    return range

def apply_range_buff(source):
    if hasattr(source, 'range_shot') and source.range_shot:
        source.range_shot = False
        source.range_shot_count = 0
    for buff in source.buff[Buff_Type.RANGE_BUFF].copy():
        buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.RANGE_BUFF].remove(buff)
    for buff in source.buff[Buff_Type.RANGE_DEBUFF].copy():
        buff.apply()
        if buff.duration < 1:
            source.buff[Buff_Type.RANGE_DEBUFF].remove(buff)

def pos_diff(source, target):
    return max(abs(source.pos.x - target.pos.x), abs(source.pos.y - target.pos.y))
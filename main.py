from player.character import *
from player.classes import *
from globalss.globals import *
from globalss.colors import *
from game_stats.prompt import *
from game_stats.game_stats import *
from game_stats.UI_utils import *
from mechanics.abilities import *
from player.player import Player

import sys

p1 = Player(name='P1', color=BLUE)
p2 = Player(name='P2', color=RED)
p1_Archer = Archer(player=p1, name='p1 Archer', profession='ARCHER', pos=Position(3, 3))
p1_Warrior = Warrior(player=p1, name='p1 Warrior', profession='WARRIOR', pos=Position(3, 4))
p1_Mage = Mage(player=p1, name='p1 Mage', profession='MAGE', pos=Position(3, 5))

p2_Archer = Archer(player=p2, name='p2 Archer', profession='ARCHER', pos=Position(7, 4))
p2_Warrior = Warrior(player=p2, name='p2 Warrior', profession='WARRIOR', pos=Position(7, 3))
p2_Mage = Mage(player=p2, name='p2 Mage', profession='MAGE', pos=Position(7, 5))


p1.characters = [p1_Archer, p1_Warrior, p1_Mage]
p1.avail_characters = p1.characters
p2.characters = [p2_Warrior, p2_Archer, p2_Mage]
p2.avail_characters = p2.characters

# p1 = get_player_info(1)
# p2 = get_player_info(2)

# Initialize global/player lists and maps
init_lists_and_maps(p1, p2)

# Initialize Map
init_map()

print(f"{BLUE}-----------------Version 1.0-----------------{RESET}")


while(1):
    
    if Stats.CUR_MOVE == 'p1':
        # p1 round
        for c in p1.avail_characters:
            print_players_stats()
            init_map()
            divide_line()
            print_map_2D()
            print(f'{YELLOW}ROUND: {Stats.ROUND}{RESET}')
            prompt_move(c, p2)
            check_characters()
            if check_end():
                sys.exit()
    else:
        # p2 round
        for c in p2.avail_characters:
            print_players_stats()
            init_map()
            divide_line()
            print_map_2D()
            print(f'{YELLOW}ROUND: {Stats.ROUND}{RESET}')
            prompt_move(c, p1)
            check_characters()
            if check_end():
                sys.exit()

    Stats.ROUND += 1
    if Stats.CUR_MOVE == 'p1':
        Stats.CUR_MOVE = 'p2'
    else:
        Stats.CUR_MOVE = 'p1'
    
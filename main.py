from player.character import *
from player.classes import *
from globals.globals import *
from globals.colors import *
from game_stats.prompt import *
from game_stats.game_stats import *
from game_stats.UI_utils import *
from mechanics.abilities import *
from player.player import Player


p1 = Player(name='p1', color=BLUE)
p2 = Player(name='p2', color=RED)
p1_Archer = Archer(player=p1, name='p1 Archer', profession='ARCHER', pos=Position(4, 5), abilities=[Power_Shot(), Precision()])
p1_Warrior = Warrior(player=p1, name='p1 Warrior', profession='WARRIOR', pos=Position(4, 6), abilities=[Charge()])

p2_Archer = Archer(player=p2, name='p2 Archer', profession='ARCHER', pos=Position(8, 6), abilities=[Power_Shot(), Precision()])
p2_Warrior = Warrior(player=p2, name='p2 Warrior', profession='WARRIOR', pos=Position(8, 5), abilities=[Charge()])


p1.characters = [p1_Archer, p1_Warrior]
p1.avail_characters = p1.characters
p2.characters = [p2_Warrior, p2_Archer]
p2.avail_characters = p2.characters

# p1 = get_player_info(1)
# p2 = get_player_info(2)

PLAYER_LIST.append(p1)
PLAYER_LIST.append(p2)
NAME_TO_PLAYER_MAP[p1.name] = p1
NAME_TO_PLAYER_MAP[p2.name] = p2


print(f"{BLUE}-----------------Version 1.0-----------------{RESET}")

print_players_stats()

# while(1):
#     divide_line()
#     print(f'{YELLOW}ROUND: {ROUND}{RESET}')
#     print_map()
#     if CUR_MOVE == 'p1':
#         # p1 round
#         prompt_move(p1)
#     else:
#         # p2 round
#         prompt_move(p2)
    
#     print_players_stats()
    
#     if check_end():
#         break

#     ROUND += 1
#     if CUR_MOVE == 'p1':
#         CUR_MOVE = 'p2'
#     else:
#         CUR_MOVE = 'p1'
    
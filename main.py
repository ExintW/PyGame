from player.player import *
from player.classes import *
from globals.globals import *
from globals.colors import *
from game_stats.prompt import *
from game_stats.game_stats import *
from game_stats.UI_utils import *
from mechanics.abilities import *

p1 = Archer('p1', 'ARCHER', -1, BLUE)
p2 = Warrior('p2', 'WARRIOR', 1, RED)

# p1 = get_player_info(1)
# p2 = get_player_info(2)

PLAYER_LIST.append(p1)
PLAYER_LIST.append(p2)
NAME_TO_PLAYER_MAP[p1.name] = p1
NAME_TO_PLAYER_MAP[p2.name] = p2

print(f"{BLUE}-----------------Version 1.0-----------------{RESET}")

print_players_stats()

while(1):
    divide_line()
    print(f'{YELLOW}ROUND: {ROUND}{RESET}')
    print_map()
    if CUR_MOVE == 'p1':
        # p1 round
        prompt_move(p1)
    else:
        # p2 round
        prompt_move(p2)
    
    print_players_stats()
    
    if check_end():
        break

    ROUND += 1
    if CUR_MOVE == 'p1':
        CUR_MOVE = 'p2'
    else:
        CUR_MOVE = 'p1'
    
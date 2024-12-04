from player.character import *
from player.classes import *
from globalss.globals import *
from game_stats.UI_utils import *
from game_stats.game_stats import *

def get_player_info(num):
    while (1):
        text = input(f"{GREEN}Enter the name and class of player {num}: {RESET}").split()
        if text[1].upper() == 'ARCHER':
            return Archer(text[0], text[1].upper(), -1)
        elif text[1].upper() == 'WARRIOR':
            return Warrior(text[0], text[1].upper(), -1)
        else:
            print(f'{RED}Wrong player info!{RESET}')

def main_prompt(player, opponent):
    apply_map_effects() 
    for c in player.avail_characters:  
        check_characters()
        init_map()
        print_players_stats()
        divide_line()
        dump_info()
        clear_dump()
        print_map_2D()
        print(f'{YELLOW}ROUND: {Stats.ROUND}{RESET}')
        prompt_move(c, opponent)
        check_characters()
        if check_end():
            return False
        init_map()
        divide_line()
    return True

def prompt_move(c, target):
    """
    Prompt format:
        MOVE:
            "mov <del_x> < <del_y>" (can be pos or neg)
        ATTACK:
            "atk <target character symbol>"
        ABILITIES:
            "abl <ability number> <player> <char symbol>"
            "abl <ability number>"  -> for self buff abilities
        END:
            "end"
    """
    while(1):
        end_round = False
        text = input(f'{GREEN}Enter the action for {RESET}{c.color}{c.name}{RESET}{GREEN} (MOV, ATK, ABL, SIG, END): {RESET}').split()
        
        match text[0].upper():     # text[0].upper() is the first arg       
            case 'END':
                print(f'{CYAN}Round Ended{RESET}')
                end_round = True
                
            case 'MOV':
                try:
                    end_round = c.move(int(text[1]), -int(text[2]))
                except:
                    print(f'{RED}Error in Move!{RESET}')
            case 'ATK':
                try: 
                    end_round = c.attack(target.sym_to_char_map[text[1]])  
                except:
                    print(f'{RED}Error in Attack!{RESET}')
            case 'ABL':
                try:
                    if int(text[1]) > len(c.abilities):
                        print(f'{RED}Invalid ability number!{RESET}')
                    elif len(text) == 2 and c.abilities[int(text[1])-1].ability_type == Ability_Type.BUFF_ABIL: # For buff abilities: abl <#> -> means apply to self
                        end_round = c.abilities[int(text[1])-1].use(c, c)
                    elif len(text) == 3 and ((c.abilities[int(text[1])-1].ability_type == Ability_Type.ATK_ABIL) or (c.abilities[int(text[1])-1].ability_type == Ability_Type.AB_ABIL)):  # For atk abilities: abl <#> <char>
                        end_round = c.abilities[int(text[1])-1].use(c, target.sym_to_char_map[text[2].upper()])
                    else:
                        end_round = c.abilities[int(text[1])-1].use(c, Stats.NAME_TO_PLAYER_MAP[text[2].upper()].sym_to_char_map[text[3].upper()]) # "abil <abil #> <player> <char symbol>"
                except:
                    print(f'{RED}Error in Ability!{RESET}')
            case 'SIG':
                try:
                    end_round = c.sig_ability.use(from_player=c.player)
                except:
                    print(f'{RED}Error in Sig Ability!{RESET}')
            case _:
                print(f'{RED}Invalid Move!{RESET}')
            
        if end_round:
            c.apply_abnormalities()
            return
from player.character import *
from player.classes import *
from globalss.globals import *
from game_stats.UI_utils import *
from game_stats.game_stats import *
from mechanics.abilities import *

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
    update_projectiles()
    check_init_rage()
    check_characters()
    for c in player.avail_characters:
        check_characters()
        init_map()
        check_special_mechanics(c)   # e.g. decrement sheath counter
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
        decrement_cd(c)
        init_map()
        divide_line()
    check_end_rage()
    return True

def prompt_move(c, target):
    """
    Prompt format:
        MOVE:
            "mov <del_x> <del_y>" (can be pos or neg)
        ATTACK:
            "atk <target character symbol>"
        ABILITIES:
            "abl <ability number> <player> <char symbol>"
            "abl <ability number>"  -> for self buff abilities
            "abl <ability number> <char symbol>" -> for atk or heal abilities
        SIG:
            "sig"
        END:
            "end" or "e"
    """
    while(1):
        end_round = False
        
        if c.apply_abnormalities(AB_Type.STUN):
            end_round = True
            if c.sig_ability != None:
                c.channel_counter = -1   # interrupt channeling
                c.sig_ability.rounds_used = 0
                c.sig_ability.using = False
            Stats.DUMPS.append(f'{RED}{c.name} is stunned!{RESET}')
              
        elif c.sig_ability != None and c.channel_counter != -1:
            end_round = c.sig_ability.channel()
            if not end_round:
                print(f'{RED}Signiture ability use failed!{RESET}')
            
        elif not end_round:
            text = input(f'{GREEN}Enter the action for {RESET}{c.color}{c.name}{RESET}{GREEN} (MOV, ATK, ABL, SIG, END): {RESET}').split()
            
            match text[0].upper():     # text[0].upper() is the first arg   
                case 'E':
                    print(f'{CYAN}Round Ended{RESET}')
                    end_round = True
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
                        end_round = c.attack(target.sym_to_char_map[text[1].upper()])  
                    except:
                        print(f'{RED}Error in Attack!{RESET}')
                case 'ABL':
                    try:
                        abil_type = c.abilities[int(text[1])-1].ability_type
                        if int(text[1]) > len(c.abilities):
                            print(f'{RED}Invalid ability number!{RESET}')
                        elif len(text) == 2 and (abil_type == Ability_Type.BUFF_ABIL or abil_type == Ability_Type.HEAL_ABIL): # For buff abilities: abl <#> -> means apply to self
                            end_round = c.abilities[int(text[1])-1].use(target=c)
                        elif len(text) == 3 and ((abil_type == Ability_Type.ATK_ABIL) or (abil_type == Ability_Type.AB_ABIL)):  # For atk abilities: abl <#> <char> -> apply to enemy <char>
                            end_round = c.abilities[int(text[1])-1].use(target=target.sym_to_char_map[text[2].upper()])
                        elif len(text) == 3 and (abil_type == Ability_Type.HEAL_ABIL or abil_type == Ability_Type.BUFF_ABIL):   # For buff and heal abilities: abl <#> <char> -> apply to ally <char>
                            end_round = c.abilities[int(text[1])-1].use(target=c.player.sym_to_char_map[text[2].upper()])
                        else:
                            end_round = c.abilities[int(text[1])-1].use(target=Stats.NAME_TO_PLAYER_MAP[text[2].upper()].sym_to_char_map[text[3].upper()]) # "abil <abil #> <player> <char symbol>"
                    except:
                        print(f'{RED}Error in Ability!{RESET}')
                case 'SIG':
                    try:
                        end_round = c.sig_ability.channel()
                    except:
                        print(f'{RED}Error in Sig Ability!{RESET}')
                case _:
                    print(f'{RED}Invalid Move!{RESET}')
            
        if end_round:
            c.apply_abnormalities(AB_Type.BURN)
            return
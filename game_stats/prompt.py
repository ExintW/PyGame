from player.player import *
from player.classes import *
from globals.globals import *

def get_player_info(num):
    while (1):
        text = input(f"{GREEN}Enter the name and class of player {num}: {RESET}").split()
        if text[1].upper() == 'ARCHER':
            return Archer(text[0], text[1].upper(), -1)
        elif text[1].upper() == 'WARRIOR':
            return Warrior(text[0], text[1].upper(), -1)
        else:
            print(f'{RED}Wrong player info!{RESET}')

def prompt_move(player):
    """
    Prompt format:
        MOVE:
            "mov <steps>" (steps can be pos or neg)
        ATTACK:
            "atk <target name>"
        ABILITIES:
            "abl <ability number> <target name>
    """
    while(1):
        end_round = False
        text = input(f'{GREEN}Enter the action for {RESET}{player.color}{player.name}{RESET}{GREEN} (MOV, ATK, ABL, END): {RESET}').split()
        
        if text[0].upper() == 'END':
            print(f'{CYAN}Round Ended{RESET}')
            end_round = True
            
        elif text[0].upper() == 'MOV':
            try:
                end_round = player.move(int(text[1]))
            except:
                print(f'{RED}Error in Move!{RESET}')
        elif text[0].upper() == 'ATK':
            try: 
                end_round = player.attack(NAME_TO_PLAYER_MAP[text[1]])
            except:
                print(f'{RED}Error in Attack!{RESET}')
        elif text[0].upper() == 'ABL':
            try:
                if int(text[1]) > len(player.abilities):
                    print(f'{RED}Invalid ability number!{RESET}')
            except:
                print(f'{RED}Invalid ability number!')
            else:
                try:
                    end_round = player.abilities[int(text[1])-1].use(player, NAME_TO_PLAYER_MAP[text[2]])
                except:
                    print(f'{RED}Error in Ability!{RESET}')
        else:
            print(f'{RED}Invalid Move!{RESET}')
        
        if end_round:
            return
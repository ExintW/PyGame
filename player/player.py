from globalss.globals import *
from globalss.colors import *

class Player:
    def __init__(self, name=None, color=RESET, characters=None, sym_to_char_map=None):
        self.name=name
        self.color=color
        self.characters=characters
        self.avail_characters = characters
        self.sym_to_char_map = sym_to_char_map
        
    def print_char_stat(self):
        print(f"{YELLOW}{BOLD}{self.name}:{RESET}")
        for char in self.avail_characters:
            char.print_stat()
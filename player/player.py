from globals.globals import *
from globals.colors import *

class Player:
    def __init__(self, name=None, color=RESET, characters=None):
        self.name=name
        self.color=color
        self.characters=characters
        self.avail_characters = characters
        
    def print_char_stat(self):
        print(f"{YELLOW}{BOLD}{self.name}:{RESET}")
        for char in self.avail_characters:
            char.print_stat()
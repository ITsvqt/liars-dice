
import random
from collections import Counter
from utility import try_parse_int
from player.human_player import HumanPlayer
from player.ai_player import AIPlayer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player.base.player import Player

ai_players = {
    "Captain Blackbeard"     : 0.75, # big bluffer
    "Naga Seawitch"          : 0.55, # balanced
    "Devil Itslef"           : 0.66, # a bit cocky
    "The Pope"               : 0.33, # safe player
    "Little Red Riding Hood" : 0.50  # dzen
}


class Game:
    
    def __init__(self):
        self.players: list[Player] = []
        self.all_dice_values: Counter = None
        self.curr_player_idx = 0
        
        self.set_up()
        
        
    def set_up(self):
        self._add_human_player()
        self._add_ai_players()
        
        random.shuffle(self.players)

    def game_loop(self):
        
        while True:
            ...
            
            
            #TODO : 1st turn index 0 in player's list
            #TODO : loser of round starts firts in the next round
            #TODO : if loser gets eliminated, next index in the player's list is first
            



    def _add_human_player(self):
        humanp_name = input("Enter your battle name (Captain): ")
        self.players.append(HumanPlayer(humanp_name))
        
        
    def _add_ai_players(self):
        
        while True:
            try:
                aip_cnt = try_parse_int(input("Enter count of AI enemies [1:5](2): "))
                if not 1 <= aip_cnt <= 5:
                    raise ValueError(f"Illegal opponents count[1:5]: {aip_cnt}")
                break
            except ValueError as e:
                print(e.args[0])
                
        for ai_token in random.sample(list(ai_players.items()), aip_cnt):
            self.players.append(AIPlayer(ai_token[0], ai_token[1]))
                
                
        

import random
from collections import Counter
from typing import TYPE_CHECKING

from engine.player_circle import PlayerCircle
from engine.rules import LiarsDiceRules
from utility.parsing import try_parse_int
from models.player.human_player import HumanPlayer
from models.player.ai_player import AIPlayer

if TYPE_CHECKING:
    from models.player.base.player import Player

AI_PLAYERS = {
    "Captain Blackbeard"     : 0.75, # big bluffer
    "Naga Seawitch"          : 0.55, # balanced
    "Devil Itslef"           : 0.66, # a bit cocky
    "The Pope"               : 0.33, # safe player
    "Little Red Riding Hood" : 0.50  # dzen
}


class Game:
    
    def __init__(self):
        self.players: list[Player] = self._set_up()
        self.player_circle = PlayerCircle(self.players)
        #! use scope var instead
        self.all_dice_values: Counter = None
        
        self.turn_cnt = 0
        
        
        
    def _set_up(self) -> list[Player]:
        """Create players and return them in shuffled order."""
        
        #todo: use name as UID, by first creating bots and then asking for player name
        player_list: list[Player] = (
            [self._create_human_player()]
            + self._create_ai_players()
        )
        
        random.shuffle(player_list)
        return player_list
        

    def game_loop(self):

        while True:

            ...
            #TODO : doubly linked circular list for data
            #TODO : pick bots, and then ask user for unique name
            
            #TODO : loser of round starts firts in the next round
            #TODO : if loser gets eliminated, next index in the player's list is first
            
            #TODO : implement human.take_turn
            #TODO : implement AI.take_turn

            

        
        
        
            



    def _create_human_player(self) -> Player:
        humanp_name = input("Enter your battle name (Captain): ")
        return HumanPlayer(humanp_name)
        
        
    def _create_ai_players(self) -> list[Player]:
        while True:
            try:
                max_ai_cnt = LiarsDiceRules.CNT_MAX_PLAYER - 1
                aip_cnt = try_parse_int(input(f"Enter count of AI enemies [1:{max_ai_cnt}](2): "))
                if not 1 <= aip_cnt <= 5:
                    raise ValueError(f"Illegal opponents count[1:{max_ai_cnt}]: {aip_cnt}")
                break
            except ValueError as e:
                print(e.args[0])
                
        return [
            AIPlayer(name, aggression)
            for name, aggression
            in random.sample(list(AI_PLAYERS.items()), aip_cnt)
            ]
                
                
        
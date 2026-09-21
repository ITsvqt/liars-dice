
import random
from collections import Counter
from utility.parsing import try_parse_int
from models.player.human_player import HumanPlayer
from models.player.ai_player import AIPlayer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.models.player.base.player import Player

ai_players = {
    "Captain Blackbeard"     : 0.75, # big bluffer
    "Naga Seawitch"          : 0.55, # balanced
    "Devil Itslef"           : 0.66, # a bit cocky
    "The Pope"               : 0.33, # safe player
    "Little Red Riding Hood" : 0.50  # dzen
}


class Game:
    
    def __init__(self):
        self.players: dict[int, Player] = self.set_up()
        
        #! use scope var instead
        self.all_dice_values: Counter = None
        
        self.turn_cnt = 0
        
        self.active_players: list[int] = [i for i in range(len(self.players))]
        
        
    def set_up(self) -> dict[int, Player]:
        """Create players, return player_idx:Player """
        
        player_list: list[Player] = (
            [self._create_human_player()]
            + self._create_ai_players()
        )
        
        return {
            i: p
            for i, p
            in enumerate(random.shuffle(player_list))
        }


    def game_loop(self):
        
        starting_player_idx = 0
        while True: # while len(active_player) != 1:
            #self._play_round(starting_player_idx)
            player_order = [idx for idx in self.active_players]
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
                aip_cnt = try_parse_int(input("Enter count of AI enemies [1:5](2): "))
                if not 1 <= aip_cnt <= 5:
                    raise ValueError(f"Illegal opponents count[1:5]: {aip_cnt}")
                break
            except ValueError as e:
                print(e.args[0])
                
        return [
            AIPlayer(name, aggression)
            for name, aggression
            in random.sample(list(ai_players.items()), aip_cnt)
            ]
                
                
        
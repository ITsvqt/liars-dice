
import random
from collections import Counter
from typing import TYPE_CHECKING

from engine.player_circle import PlayerCircle
from engine.rules import LiarsDiceRules
from utility.type_parsing import try_parse_int
from models.player.human_player import HumanPlayer
from models.player.ai_player import AIPlayer

if TYPE_CHECKING:
    from models.player.base.player import Player
    from ui.base.ui import GameUI

AI_PLAYERS = {
    "Captain Blackbeard"     : 0.75, # big bluffer
    "Naga Seawitch"          : 0.55, # balanced
    "Devil Itslef"           : 0.66, # a bit cocky
    "The Pope"               : 0.33, # safe player
    "Little Red Riding Hood" : 0.50  # dzen
}


class Game:
    
    def __init__(self, ui: GameUI):
        
        self.ui = ui
        self.player_circle = PlayerCircle(self._set_up())
        self.turn_cnt = 0
        

        

    def game_loop(self):

        cnt = 0
        while not LiarsDiceRules.is_game_over(self.player_circle):
            self._play_round()
            
            if cnt > 5:
                break
            cnt += 1
            print()
            print('-----------')
            print()
            
            #TODO : doubly linked circular list for data
            #TODO : pick bots, and then ask user for unique name
            
            #TODO : loser of round starts firts in the next round
            #TODO : if loser gets eliminated, next index in the player's list is first
            
            #TODO : implement human.take_turn
            #TODO : implement AI.take_turn

    def _play_round(self):
        print(self.player_circle.get_players_dice_face_cnt().items())


    def _set_up(self) -> list[Player]:
        """Create players and shuffle them in random order"""
        
        ai_players: list[Player] = self._create_ai_players()
        human_player: Player = self._create_human_player([p.name for p in ai_players])
        
        ai_players.append(human_player)
        
        random.shuffle(ai_players)
        return ai_players
    
    
    def _create_ai_players(self) -> list[Player]:
        
        max_ai_cnt = LiarsDiceRules.CNT_MAX_PLAYER - 1
        
        while True:
            aip_cnt = self.ui.ask_ai_count(1, max_ai_cnt, 2)
            
            if 1 <= aip_cnt <= max_ai_cnt:
                return [
                    AIPlayer(name, aggression)
                    for name, aggression
                    in random.sample(list(AI_PLAYERS.items()), aip_cnt)
                ] 
                
            self.ui.show_message(f"Illegal opponents count[1:{max_ai_cnt}]: {aip_cnt}")
            
            
    def _create_human_player(self, reserved_names: list[int]) -> Player:
        
        while True:
            human_p_name = self.ui.ask_player_name("Captain")
            
            if human_p_name not in reserved_names:
                return HumanPlayer(human_p_name)
                
            self.ui.show_message(f"'{human_p_name}' is already taken")
        

                
        


import random
from typing import TYPE_CHECKING

from engine.player_circle import PlayerCircle
from engine.rules import LiarsDiceRules
from utility.type_parsing import try_parse_int
from models.player.human_player import HumanPlayer
from models.player.ai_player import AIPlayer

if TYPE_CHECKING:
    from models.player.base.player import Player
    from ui.base.ui import GameUI
    from collections import Counter

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
        self.human_player: HumanPlayer = None
        self.players:  list[Player] = self._set_up()
        self.player_circle = PlayerCircle(self.players)
        self.turn_cnt: int = 0
        

        

    def game_loop(self):

        while not LiarsDiceRules.is_game_over(self.player_circle):
            self._play_round()


    def _play_round(self):
        
        #setup
        dice_face_cnt: Counter = self.player_circle.get_players_dice_roll_face_cnt()
        dice_cnt = sum(dice_face_cnt.values())
        
        current_bid = None        
        
        #action
        while True:
            """Until players call previous is bluffing"""
            player = self.player_circle.current_player
            
            while True:
                """Until valid move"""
                
                # move: tuple[str, Bid | None] => ("Call", None); ("Bid", Bid)
                if player.IS_BOT:
                    move = player.take_turn(current_bid)
                else:
                    move = self.ui.ask_move(current_bid)
                
            
                
            
                
                
            
        
        
        print(self.player_circle.get_players_dice_roll_face_cnt().items())
        #: get dict of dice face values
        #TODO: ask player to make a turn, make bid or call out
        #TODO: 1 . bid -> catch validation of invalid bid, catch validation of rules bid, show message and redo
        #TODO:     player_circle.advance_player()
        #TODO  2 . call_out -> determine who loses, the one calling bluff or the one who made the bid
        #TODO:     decrease their dices 
        #* struct handles that just provide the flag on removing
        


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
                h_p = HumanPlayer(human_p_name)
                self.human_player = h_p
                return 
                
            self.ui.show_message(f"'{human_p_name}' is already taken")
        

                
        

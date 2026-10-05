
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.player.base.player import Player
    from models.bid import Bid

from ui.base.ui import GameUI



class WebUI(GameUI):
    
    def __init__(self):
        self.state = {
            "players": [],
            "current_player": None,
            "current_bid": None,
            "phase": None
        }
    ...

    #TODO: show methods change the state 
    #TODO: get methods awaits for response, use events to effectively not waste while True CPU time

    def initiate(self):
        """Start UI"""
        ...
        
    def show_prestart(self, players: list[Player], wild_ones: bool):
        """Show initial game state"""
        ...  
    
    def show_round(self, round_num: int, active_players: list[Player], wild_ones: bool):
        """Update UI to round start state"""
        ...
        
    def show_turn_header(self, current_player: Player):
        ... 
    
    def show_turn(self,  player_name: str, bid: Bid | None):
        """Update UI to turn state"""
        ...
        
    def show_reveal(self, active_players: list[Player], wild_ones: bool):
        """Update UI to round end state"""
        ...

    def show_round_result(
        self,
        loser_name: str,
        loser_is_bot: bool,
        eliminated: bool,
        bid: Bid,
        challenger_name: str,
        challenge_valid: bool):
        """Update UI to round result state"""
        ...
        
    def show_winner(self, player: Player):
        """Update UI to game end state"""
        ...
        
        
    def get_setup_vars(
        self,
        min_ai_cnt: int,
        max_ai_cnt: int,
        suggested_ai_cnt: int,
        reserved_names: set[str]
        ) -> dict:
        """
        Return:
            cnt_ai: int
            player_name: str
            wild_ones: True | False
        """
        return 0
    
    def ask_player_move(self,
        current_bid: Bid,
        player: Player,
        dice_cnt: int,
        wild_ones: bool = False
        )-> tuple[str, tuple[int, int] | None]:
        """UI should limit player for making Challenge move when there is no initial Bid\n
        Should display current Bid and Dice_cnt\n
        Returns ("Challenge", None) | ("Bid", (face, quantity))"""
        ...
    
    def show_message(self, msg: str):
        ...
        
    def show_error(self, error_msg: str):
        ...
        
    def ask_confirmation(self, msg: str):
        ...

from __future__ import annotations
from typing import TYPE_CHECKING
import threading

if TYPE_CHECKING:
    from models.player.base.player import Player
    from models.bid import Bid

from ui.base.ui import GameUI



class WebUI(GameUI):
    
    def __init__(self):
        
        #* Browser info
        self.state = {
            "round": None,
            "players": [],
            "current_player": None,
            "current_bid": None,
            "dice_count": None,
            "wild_ones": False,
            "message": None,
            "winner": None,
        }
        
        #* Setup
        self.setup_event = threading.Event()
        self.setup_data: dict | None = None

        #* Player move
        self.move_event = threading.Event()
        self.move_data = None


    def get_setup_vars(self) -> dict:
        """
        Return:
            cnt_ai: int
            player_name: str
            wild_ones: True | False
        """
        
        self.setup_event.wait()
        return self.setup_data
    
    #TODO: show methods change the state 
    #TODO: get methods awaits for response, use events to effectively not waste while True CPU time


    def show_prestart(self, players: list[Player], wild_ones: bool):
        """Show initial game state"""
        self.state["players"] = players
        self.state["wild_ones"] = wild_ones
    
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
        
        

    def ask_player_move(self,
        current_bid: Bid,
        player: Player,
        dice_cnt: int,
        wild_ones: bool = False
        )-> tuple[str, tuple[int, int] | None]:
        """UI should limit player for making Challenge move when there is no initial Bid\n
        Should display current Bid and Dice_cnt\n
        Returns ("Challenge", None) | ("Bid", (face, quantity))"""
        
        
        
    
    def show_message(self, msg: str):
        ...
        
    def show_error(self, error_msg: str):
        self.state["error"] = error_msg
        
    def ask_confirmation(self, msg: str):
        ...
        
        
    def initiate(self):
        """Start UI"""
        ...
        
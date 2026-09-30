from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.bid import Bid
    from models.player.base.player import Player

from abc import ABC, abstractmethod


class GameUI(ABC):
    
    @abstractmethod
    def initiate(self):
        """Start UI"""
        ...
        
    @abstractmethod
    def start_game(self, players: list[Player], wild_ones: bool):
        """Show initial game state"""
        ...  
    
    @abstractmethod
    def show_round(self, round_num: int, players: list[Player], wild_ones: bool):
        """Update UI to round start state"""
        ...
        
    @abstractmethod
    def show_turn(self, player_name: str, is_bot: bool):
        """Update UI to turn state"""
        ...
        
    @abstractmethod
    def show_reveal(self, players: list[Player], wild_ones: bool):
        """Update UI to round end state"""
        ...

    @abstractmethod
    def show_round_result(self, loser_name: str, loser_is_bot: bool, eliminated: bool, bid_str: str, challenger_name: str, bid_valid: bool):
        """Update UI to round result state"""
        ...
        
    @abstractmethod
    def show_winner(self, player_name: str, is_bot: bool):
        """Update UI to game end state"""
        ...
        
        
    @abstractmethod
    def get_set_up_vars(self, min_ai_cnt: int, max_ai_cnt: int, suggested_ai_cnt) -> dict:
        """
        Return:
            cnt_ai: int
            player_name: str
            wild_ones: True | False
        """
        ...
    
    @abstractmethod
    def ask_player_move(self,
        current_bid: Bid,
        player_dice: list[int],
        dice_cnt: int,
        wild_ones: bool = False
        )-> tuple[str, tuple[int, int] | None]:
        """UI should limit player for making Challenge move when there is no initial Bid\n
        Should display current Bid and Dice_cnt\n
        Returns ("Challenge", None) | ("Bid", (face, quantity))"""
        ...
    
    @abstractmethod
    def show_message(self, msg: str):
        ...
    
    @abstractmethod
    def ask_confirmation(self, msg: str):
        ...
        


    
    
        
        
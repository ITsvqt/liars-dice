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
    def show_prestart(self, players: list[Player], wild_ones: bool):
        """Show initial game state"""
        ...  
    
    @abstractmethod
    def show_round(self, round_num: int, active_players: list[Player], wild_ones: bool):
        """Update UI to round start state"""
        ...
        
    @abstractmethod
    def show_turn_header(self, current_player: Player):
        ... 
    
    @abstractmethod
    def show_turn(self,  palyer: Player, bid: Bid | None):
        """Update UI to turn state"""
        ...
        
    @abstractmethod
    def show_reveal(self, active_players: list[Player], wild_ones: bool):
        """Update UI to round end state"""
        ...

    @abstractmethod
    def show_round_result(
        self,
        loosing_player: Player,
        is_eliminated: bool,
        bid: Bid,
        challenger_player: Player,
        is_challenge_valid: bool):
        """Update UI to round result state"""
        ...
        
    @abstractmethod
    def show_winner(self, player: Player):
        """Update UI to game end state"""
        ...
        
        
    @abstractmethod
    def get_setup_vars(self) -> dict:
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
        player: Player,
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
    def show_error(self, error_msg: str):
        ...
        
    @abstractmethod
    def ask_confirmation(self, msg: str):
        ...
        


    
    
        
        
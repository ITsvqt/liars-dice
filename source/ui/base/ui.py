from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.bid import Bid

from abc import ABC, abstractmethod


class GameUI(ABC):
    
    @abstractmethod
    def ask_player_move(self,
        current_bid: Bid,
        player_dice: list[int],
        dice_cnt: int
        )-> tuple[str, tuple[int, int] | None]:
        """UI should limit player for making Challenge move when there is no initial Bid\n
        Should display current Bid and Dice_cnt\n
        Returns ("Challenge", None) | ("Bid", (face, quantity))"""
        ...
    
    @abstractmethod
    def show_message(self, msg: str):
        ...
    
    @abstractmethod
    def ask_confirmation(self):
        ...
        
    @abstractmethod
    def ask_ai_count(self, min: int, max: int, suggestion: int) -> int:
        ...
        
    @abstractmethod
    def ask_player_name(self, suggestion: str) -> str:
        ...



    
    
        
        
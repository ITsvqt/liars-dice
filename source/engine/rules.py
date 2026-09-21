from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.bid import Bid
    from engine.player_circle import PlayerCircle

class LiarsDiceRules:
    
    @classmethod
    def is_bid_correct(cls, bid: Bid, face_count: dict[int,int], wild_ones: bool = False) -> bool:
        """Bid is valid if dice quantity for die face - is not greater than the actual."""
        dice_cnt_for_bid_face = face_count[bid.face_value]
        
        if wild_ones is True and bid.face_value != 1:
            dice_cnt_for_bid_face += face_count[1]
        
        return dice_cnt_for_bid_face >= bid.quantity
    
    @classmethod
    def is_game_over(cls, players: PlayerCircle):
        """Game ends when 1 player is remaining"""
        return players.count == 1
        
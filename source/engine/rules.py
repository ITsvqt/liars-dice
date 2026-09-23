from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections import Counter
    from models.bid import Bid
    from engine.player_circle import PlayerCircle

class LiarsDiceRules:
    
    CNT_MIN_PLAYERS = 2
    CNT_MAX_PLAYER = 5
    CNT_DICE_PER_PLAYER = 5
    
    @staticmethod
    def is_bid_correct(bid: Bid, face_count: Counter[int,int], wild_ones: bool = False) -> bool:
        """Bid is valid if dice quantity for die face - is not greater than the actual."""
        dice_cnt_for_bid_face = face_count[bid.face_value]
        
        if wild_ones is True and bid.face_value != 1:
            dice_cnt_for_bid_face += face_count[1]
        
        return dice_cnt_for_bid_face >= bid.quantity
    
    @staticmethod
    def is_game_over(players: PlayerCircle):
        """Game ends when 1 player is remaining"""
        return players.count == 1
    
    
        
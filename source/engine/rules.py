from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections import Counter
    from models.bid import Bid
    from engine.player_circle import PlayerCircle

class LiarsDiceRules:
    
    
    #* version with max_dice_cnt in mind, honestly the game should enforce a challenge move, honestly going beyond dice count is awesome
    # @staticmethod
    # def is_new_bid_valid(current: Bid, new: Bid, dice_cnt: int):
    #     return (new.quantity <= dice_cnt) and (current < new)
    
    @staticmethod
    def is_new_bid_valid(current: Bid, new: Bid) -> bool:
        return new > current
    
    @staticmethod
    def is_challenge_correct(bid: Bid, face_count: Counter[int,int], wild_ones: bool = False) -> bool:
        """If Bid is higher than the actual\n
        Returns: If the challenging players wins
        """
        dice_cnt_for_bid_face = face_count[bid.face_value]
        
        if wild_ones is True and bid.face_value != 1:
            dice_cnt_for_bid_face += face_count[1]
        
        return bid.quantity > dice_cnt_for_bid_face
    
    @staticmethod
    def is_game_over(players: PlayerCircle):
        """Game ends when 1 player is remaining"""
        return players.count == 1
    
    
        
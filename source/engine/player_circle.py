from dataclasses import dataclass
from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from source.models.player.base.player import Player

@dataclass
class PlayerNode:
    
    value: Player
    next: Optional[PlayerNode]
    prev: Optional[PlayerNode]
    

class PlayerCircle:
    
    def __init__(self, players: list[Player]):
        if players is None or len(players) <= 1:
            raise ValueError(f"Need atleast 2 player to init circle. Current: {players}")

        self.count = len(players)
        self.current_player: PlayerNode = None
        self._build_player_circle(players)
        
    def is_one_player_remaining(self) -> bool:
        return self.count == 1
    
    def remove_player(self, previous = False):
        """Removes current or previous."""
        
        
        
        
        
    def get_next_player(self):
        self.current_player = self.current_player.next
        
        return self.current_player.value
        
    def _build_player_circle(self, players: list[Player]):
        
        prev_n = PlayerNode(players[0])
        self.current_player = prev_n
        
        for i in range(1, len(players)):
            current_n = PlayerNode(players[i], prev=prev_n)
            prev_n.next = current_n
            prev_n = current_n
            
        current_n.next = self.current_player
        self.current_player.prev = current_n
            
        

                

    
    
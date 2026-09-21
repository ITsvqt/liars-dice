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
    """Circular doubly linked list of active players representing turn oreder."""
    
    def __init__(self, players: list[Player]):


        self.count = len(players)
        self.current_player: PlayerNode = None
        self._build_player_circle(players)

    def remove_player(self, previous = False):
        """Removes eliminated player from the circle."""
        #todo:  when player gets removed, self.current_player is removed.next
        
        
        
        
    def get_next_player(self):
        self.current_player = self.current_player.next
        
        return self.current_player.value
        
    def _build_player_circle(self, players: list[Player]):
        if players is None or len(players) <= 1:
            raise ValueError(f"Need atleast 2 player to init circle. Current: {players}")
        
        prev_node = PlayerNode(players[0])
        self.current_player = prev_node
        
        for i in range(1, len(players)):
            current_node = PlayerNode(players[i], prev=prev_node)
            prev_node.next = current_node
            prev_node = current_node
            
        current_node.next = self.current_player
        self.current_player.prev = current_node
        
    def _remove_player(self, player_node:PlayerNode):
        if self.count <= 1:
            raise ValueError("Removing player when 1 is remaining, game should have ended by now!")
        
        next_node = player_node.next
        prev_node = player_node.prev
        
        next_node.prev = prev_node
        prev_node.next = next_node
        player_node.next = player_node.prev = None
        self.count -= 1
            
        

                

    
    
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from utility.constants import CNT_MIN_PLAYERS, CNT_MAX_PLAYER


if TYPE_CHECKING:
    from models.player.base.player import Player
    
    
@dataclass
class PlayerNode:
    
    value: Player
    next: Optional[PlayerNode] = None
    prev: Optional[PlayerNode] = None
    

class PlayerCircle:
    """Circular doubly linked list of active players representing turn oreder."""
    
    def __init__(self, players: list[Player]):
        self._ensure_valid_player_count(players)
        
        self._current_player: PlayerNode = None
        self._count = len(players)
        self._build_player_circle(players)


    @property
    def current_player(self) -> Player:
        return self._current_player.value
    
    @property
    def previous_player(self) -> Player:
        return self._current_player.prev.value
    
    @property
    def all_players(self):
        res = []
        for _ in range(self._count):
            res.append(self.current_player)
            self.advance

        return res
    
    @property
    def count(self) -> int:
        return self._count


    def remove_player(self, previous: bool):
        """Removes either the current or the previous player from the game circle based on the given boolean flag."""
        
        #if previous is eliminated, current player stays, because he is after him and should start the next round
        if previous is True:
            self._remove_node_from_circle(self._current_player.prev)
            
        else: # previous is False
        # if current is removed we should advance the current player and remove the previous
        # this way the starting player of the next round is already set
            self.advance()
            self.remove_player(previous = True)
                
        
    def advance(self):
        self._current_player = self._current_player.next
        
        
    def _build_player_circle(self, players: list[Player]):

        prev_node = PlayerNode(players[0])
        self._current_player = prev_node
        
        for i in range(1, len(players)):
            current_node = PlayerNode(players[i], prev=prev_node)
            prev_node.next = current_node
            prev_node = current_node
            
        current_node.next = self._current_player
        self._current_player.prev = current_node
        
        
    def _remove_node_from_circle(self, player_node:PlayerNode):
        """Removes node from the linked list."""
        if self.count <= 1:
            raise ValueError("Removing player when 1 is remaining, game should have ended by now!")
        
        next_node = player_node.next
        prev_node = player_node.prev
        
        next_node.prev = prev_node
        prev_node.next = next_node
        player_node.next = player_node.prev = None
        self._count -= 1
        
        
        
    @staticmethod
    def _ensure_valid_player_count(players: list[Player]):
        """ Data should already be valid at this points. """
        if not players:
            raise ValueError(f"Player list cannot be None or empty. Received: {players}")
    
        if not CNT_MIN_PLAYERS <= len(players) <= CNT_MAX_PLAYER:
            raise ValueError(
                f"[Error] Illegal player count to init circle"
                f"[{CNT_MIN_PLAYERS}:{CNT_MAX_PLAYER}]."
                f"Current count: {len(players)}\n"
                f"Players:\n"
                f"\t{'\n\t'.join([f"{i}.{str(p)}" for i, p in enumerate(players,1)])}"
                )
            
    def __repr__(self):
        res = [f"\tPlayers Circle [{self.count}]:"]
        
        for i in range(self.count):
            res.append(f"\t\t[{i + 1}] {self.current_player}")
            self.advance()
            
        return "\n".join(res)
            
        

                

    
    
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING


from engine.rules import LiarsDiceRules


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
    def count(self) -> int:
        return self._count


    def remove_player(self, previous: bool = False):
        """Removes either the current or the previous player from the game circle based on the given boolean flag."""
        
        #if previous is eliminated, current player stays, because he is after him and should start the next round
        if previous is True:
            self._remove_player_from_circle(self._current_player)
        else: # remove current
        # if current is removed we should advance the current and remove the previous
        # this way the starting player of the next round is already set
            self.advance()
            self.remove_player(previous = True)
                
        
    def advance(self):
        self._current_player = self._current_player.next
        
    def get_players_dice_roll_face_cnt(self) -> Counter[int, int]:
        #- tested current player not changed after looping through all player to roll
        #- tested expected sum of face occurence == count of player dice
        #- briefly looked on the random values
        """Make all players roll and return summary of dice face cnt"""
        
        result = Counter()
        
        for _ in range(self._count):
            p = self.current_player
            p.roll()
            result.update(p.values)
            print(p.name)
            self.advance()

        return result
        

    def _build_player_circle(self, players: list[Player]):

        prev_node = PlayerNode(players[0])
        self._current_player = prev_node
        
        for i in range(1, len(players)):
            current_node = PlayerNode(players[i], prev=prev_node)
            prev_node.next = current_node
            prev_node = current_node
            
        current_node.next = self._current_player
        self._current_player.prev = current_node
        
        
    def _remove_player_from_circle(self, player_node:PlayerNode):
        """Removes eliminated player from the circle."""
        if self.count <= 1:
            raise ValueError("Removing player when 1 is remaining, game should have ended by now!")
        
        next_node = player_node.next
        prev_node = player_node.prev
        
        next_node.prev = prev_node
        prev_node.next = next_node
        player_node.next = player_node.prev = None
        self.count -= 1
        
        
    @staticmethod
    def _ensure_valid_player_count(players: list[Player]):
        if not players:
            raise ValueError(f"Player list cannot be None or empty. Received: {players}")
        
        min_cnt = LiarsDiceRules.CNT_MIN_PLAYERS
        max_cnt = LiarsDiceRules.CNT_MAX_PLAYER
        player_count = len(players)
        
        if not min_cnt <= player_count <= max_cnt:
            raise ValueError(
                f"Illegal player count to init circle[{min_cnt}:{max_cnt}]. Current count: {player_count}\n"
                f"Players:\n"
                f"\t{'\n\t'.join([f"{i}.{str(p)}" for i, p in enumerate(players,1)])}"
                )
            
        

                

    
    
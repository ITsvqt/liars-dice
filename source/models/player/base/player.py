from models.dice import Dice
from abc import ABC, abstractmethod

class Player(ABC):
    
    CNT_DICE = 5
    
    def __init__(self, name: str):
        self.name: str = name
        self.hand: list[Dice] = [Dice() for _ in range(self.CNT_DICE)]
        
    @abstractmethod
    def take_turn(self):
        ...
        
    @property
    def cnt_dice(self) -> int:
        return len(self.hand)
    
    @property
    def values(self) -> list[int]:
        """List of all player dice values."""
        self._ensure_hand_is_not_empty(Player.values)
        
        return [d.value for d in self.hand]
    
    def is_hand_empty(self) -> bool:
        return len(self.hand) == 0
    
    def roll(self):
        for die in self.hand:
            die.roll()
    
    def remove_die(self):
        self._ensure_hand_is_not_empty(self.remove_die)

        self.hand.pop()

    def __str__(self):
        return f"{f"[{type(self).__name__}]"} {self.name}"
    
    
    def _ensure_hand_is_not_empty(self, call_func: function):
        #- tested raiseError on invalid data
        if self.cnt_die == 0:
            raise ValueError(
                f"[{type(self).__name__}."
                f"{call_func.__name__}] Error: Player\'s hand is empty !"
                )
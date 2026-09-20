from random import randint

class Dice:
    """Represents a single die."""
    
    def __init__(self):
        self.value: int = 0

    def roll(self) -> int:
        self.value = randint(1, 6)
    
class Hand:
    """Represents a player's hand of dice."""

    def __init__(self, count: int = 5):
        self.dice = [Dice() for _ in range(count)]
        
        
    @property
    def cnt_die(self) -> int:
        return len(self.dice)
    
    
    @property
    def values(self) -> list[int]:
        self._ensure_hand_is_not_empty(Hand.values.__name__)
        
        return [d.value for d in self.dice]
        
        
    def roll(self):
        self._ensure_hand_is_not_empty(self.roll.__name__)
        
        for die in self.dice:
            die.roll()
            
            
    def remove_die(self):
        self._ensure_hand_is_not_empty(self.remove_die.__name__)
        
        self.dice.pop()
        
        
    def _ensure_hand_is_not_empty(self, func_name: str):
        if self.cnt_die == 0:
            raise ValueError(f"[Hand.{func_name}] Error: Player\'s hand is empty !")
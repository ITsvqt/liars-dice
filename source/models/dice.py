from random import randint

class Dice:
    """Represents a single die."""
    
    def __init__(self):
        self.value: int = 0

    def roll(self) -> int:
        self.value = randint(1, 6)
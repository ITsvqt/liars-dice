from core.dice import Hand
from abc import ABC, abstractmethod

class Player(ABC):
    
    def __init__(self, name: str):
        self.name = name
        self.hand = Hand()
        
    @abstractmethod
    def take_turn(self):
        ...
        
    def __str__(self):
        return f"[{type(self).__name__}] {self.name}"
    
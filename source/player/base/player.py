from core.dice import Hand
from abc import ABC, abstractmethod

class Player(ABC):
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    def take_turn(self):
        ...
    
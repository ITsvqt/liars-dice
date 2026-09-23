from abc import ABC, abstractmethod


class GameUI(ABC):
    
    @abstractmethod
    def ask_player_name(self, suggestion: str) -> str:
        ...
        
    @abstractmethod
    def ask_ai_count(self, min: int, max: int, suggestion: int) -> int:
        ...
        
    @abstractmethod
    def show_message(self, msg: str):
        ...
        
    @abstractmethod
    def ask_confirmation(self):
        ...
    
    
        
        
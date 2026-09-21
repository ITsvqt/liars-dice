from models.player.base.player import Player


class AIPlayer(Player):
    
    def __init__(self, name: str, aggression: float):
        super().__init__(name)
        self.aggression = aggression
        
    def take_turn(self):
        if True:
            ...
            
            
    def __str__(self):
        return super().__str__() + f" aggresion: {self.aggression}"
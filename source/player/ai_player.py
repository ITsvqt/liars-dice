from player.base.player import Player


class AI_player(Player):
    
    def __init__(self, name: str, risk_factor: float):
        super().__init__(name)
        self. risk_factor = risk_factor
        
    def take_turn(self):
        ...
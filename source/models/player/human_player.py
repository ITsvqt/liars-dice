from models.player.base.player import Player


class HumanPlayer(Player):
    
    REQUIRES_UI_INPUT = True
    
    def take_turn(self):
        if True:
            ...
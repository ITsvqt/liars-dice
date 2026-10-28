from ui.terminal_ui import TerminalUI
from engine.game import Game

class TerminalGameRunner:
    
    @classmethod
    def run(cls):
        """ Game loop interacts with the terminal. """
        
        terminal_ui = TerminalUI()
        game = Game(terminal_ui)
        game.start()
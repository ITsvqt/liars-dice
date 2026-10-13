from ui.terminal_ui import TerminalUI
from engine.game import Game

class TerminalGameRunner:
    def run(self):
        terminal_ui = TerminalUI()
        game = Game(terminal_ui)
        game.start()
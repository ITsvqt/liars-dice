from engine.game import Game



from ui.terminal import TerminalUI

t_ui = TerminalUI()
g = Game(t_ui)
g.start()

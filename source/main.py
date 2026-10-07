from threading import Thread
import uvicorn

from engine.game import Game
from ui.terminal_ui import TerminalUI
from ui.web.web_ui import WebUI
from ui.web import server


if __name__ ==  '__main__':
    
    IS_UI_WEB = True

    if IS_UI_WEB:
        
        web_ui = WebUI()
        server.set_ui(web_ui)
        game = Game(web_ui)
        
        # Run the server on the main thread
        # and the game loop on the background thread
        thread = Thread(target = game.start)
        thread.start()
        
        uvicorn.run("ui.web.server:app", reload = True)

    else: # TERMINAl
        terminal_ui = TerminalUI()
        game = Game(terminal_ui)
        game.start()

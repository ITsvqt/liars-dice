import uvicorn
from threading import Thread

from ui.web import server
from ui.web.web_ui import WebUI
from engine.game import Game


class WebGameRunner:
    
    @classmethod
    def run(cls):
        """ Server runs on main thread. And game loop on branch thread."""
        
        web_ui = WebUI()
        server.set_ui(web_ui)
        
        game = Game(web_ui)
        game_thread = Thread(target = game.start, daemon=True)
        game_thread.start()
                
        uvicorn.run("ui.web.server:app")
       
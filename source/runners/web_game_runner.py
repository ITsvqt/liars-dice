import uvicorn
from threading import Thread

from ui.web import server
from ui.web.web_ui import WebUI
from engine.game import Game


class WebGameRunner:
    def run(self):
        web_ui = WebUI()
        server.set_ui(web_ui)
        
        game = Game(web_ui)
        game_thread = Thread(target = game.start)
        game_thread.start()
        
        
        try:
            uvicorn.run("ui.web.server:app")
        finally:
            web_ui.shutdown()
            game_thread.join(timeout=5)
        # Run the server on the main thread
        # and the game loop on the background  thread
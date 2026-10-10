from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.web.web_ui import WebUI

import utility.constants as c
from fastapi import Body, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse


import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


#* Bridge between game and server
web_ui: WebUI = None 

def set_ui(ui: WebUI):
    global web_ui
    web_ui = ui
    
    
#* FastAPI
app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
# app.mount("/static", StaticFiles(directory="ui/web/static"), name = "static")


# *** HOME PAGE ***
@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "static/index.html"))


# *** GAME ***
@app.get("/game")
def game():
    return FileResponse(os.path.join(BASE_DIR, "static/game/game.html"))


# *** RECEIVE GAME CONSTANTS ***
@app.get("/setup")
def send_constants():
    return {
        "suggested_name": c.SUGGESTED_PLAYER_NAME,
        "ai_names" : list(c.RESERVED_NAMES),
        "suggested_wild_ones" : c.SUGGESTED_WILD_ONES,
        "suggested_ai_count" : c.SUGGESTED_AI_PLAYER_CNT,
        "min_ai" : c.CNT_MIN_PLAYERS - 1,
        "max_ai" : c.CNT_MAX_PLAYERS - 1
    }
    
    
# *** SEND GAME SETTINGS ***
@app.post("/setup")
def receive_game_setup(data: dict = Body()):
    if web_ui.state["is_running"]:
        return JSONResponse(status_code = 400, content = {"error": "Game already in progress"})
    web_ui.setup_data = data
    web_ui.setup_event.set()
    
    return {"success": True}


# *** GET WEB_UI STATE ***
@app.get("/state")
def get_state():
    return web_ui.state


# *** SEND PLAYER MOVE ***
@app.post("/move")
def player_move(data: dict = Body()):
    web_ui.move_data = data
    web_ui.move_event.set()
    
    
# *** CLOSE REVEAL PANEL ***
@app.post("/reveal_continue")
def reveal_continue():
    web_ui.reveal_event.set()
    return {"success": True}

# *** END GAME ***

@app.post("/restart")
def restart():
    web_ui.restart_data = "restart"
    web_ui.restart_event.set()
    return {"success": True}

@app.post("/quit")
def quit():
    web_ui.restart_data = "quit"
    web_ui.restart_event.set()
    return {"success": True}
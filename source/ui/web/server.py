from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.web.web_ui import WebUI

import utility.constants as c
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

#* Bridge between game and server
web_ui: WebUI = None 

def set_ui(ui: WebUI):
    global web_ui
    web_ui = ui
    
    
#* FastAPI
app = FastAPI()
app.mount("/static", StaticFiles(directory="ui/web/static"), name = "static")


    
    
    
@app.get("/")
def home():
    return FileResponse("ui/web/static/index.html")


@app.get("/game")
def game():
    return FileResponse("ui/web/static/game/game.html")


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
    
    

# 1. #? I dont understand how the input field for name gets validated on every key stroke.
# 2. #? Looking and the game implementation i would just leave some abstract methods from the parrent implemented with nothing,
# 3. #? 

@app.post("/setup")
def receive_game_setup(data: dict):
    web_ui.setup_data = data
    web_ui.setup_event.set()
    
    return {"success": True}


#* ENDPOINTS: 
#!
#TODO


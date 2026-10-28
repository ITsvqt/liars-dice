from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.web.web_ui import WebUI

import utility.constants as c
from fastapi import Body, FastAPI, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware


import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


#* Bridge between game and server
web_ui: WebUI = None 

def set_ui(ui: WebUI):
    global web_ui
    web_ui = ui
    
    
#* FastAPI
app = FastAPI()

#* Prevent browser from caching static files (avoids stale JS/CSS during dev)
class NoCacheStaticMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/static"):
            response.headers["Cache-Control"] = "no-store"
        return response

app.add_middleware(NoCacheStaticMiddleware)

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
def get_constants():
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
def send_game_setup(data: dict = Body()):
    
    # Wait until the game thread is genuinely parked & ready for a new setup
    if not web_ui.setup_ready_event.wait(timeout=10):
        return JSONResponse(
            status_code=503,
            content= {"error": "Game not ready for setup"}
        )
    
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
    # Only accept a restart when a game is genuinely finished & awaiting replay
    if web_ui.phase != "game_over":
        return JSONResponse(
            status_code=409,
            content={"error": "No finished game to restart"}
        )
    web_ui.restart_data = True
    web_ui.restart_event.set()
    return {"success": True}


@app.get("/quit")
def quit():
    # Stop the game thread, serve a themed blank page, then shut the process down
    # (BackgroundTask runs only AFTER this response is sent to the browser).
    def _shutdown():
        os._exit(0)
    web_ui.restart_data = False
    web_ui.restart_event.set()
    tasks = BackgroundTasks()
    tasks.add_task(_shutdown)
    return HTMLResponse(
        "<!DOCTYPE html><meta charset='utf-8'>"
        "<style>html,body{height:100%;margin:0;background:#0e0c0a}</style>",
        background=tasks
    )
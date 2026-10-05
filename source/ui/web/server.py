from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.web.web_ui import WebUI


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
    
#* ENDPOINTS: 
#!
#TODO


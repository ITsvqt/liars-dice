from runners.terminal_game_runner import TerminalGameRunner
from runners.web_game_runner import WebGameRunner

#! download 3.8 and run with this interpreter
#! try to run imports on Python 3.8 

#! RESTFULL API 
#- get.state = get.("game")
# = @app.post("/setup") -> "options"
#-  @app.get("/quit") -> app.delete("/game")

#- @app.post("/move") -> @app.post("/moves")
#* return 201 Created

#- ADD Pydantic models for validation in presentation layer, not in service

# pylance Type checking mode -> or other extension for chekcing method reuturn signature with exact return type

#unit tests for service layer | game engine





IS_UI_WEB = True


if IS_UI_WEB:
    WebGameRunner.run()
else:
    TerminalGameRunner.run()



from runners.terminal_game_runner import TerminalGameRunner
from runners.web_game_runner import WebGameRunner





IS_UI_WEB = True


if IS_UI_WEB:
    WebGameRunner.run()
else:
    TerminalGameRunner.run()



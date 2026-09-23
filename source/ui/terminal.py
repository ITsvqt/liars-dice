from ui.base.ui import GameUI
from utility.type_parsing import try_parse_int, try_parse_bool

class TerminalUI(GameUI):
    
    def ask_ai_count(self, min: int, max: int, suggestion: int) -> int:
        while True:
            try:
                return try_parse_int(input(f"Enter count of AI enemies [{min}:{max}]({suggestion}): "))
            except ValueError as e:
                self.show_message("Number input is required")

    def ask_player_name(self, suggestion: str) -> str:
        while True:
            p_name = input(f"Enter your battle name ({suggestion}): ")
            
            if 0 < len(p_name) < 30:
                return p_name
            
            self.show_message("Cannot accept empty input")
        
        
        
    def show_message(self, msg: str):
        print(msg)
        
    def ask_confirmation(self):
        input("Press enter to continue...")        
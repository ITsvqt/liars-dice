from ui.base.ui import GameUI
from models.bid import Bid
from utility.type_parsing import try_parse_int, try_parse_bool # todo : add the wild ones

class TerminalUI(GameUI):
    
    
    
    def ask_player_move(self, current_bid: Bid, player_dice: list[int], dice_cnt: int):
        
        print(f"Your hand : ({' '.join(list(map(str, player_dice)))})")
        print(f"Total dice count: {dice_cnt}")
        
        if current_bid is not None:
            print(f"Current bid: {current_bid}")
            # get move type: [Raise, Challenge]
            while True:
                print("Choose option:")
                print("[1] Raise the bid:")
                print("[2] Challenge - call Liar!:")
                choice = self._ask_number("  Choose")
                
                if choice in [1,2]:
                    break
                
                print("Invalid menu selection")
                
            if choice == 2:   #Challenge
                return ("Challenge", None)
            
        return ("Bid", self._ask_bid())
                    
            
    def _ask_bid(self) -> tuple[int, int]:
        cnt = self._ask_number("Quantity (how many dice)")
        face = self._ask_number("Face value (1-6)")
        
        return (cnt,face)
    
    
    @staticmethod
    def show_message(msg: str):
        print(msg) 
        
        
    @staticmethod  
    def ask_confirmation():
        input("Press enter to continue...")
        
        
    def ask_ai_count(self, min: int, max: int, suggestion: int) -> int:
        return self._ask_number(f"Enter count of AI enemies [{min}:{max}]({suggestion}): ")


    def ask_player_name(self, suggestion: str) -> str:
        while True:
            p_name = input(f"Enter your battle name ({suggestion}): ")
            
            if 0 < len(p_name) < 30:
                return p_name
            
            print("Cannot accept empty input")

    def _ask_number(msg: str):
        while True:
            try:
                return try_parse_int(input(msg))
            except ValueError:
                print("Number input is required")
                


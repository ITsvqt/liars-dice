import os

import utility.constants as const
from ui.base.ui import GameUI
from models.bid import Bid
from utility.type_parsing import try_parse_int, try_parse_bool

class TerminalUI(GameUI):
    
    def initiate():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcome to the Liars Dice Game ; )\n\tGOOD LUCK\n")
        
    def get_set_up_vars(self) -> dict:

        setup = {}
        
        setup["cnt_ai"] = self._ask_ai_count(
            const.CNT_MIN_PLAYERS - 1, # -1 for the human player
            const.CNT_MAX_PLAYER - 1,  # -1 for the human player
            const.SUGGESTION_AI_PLAYER_CNT
            )
        setup["player_name"] = self._ask_player_name(const.SUGGESTION_PLAYER_NAME)
        setup["wild_ones"] = self._ask_wild_ones()
        
        return setup
        
        
        
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
        """Returns (for_face, dice_cnt)"""
        cnt = self._ask_number("Quantity (how many dice): ")
        face = self._ask_number("Face value (1-6): ")
        
        return (face, cnt)
    
    
    @staticmethod
    def show_message(msg: str):
        print(msg) 
        
        
    @staticmethod  
    def ask_confirmation():
        input("\tPress enter to continue... ")
        
        
    def _ask_ai_count(self, min_cnt: int, max_cnt: int, suggestion: int) -> int:
        while not min_cnt <= (
            number:= self._ask_number(f"Enter count of AI enemies [{min_cnt}:{max_cnt}]({suggestion}): ")
        ) <= max_cnt:
            
            print("\tInvalid AI count!")
            
        return number


    @staticmethod
    def _ask_player_name(suggestion: str) -> str:
        reserved_names = {name for name in const.AI_PLAYERS.keys()}
        
        while True:
            p_name = input(f"Enter your battle name ({suggestion}): ")
            
            if not 0 < len(p_name) < 30:
                print("\tCannot accept empty name!")
                continue
            if p_name in reserved_names:
                print("\tName is reserved by AI player!")
                continue
            
            return p_name

            
            
    @staticmethod
    def _ask_wild_ones() -> bool:
        while True:
            try:
                return try_parse_bool(input("Enable wild ones ? [y/n](n): "))
            except ValueError:
                print("\tEnter y/n!")


    @staticmethod
    def _ask_number(msg: str):
        while True:
            try:
                return try_parse_int(input(msg))
            except ValueError:
                print("\tNumber input is required!")
                


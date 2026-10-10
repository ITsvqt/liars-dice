from __future__ import annotations
from typing import TYPE_CHECKING
import threading

if TYPE_CHECKING:
    from models.player.base.player import Player
    from models.bid import Bid
    from collections import Counter

from ui.base.ui import GameUI



class WebUI(GameUI):
    
    def __init__(self):
        
        #* Browser info
        self.state = {              # Hint  # SET BY
            "is_running": False,    # bool  # get_setup_vars
            "phase": "waiting",                 # str   # show,round, reveal, winner ("playing" / "reveal" / "game_over")
            "round": None,          # int   # show round : int
            "players": [],          # player.to_dict()  # show round
            "current_player": None, # str(name)  # show_turn_header {}
            "bid_holder": None,     # str(name)  # show turn
            "current_bid": None,    # bid.to_dict()  # show turn
            "dice_count": None,     # int  # show turn
            "reveal": None,         # dict  # show_reveal, round_results
            "log": [],              # list # any method 
            "winner": None,         # str(name)  # show winner
            "wild_ones": False,      # bool # get_setup_vars
        }
        
        #* Setup
        self.setup_event = threading.Event()
        self.setup_data: dict | None = None 

        #* Player move
        self.move_event = threading.Event()
        self.move_data = None
        
        #* Reveal
        self.reveal_event = threading.Event()

        #* Restart
        self.restart_event = threading.Event()
        self.restart_data = None
        
        



    def get_setup_vars(self) -> dict:
        """
        Return:
            cnt_ai: int
            player_name: str
            wild_ones: True | False
        """
        
        self.setup_event.wait()
        self.state["is_running"] = True
        self.state["wild_ones"] = self.setup_data["wild_ones"]
        return self.setup_data
    
    def ask_player_move(self,
        current_bid: Bid,
        player: Player,
        dice_cnt: int,
        wild_ones: bool = False
        )-> tuple[str, tuple[int, int] | None]:
        """UI should limit player for making Challenge move when there is no initial Bid\n
        Should display current Bid and Dice_cnt\n
        Returns ("Challenge", None) | ("Bid", (face, quantity))"""

        #TODO no parameters used
        self.move_event.clear()
        self.move_data = None
        
        self.move_event.wait()
        
        data = self.move_data
        if data["type"] == "Challenge":
            return ("Challenge", None)
        else:
            return ("Bid", (data["face"], data["quantity"]))



    def show_prestart(self, players: list[Player], wild_ones: bool):
        """Show initial game state"""
        self.state["players"] = [p.to_dict() for p in players]
    
    
    def show_round(self, round_num: int, active_players: list[Player], dice_cnt:int, wild_ones: bool):
        """Update UI to round start state"""
        
        #* Reset from previous round
        self.state["current_bid"] = None
        self.state["bid_holder"] = None
        self.state["reveal"] = None
        
        #* Set round data
        self.state["phase"] = "playing"
        self.state["round"] = round_num
        self.state["players"] = [p.to_dict() for p in active_players]
        
    def show_turn_header(self, current_player: Player):
        self.state["current_player"] = current_player.name
        
    
    def show_turn(self,  player: Player, bid: Bid | None):
        """Update UI to turn state"""
        
        if bid is not None:
            self.state["bid_holder"] = player.name
            self.state["current_bid"] = bid.to_dict()
            self.state["log"].append(f"{player.name} bids {bid}")
        else:
            self.state["log"].append(f"{player.name} calls LIAR!")
            
        
    def show_reveal(
        self,
        active_players: list[Player],
        face_counts: Counter,
        current_bid: Bid,
        wild_ones: bool
        ):
        """Update UI to round end state"""
        
        self.reveal_event.clear()
        self.state["phase"] = "reveal"
        self.state["reveal"] = {
            "player_hands": [p.to_dict(True) for p in active_players],
            "face_counts": {
                "1": face_counts[1],
                "2": face_counts[2],
                "3": face_counts[3],
                "4": face_counts[4],
                "5": face_counts[5],
                "6": face_counts[6]
                },
            "winner": None,
            "loser": None,
            "loser_eliminated": None,
            "challenge_valid": None
        }
        

    
    def show_round_result(
        self,
        loser_player: Player,
        winning_player: Player,
        is_eliminated: bool,
        bid: Bid,
        challenger_player: Player,
        is_challenge_valid: bool,
        bid_holder: Player
        ):
        """Update UI to round result state"""
        
        self.state["reveal"]["winner"] = winning_player.name
        self.state["reveal"]["loser"] = loser_player.name
        self.state["reveal"]["loser_eliminated"] = is_eliminated
        self.state["reveal"]["challenge_valid"] = is_challenge_valid
        
        if is_challenge_valid:
            self.state["log"].append(f"Bluff called! {loser_player.name} loses a die.")
        else:
            self.state["log"].append(f"Bid stands! {loser_player.name} loses a die.")

        if is_eliminated:
            self.state["log"].append(f"{loser_player.name} is eliminated!")
            
        self.reveal_event.wait()
        self.reveal_event.clear()
        
        
    def show_winner(self, player: Player) -> bool:
        """Update UI to game end state"""
        self.state["phase"] = "game_over"
        self.state["winner"] = player.name
        self.state["log"].append(f"🏆 {player.name} wins the game!")
        
        self.restart_event.wait()
        self.restart_event.clear()
        
        action = self.restart_data
        # reset state for new game
        self.state["is_running"] = False
        self.state["phase"]      = "waiting"
        self.state["winner"]     = None
        self.state["log"]        = []
        
        return True if action == "restart" else False
        
        
        
        


        
        
        
    
    def show_message(self, msg: str):
        self.state["log"].append(msg)
        
    def show_error(self, error_msg: str):
        self.state["error"] = error_msg
        self.state["log"].append(f"Error: {error_msg}")
        
    def ask_confirmation(self, msg: str):
        pass  # no blocking confirmation in web UI
        
        
    def initiate(self):
        """Start UI"""
        pass # server is already running before game starts
        
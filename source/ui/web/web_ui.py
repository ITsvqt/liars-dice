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
        super().__init__()
        
        #* Setup
        self.setup_event = threading.Event()

        #* Player move
        self.move_event = threading.Event()
        
        #* Reveal
        self.reveal_event = threading.Event()

        #* Restart
        self.restart_event = threading.Event()
        
        #* Game thread is parked & ready to receive setup (raised in get_setup_vars)
        self.setup_ready_event = threading.Event()
        
        self._set_starting_web_state()

        
    def _set_starting_web_state(self):
        """Reset UI state attributes to their starting values for a new game."""
        self.is_running: bool = False
        self.phase: str = "waiting"
        self.round: int = None
        self.players: list[dict] = []
        self.current_player: str = None
        self.bid_holder: str = None
        self.current_bid = None
        self.dice_count: int = None
        self.reveal: dict = None
        self.log: list[str] = []
        self.winner: str = None
        self.wild_ones = False
        self.player_hand: list[int] = []
        self.is_reveal_shown: bool = False
        self.error: str = ""

    @property
    def state(self) -> dict:
        """Fronted consumed"""
        return {
            "is_running": self.is_running,
            "phase": self.phase,
            "round": self.round,
            "players": self.players,
            "current_player": self.current_player,
            "bid_holder": self.bid_holder,
            "current_bid": self.current_bid,
            "dice_count": self.dice_count,
            "reveal": self.reveal,
            "log": self.log,
            "winner": self.winner,
            "wild_ones": self.wild_ones,
            "player_hand": self.player_hand,
            "show_reveal": self.is_reveal_shown,
            "error": self.error,
        }

    def initiate(self):
        """Set starting  web_UI state"""
        
        self._set_starting_web_state()

        self.setup_data: dict | None = None  # game start options
        self.move_data = None
        self.restart_data = None
        self.setup_event.clear()
        self.restart_event.clear()
        self.move_event.clear()
        self.reveal_event.clear()
        self.setup_ready_event.clear()
        
        
        
        
    def get_setup_vars(self) -> dict:
        """
        Return:
            cnt_ai: int
            player_name: str
            wild_ones: True | False
        """
        
        
        self.setup_ready_event.set()
        # wait until player sends request with game settings, saved to self.setup_data
        self.setup_event.wait()
        self.setup_ready_event.clear()
        
        self.is_running = True
        self.wild_ones = self.setup_data["wild_ones"]
        return self.setup_data
    
    def ask_player_move(self,
        current_bid: Bid,
        player: Player,
        dice_cnt: int
        )-> tuple[str, tuple[int, int] | None]:
        """UI should limit player for making Challenge move when there is no initial Bid\n
        Should display current Bid and Dice_cnt\n
        Returns ("Challenge", None) | ("Bid", (face, quantity))"""

        self.move_event.clear()
        self.move_data = None
        self.move_event.wait()
        
        data = self.move_data
        if data["type"] == "Challenge":
            return ("Challenge", None)
        else:
            return ("Bid", (data["face"], data["quantity"]))



    def show_prestart(self, players: list[Player]):
        """Show initial game state"""
        self.players = [p.to_dict() for p in players]
    
    
    def show_round(self, round_num: int, active_players: list[Player], dice_cnt:int):
        """Update UI to round start state"""
        
        #* Reset from previous round
        self.current_bid = None
        self.bid_holder = None
        self.reveal = None
        self.is_reveal_shown = False
        
        #* Set round data
        self.phase = "playing"
        self.round = round_num
        self.players = [p.to_dict() for p in active_players]
        
        #* Pass human player's hand to frontend at round start
        human = next((p for p in active_players if not p.is_bot), None)
        self.player_hand = human.values if human else []
        
    def show_turn_header(self, current_player: Player):
        self.current_player = current_player.name
        
    
    def show_turn(self,  player: Player, bid: Bid | None):
        """Update UI to turn state"""
        
        if bid is not None:
            self.bid_holder = player.name
            self.current_bid = bid.to_dict()
            self.log.append(f"{player.name} bids {bid}")
        else:
            self.log.append(f"{player.name} calls LIAR!")
            
        
    def show_reveal(
        self,
        active_players: list[Player],
        face_counts: Counter,
        current_bid: Bid
        ):
        """Update UI to round end state"""
        
        self.reveal_event.clear()
        self.phase = "reveal"
        self.reveal = {
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
        
        self.reveal["winner"] = winning_player.name
        self.reveal["loser"] = loser_player.name
        self.reveal["loser_eliminated"] = is_eliminated
        self.reveal["challenge_valid"] = is_challenge_valid
        
        if is_challenge_valid:
            self.log.append(f"Bluff called! {loser_player.name} loses a die.")
        else:
            self.log.append(f"Bid stands! {loser_player.name} loses a die.")

        if is_eliminated:
            self.log.append(f"{loser_player.name} is eliminated!")
            
        self.player_hand = []
        self.is_reveal_shown = True
            
        self.reveal_event.wait()
        self.is_reveal_shown = False
        self.reveal_event.clear()
        
        self.log.append("")
        self.log.append("")
        self.log.append("")


        
        
    def show_winner(self, player: Player) -> bool:
        """Update UI to game end state"""
        self.is_reveal_shown = False
        self.phase = "game_over"
        self.winner = player.name
        self.log.append(f"🏆 {player.name} wins the game!")
        

        
    def ask_replay_game(self) -> bool:
        """Restart game after finish ?"""
        self.restart_event.wait()
        self.restart_event.clear()
                
        return self.restart_data
    
    def show_message(self, msg: str):
        self.log.append(msg)
        
    def show_error(self, error_msg: str):
        self.error = error_msg
        self.log.append(f"Error: {error_msg}")
        
    def ask_confirmation(self, msg: str):
        pass  # no blocking confirmation in web UI
        
        


import random
from typing import TYPE_CHECKING

from engine.player_circle import PlayerCircle
from engine.rules import LiarsDiceRules
from utility.type_parsing import try_parse_int
from models.player.human_player import HumanPlayer
from models.player.ai_player import AIPlayer
from models.bid import Bid

if TYPE_CHECKING:
    from models.player.base.player import Player
    from ui.base.ui import GameUI
    from collections import Counter

AI_PLAYERS = {
    "Captain Blackbeard"     : 0.75, # big bluffer
    "Naga Seawitch"          : 0.55, # balanced
    "Devil Itslef"           : 0.66, # a bit cocky
    "The Pope"               : 0.33, # safe player
    "Little Red Riding Hood" : 0.50  # dzen
}


class Game:
    
    
    
    def __init__(self, ui: GameUI, wild_ones = False):
        
        self.ui = ui
        self.human_player: HumanPlayer = None #! the idea was to display the hand of this player, but the refference ended up useless for now ( check the game loop if its not there, its useless)
        self.players:  list[Player] = self._set_up()
        self.player_circle = PlayerCircle(self.players)
        self.wild_ones = wild_ones
        
        self.turn_cnt: int = 0
        

    def game_loop(self):

        #todo : test game logic
        while not LiarsDiceRules.is_game_over(self.player_circle):
            self._play_round()

        #todo : what happens after this loop, who is the current player, is he the winner, 

    def _play_round(self):
        
        dice_face_cnt: Counter = self._roll_and_collect_dice()
        dice_cnt = sum(dice_face_cnt.values())
        current_bid = None        
        
        #* Until plays challenge move
        while True:
            player: Player = self.player_circle.current_player
            
            move = self._get_valid_player_move(player, current_bid, dice_cnt)
            
            if move[0] == "Challenge":
                break
            else: #move[0] == 'Bid'
                current_bid = move[1]
                
            self.player_circle.advance()
            
        #* Determine the looser
        res = LiarsDiceRules.is_challenge_correct(current_bid, dice_face_cnt, self.wild_ones)
        loosing_player = player if res is False else self.player_circle.previous_player
        loosing_player.remove_die()
        self.ui.show_message(
            f"Player {loosing_player.name} list the round"
            f"Dice remaining {loosing_player.cnt_dice}"
            )
        
        #* Check for elmination
        if loosing_player.is_hand_empty is True:
            self.player_circle.remove_player(res)
            self.ui.show_message(f"Player {loosing_player.name} was elminated")
            
        self.turn_cnt += 1
        

        
    def _get_valid_player_move(self, player: Player, current_bid: Bid, dice_cnt: int) -> tuple[str, Bid | None]:
        
            #* Until function exit with return
            while True:
                
                #* Determine input source
                if player.IS_BOT:
                    move = player.calc_turn(current_bid)
                else:
                    move = self.ui.ask_player_move(current_bid, player.values, dice_cnt)

                #* Early exit when move is "Challenge"        
                if move[0] == "Challenge":
                    if current_bid is None: # No bid, Challenge situation
                        raise ValueError("Program error: Trying to challenge last bid , when there is no initial bid.")
                    
                    return move 
                    
                #* Validate Bid, and retry if invalid
                elif move[0] == 'Bid':
                    try:
                        new_bid = Bid(move[1][0], move[1][1])
                        if LiarsDiceRules.is_new_bid_valid(current_bid, new_bid):
                            
                            return (move[0], new_bid)
                        
                    except ValueError as e:
                        self.ui.show_message(e[0])
                        
                else:
                    raise ValueError(f"Program error: invalid move [{move}]")
        
        
    def _roll_and_collect_dice(self) -> Counter[int, int]:
        #- tested current player not changed after looping through all player to roll
        #- tested expected sum of face occurence == count of player dice
        #- briefly looked on the random values
        """Make all players roll and return summary of dice face cnt"""
        
        result = Counter()
        
        for _ in range(self.player_circle.count):
            p = self.player_circle.current_player
            p.roll()
            result.update(p.values)
            print(p.name)
            self.player_circle.advance()

        return result

    def _set_up(self) -> list[Player]:
        """Create players and shuffle them in random order"""
        
        ai_players: list[Player] = self._create_ai_players()
        human_player: Player = self._create_human_player([p.name for p in ai_players])
        
        ai_players.append(human_player)
        
        random.shuffle(ai_players)
        return ai_players
    
    
    def _create_ai_players(self) -> list[Player]:
        
        max_ai_cnt = LiarsDiceRules.CNT_MAX_PLAYER - 1
        
        while True:
            aip_cnt = self.ui.ask_ai_count(1, max_ai_cnt, 2)
            
            if 1 <= aip_cnt <= max_ai_cnt:
                return [
                    AIPlayer(name, aggression)
                    for name, aggression
                    in random.sample(list(AI_PLAYERS.items()), aip_cnt)
                ] 
                
            self.ui.show_message(f"Illegal opponents count[1:{max_ai_cnt}]: {aip_cnt}")
            
            
    def _create_human_player(self, reserved_names: list[int]) -> Player:
        
        while True:
            human_p_name = self.ui.ask_player_name("Captain")
            
            if human_p_name not in reserved_names:
                h_p = HumanPlayer(human_p_name)
                self.human_player = h_p
                return 
                
            self.ui.show_message(f"'{human_p_name}' is already taken")
        

                
        


import random
from typing import TYPE_CHECKING
from collections import Counter

import utility.constants as const
from engine.player_circle import PlayerCircle
from engine.rules import LiarsDiceRules
from utility.type_parsing import try_parse_int
from models.player.human_player import HumanPlayer
from models.player.ai_player import AIPlayer
from models.bid import Bid

if TYPE_CHECKING:
    from models.player.base.player import Player
    from ui.base.ui import GameUI




class Game:
    
    
    
    def __init__(self, ui: GameUI):
        
        self.ui = ui
        
        self.players:  list[Player] = None       # all initial player
        self.player_circle: PlayerCircle = None  # active players
        self.wild_ones = None
        self.human_player: HumanPlayer = None #! the idea was to display the hand of this player, but the refference ended up useless for now ( check the game loop if its not there, its useless)
        self.cnt_round: int = 0

        
        
    def _set_up(self):
        config = self.ui.get_set_up_vars(
            const.CNT_MIN_PLAYERS - 1, # -1 for the human player
            const.CNT_MAX_PLAYER - 1,  # -1 for the human player
            const.SUGGESTION_AI_PLAYER_CNT,
            {name for name in const.AI_PLAYERS.keys()}
        )
        
        all_players: list[Player] = self._create_ai_players(config["cnt_ai"])
        human_player: Player = self._create_human_player(config["player_name"])
        all_players.append(human_player)
        
        random.shuffle(all_players)
        
        self.players = all_players
        self.player_circle = PlayerCircle(all_players)
        self.wild_ones = config["wild_ones"]
        

    def start(self):

        self.ui.initiate()
        self._set_up()
        self.ui.show_prestart(self.players, self.wild_ones)
        
        while not LiarsDiceRules.is_game_over(self.player_circle):
            self._play_round()

        winner = self.player_circle.current_player
        self.ui.show_winner(winner)
        #todo : what happens after this loop, who is the current player, is he the winner, 

    def _play_round(self):
        #* Round setup
        self.cnt_round += 1
        active_players = self.player_circle.all_players
        dice_face_cnt: Counter = self._roll_and_collect_dice()
        dice_cnt = sum(dice_face_cnt.values())
        current_bid = None        
        
        self.ui.show_round(self.cnt_round, active_players, self.wild_ones)
        
        #* Go around the circle, until someone Challenge
        while True:
            player: Player = self.player_circle.current_player
            self.ui.show_turn_header(player)
            move: tuple = self._get_valid_player_move(player, current_bid, dice_cnt)
            self.ui.show_turn(player.name, move[1])
            
            if move[0] == "Challenge":
                break
            else: #move[0] == 'Bid'
                current_bid = move[1]
                
            self.player_circle.advance()
            
        self.ui.show_reveal(active_players, dice_face_cnt, self.wild_ones)
        
        #* Determine the looser
        res = LiarsDiceRules.is_challenge_correct(current_bid, dice_face_cnt, self.wild_ones)
        loosing_player = player if res is False else self.player_circle.previous_player
        loosing_player.remove_die()
        
        # self.ui.show_message(
        #     f"Player {loosing_player.name} lost the round"
        #     f"Dice remaining {loosing_player.cnt_dice}"
        #     )
        
        #* Check for elmination
        is_eliminated = loosing_player.is_hand_empty()
        
        if is_eliminated is True:
            self.player_circle.remove_player(res)
            # self.ui.show_message(f"Player {loosing_player.name} was elminated")
            
        self.ui.show_round_result(
            loosing_player.name,
            loosing_player.is_bot,
            is_eliminated,
            str(current_bid),
            player.name,
            res
            )        

        
    def _get_valid_player_move(self, player: Player, current_bid: Bid, dice_cnt: int) -> tuple[str, Bid | None]:
        
            #* Until function exit with return
            while True:
                #* Determine input source
                if player.is_bot:
                    move = player.calc_turn(current_bid, dice_cnt, self.wild_ones)
                else:
                    move = self.ui.ask_player_move(current_bid, player, dice_cnt)

                #* Early exit when move is "Challenge"        
                if move[0] == "Challenge":
                    if current_bid is None: #! this is pre-arranged and passing through crashes the program
                        raise ValueError("Program error: Trying to challenge last bid , when there is no initial bid.")
                    
                    return move 
                    
                #* Validate Bid, and retry if invalid
                elif move[0] == 'Bid':
                    try:
                        new_bid = Bid(move[1][0], move[1][1])
                        if LiarsDiceRules.is_new_bid_valid(current_bid, new_bid):
                            
                            return (move[0], new_bid)
                        
                    except ValueError as e:
                        self.ui.show_error(e)
                        
                else: #! this is pre-arranged and passing through crashes the program
                    raise ValueError(f"Program error: Invalid move - action:[{move[0]}] bid [{move[1]}]")
        
        
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
            self.player_circle.advance()

        return result


    def _create_ai_players(self, aip_cnt: int) -> list[Player]:
        return [
            AIPlayer(name, aggression)
            for name, aggression
            in random.sample(list(const.AI_PLAYERS.items()), aip_cnt)
            ]
                   
    def _create_human_player(self, human_name: str) -> Player:
        self._ensure_valid_human_name(human_name)
        h_p = HumanPlayer(human_name)
        self.human_player = h_p
        return h_p
            
            
    @staticmethod
    def _ensure_valid_human_name(name: str):
        """Not in ai_players_names"""
        if name in {n for n in const.AI_PLAYERS.keys()}:
            raise ValueError(f"[Error] Human player name [{name}] overlaping with AI names!")

                
    def __repr__(self):
        res = ['---------------------------------']
        res.append("Game object:")
        res.append(repr(self.player_circle))
        res.append("\t Players:")
        for p in self.players:
            res.append(f"\t\t{p}")
        res.append("\t Wild ones:" + str(self.wild_ones))
        res.append('---------------------------------')
        return "\n".join(res)
        

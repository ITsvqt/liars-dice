from models.dice import Dice
from models.bid import Bid
from engine.game import Game
from models.player.human_player import HumanPlayer
from models.player.ai_player import AIPlayer
from models.player.base.player import Player


from engine.rules import LiarsDiceRules
from engine.player_circle import PlayerCircle
import time


from ui.terminal import TerminalUI

t_ui = TerminalUI()
g = Game(t_ui)
g.game_loop()

# p1 = _Required
# print(p1)
# pc = PlayerCircle([HumanPlayer("ceci")])

# pc = PlayerCircle([HumanPlayer("ceci"), AIPlayer("mechko",0.5), AIPlayer("toshko", 0.7)])

# print(LiarsDiceRules.is_game_over(pc))

# for i in range(9):
    
#     print(f"[{i}] {pc.current_player}")
#     pc.advance()


# print(LiarsDiceRules.is_bid_correct(Bid(1,1), {1:1, 2:2, 3:3}))
# print(LiarsDiceRules.is_bid_correct.__annotations__)
# g1 = Game()

# for p in g1.players:
#     print(p)

# from collections import Counter

# c1 = Counter([1,1,1,1,1,1,1,1,2,2])

# print(c1.items())

    
# cnt_opponents = try_parse_int(input('Enter number of AI opponents:\n\t'))
# is_wild_ones_on = try_parse_bool(input('Do you want to enable wild ones?\n(Yes / No)\n\t'))
# print(cnt_opponents)
# print(is_wild_ones_on)

    
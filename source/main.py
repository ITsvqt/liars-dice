from utility.parsing import try_parse_int, try_parse_bool
from models.dice import Dice
from models.bid import Bid
from models.player.base.player import Player
from engine.game import Game
from engine.rules import LiarsDiceRules

# print(LiarsDiceRules.is_bid_correct(Bid(1,1), {1:1, 2:2, 3:3}))
print(LiarsDiceRules.is_bid_correct.__annotations__)
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

    
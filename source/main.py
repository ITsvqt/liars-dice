from utility import try_parse_int, try_parse_bool
from core.dice import Dice, Hand
from player.base.player import Player
from engine.game import Game

# g1 = Game()

# for p in g1.players:
#     print(p)

from collections import Counter

c1 = Counter([1,1,1,1,1,1,1,1,2,2])

print(c1.items())
    
    
# cnt_opponents = try_parse_int(input('Enter number of AI opponents:\n\t'))
# is_wild_ones_on = try_parse_bool(input('Do you want to enable wild ones?\n(Yes / No)\n\t'))
# print(cnt_opponents)
# print(is_wild_ones_on)

    
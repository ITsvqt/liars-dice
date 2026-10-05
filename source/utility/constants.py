

CNT_MIN_PLAYERS = 2
CNT_MAX_PLAYERS = 5

CNT_DICE_PER_PLAYER = 5

SUGGESTED_AI_PLAYER_CNT = 2
SUGGESTED_PLAYER_NAME = "Captain"
SUGGESTED_WILD_ONES = False

AI_PLAYERS = {
    "Captain Blackbeard"     : 0.75, # big bluffer
    "Naga Seawitch"          : 0.55, # balanced
    "Devil Itslef"           : 0.66, # a bit cocky
    "The Pope"               : 0.33, # safe player
    "Little Red Riding Hood" : 0.50  # dzen
}

RESERVED_NAMES = set(AI_PLAYERS.keys())
#todo: add enum types for: move_type, 



def try_parse_int(int_string: str) -> int:
    try:
        return int(int_string)
    except:
        raise ValueError(f'Can\'t parse {int_string} to int!')

_BOOL_LOOKUP = {
    "yes"   : True,
    "y"     : True,
    "true"  : True,
    "no"    : False,
    "n"     : False,
    "false" : False
}
    
def try_parse_bool(bool_string: str) -> bool:
    
    result = _BOOL_LOOKUP.get(bool_string.strip().lower(), None)
    if result is None:
        raise ValueError(f'Can\'t parse {bool_string} to bool!')
    
    return result
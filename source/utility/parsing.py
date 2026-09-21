

def try_parse_int(int_string: str) -> int:
    try:
        return int(int_string)
    except:
        raise ValueError(f'Can\'t parse {int_string} to int!')
    
def try_parse_bool(bool_string: str) -> bool:
    
    norm_input = bool_string.lower()
    if norm_input.lower() == "yes":
        return True
    elif norm_input.lower() == "no":
        return False
    else:
        raise ValueError(f'Can\'t parse {bool_string} to bool!')
    
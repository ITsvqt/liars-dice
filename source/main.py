from utility import try_parse_int, try_parse_bool


cnt_opponents = try_parse_int(input('Enter number of AI opponents:\n\t'))
is_wild_ones_on = try_parse_bool(input('Do you want to enable wild ones?\n(Yes / No)\n\t'))
print(cnt_opponents)
print(is_wild_ones_on)
import string
from random import choice

ascii_letters = [x for x in string.ascii_lowercase]
numbers_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
symbols_list = [*ascii_letters, *numbers_list, "-"]


def generate_random_ct_for_req():
    ct0 = ''
    for _ in range(160):
        ct0 += str(choice(symbols_list))
    return ct0


def generate_random_state():
    state = ''
    for _ in range(43):
        state += str(choice(symbols_list))
    return state

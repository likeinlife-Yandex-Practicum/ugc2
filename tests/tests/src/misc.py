import random
from string import ascii_letters


def generate_string(length: int) -> str:
    return "".join(random.choices(ascii_letters, k=length))

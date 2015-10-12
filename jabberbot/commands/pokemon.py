import os
import random


def run_command(msg, *args):
    """Triggers encounter with a wild pokemon!"""
    dirpath = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dirpath, 'pokemon.txt')
    with open(filepath) as f:
        pokeymans = [poke.strip() for poke in f]
        return 'groupchat', 'A wild ' + random.choice(pokeymans) + ' appears!'

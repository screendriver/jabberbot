import os
import random


def run_command(msg, *args):
    """Makes a random joke"""
    dirpath = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dirpath, 'jokes.txt')
    with open(filepath) as f:
        jokes = [joke.strip() for joke in f]
        return 'groupchat', random.choice(jokes)

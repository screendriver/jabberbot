import random
import os

def slap(nick):
    """
    Slaps the given nick
    """
    if not nick:
        return 'You have to provide a nick name'
    dirpath = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dirpath, 'slaps.txt')
    with open(filepath) as f:
        slaps = tuple(slap.strip() for slap in f)
        return random.choice(slaps) % {'nick': nick}

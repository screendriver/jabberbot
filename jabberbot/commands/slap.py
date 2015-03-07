import os
import random


def run_command(msg, *args):
    """Slaps the given user

Simply type: !slap <nick> an it will slap the person
    """
    nick = ' '.join(args)
    if not nick:
        return 'groupchat', 'You have to provide a nick name'
    dirpath = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dirpath, 'slaps.txt')
    with open(filepath) as f:
        slaps = tuple(slap.strip() for slap in f)
        slap = random.choice(slaps).format(nick=nick)
        return 'groupchat', '/me {}'.format(slap)

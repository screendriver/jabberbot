import random


def muc_got_offline(nick):
    if random.choice([True, False]):
        return '{} hat den Raum verlassen? Besser isses'.format(nick)
    return None

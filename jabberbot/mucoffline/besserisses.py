from datetime import datetime, timedelta
import random

min_delta = timedelta(hours=1)
start = datetime.now()
messages = [
    '{} hat den Raum verlassen? Besser isses!',
    'Zum Glück ist {} freiwillig gegangen',
    'Endlich hat {} den Raum verlassen',
    'Pfiat di {}',
    '{} ist gerade noch so einem Kick entkommen',
]


def muc_got_offline(nick):
    global start
    if (datetime.now() - start) > min_delta:
        start = datetime.now()
        return random.choice(messages).format(nick)

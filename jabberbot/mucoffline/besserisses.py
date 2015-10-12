from datetime import datetime, timedelta

min_delta = timedelta(hours=1)
start = datetime.now()


def muc_got_offline(nick):
    if (datetime.now() - start) > min_delta:
        global start
        start = datetime.now()
        return '{} hat den Raum verlassen? Besser isses'.format(nick)

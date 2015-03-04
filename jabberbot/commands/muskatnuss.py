def run_command(msg, *args):
    """Returns 'Muskatnuss! Muskatnuss!!! 'err <nickname>!'"""
    nickname = 'Müller' if not args else ' '.join(args)
    return 'groupchat', 'Muskatnuss! Muskatnuss!!! \'err ' + nickname

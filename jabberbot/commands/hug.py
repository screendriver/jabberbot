def run_command(msg, *args):
    """Hugs the given user"""
    mtype = 'groupchat'
    if args:
        return mtype, '/me hugs {}'.format(' '.join(args))
    return mtype, 'Who should I hug?'

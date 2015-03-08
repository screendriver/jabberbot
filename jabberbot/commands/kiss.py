def run_command(msg, *args):
    """Kisses the given user

You can optionally specify the part of the body: \
kiss <nick> <part of body>
    """
    args_len = len(args)
    chat_type = 'groupchat'
    if not args:
        return chat_type, 'Who should I kiss?'
    if args_len == 1:
        return chat_type, '/me kisses {} :-*'.format(args[0])
    elif args_len == 2:
        return chat_type, '/me kisses {} on the {} :-*'.format(args[0],
                                                               args[1])
    else:
        return chat_type, 'Too many arguments'

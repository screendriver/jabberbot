import requests
import html


def run_command(msg, *args):
    """Displays a random Chuck Norris joke from http://icndb.com

    You can optionally change the name of the main character by appending \
    him as arguments: chuck <firstname> <lastname>
    """
    params = None
    if args:
        if len(args) != 2:
            return 'groupchat', 'You must append a firstname *and* a lastname'
        params = {'firstName': args[0], 'lastName': args[1]}
    request = requests.get('http://api.icndb.com/jokes/random',
                           params=params)
    joke = request.json()['value']['joke']
    return 'groupchat', html.unescape(joke)

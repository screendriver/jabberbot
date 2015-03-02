import requests
from html.parser import HTMLParser


def run_command(msg, *args):
    """Displays a random Chuck Norris joke from http://icndb.com

    You can optionally change the name of the main character by appending \
    him as arguments: chuck <firstname> <lastname>
    """
    params = None
    if args:
        if len(args) != 2:
            return 'You must append a firstname *and* a lastname'
        params = {'firstName': args[0], 'lastName': args[1]}
    request = requests.get('http://api.icndb.com/jokes/random',
                           params=params)
    joke = request.json()['value']['joke']
    return HTMLParser().unescape(joke)

#!/usr/bin/env python
from jabberbot import JabberBot, botcmd
from HTMLParser import HTMLParser
import logging
import requests

class MyJabberBot(JabberBot):
    def __init__(self, username, password, command_prefix = ''):
        super(MyJabberBot, self).__init__(username, password, command_prefix = command_prefix)
        self.PING_FREQUENCY = 300
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel(logging.DEBUG)

    @botcmd
    def chuck_norris(self, mess, args):
        """Displays a random Chuck Norris joke from http://icndb.com

You can change the name of the main character by appending it as arguments: chuck_norris firstname lastname
        """
        params = None
        if args:
            names = args.split(' ')
            if len(names) != 2:
                return 'You must append one firstname and one lastname'
            params = {'firstName': names[0], 'lastName': names[1]}
        request = requests.get('http://api.icndb.com/jokes/random', params = params)
        joke = request.json()['value']['joke']
        return HTMLParser().unescape(joke)

if __name__ == '__main__':
    username = ''
    password = ''
    nickname = ''
    chatroom = ''

    bot = MyJabberBot(username, password, '!')
    bot.join_room(chatroom, nickname)
    bot.serve_forever()

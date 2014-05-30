#!/usr/bin/env python
from jabberbot import JabberBot, botcmd
import logging
import json
import urllib2
import htmllib

class MyJabberBot(JabberBot):
    def __init__(self, username, password, command_prefix = ''):
        super(MyJabberBot, self).__init__(username, password, command_prefix = command_prefix)
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel(logging.DEBUG)

    @botcmd
    def chuck_norris(self, mess, args):
        """Displays a random Chuck Norris joke from http://icndb.com

You can change the name of the main character by appending it as arguments: chuck_norris firstnam lastname
        """
        url = 'http://api.icndb.com/jokes/random'
        if args:
            names = args.split(' ')
            if len(names) != 2:
                return 'You must append one firstname and one lastname'
            url += '?firstName=%s&lastName=%s' % (names[0], names[1])
            data = urllib2.urlopen(url)
            parsedJson = json.load(data)
            parser = htmllib.HTMLParser(None) # Escape HTML
            parser.save_bgn()
            parser.feed(parsedJson['value']['joke'])
            return parser.save_end()

if __name__ == '__main__':
    username = ''
    password = ''
    nickname = ''
    chatroom = ''

    bot = MyJabberBot(username, password, '!')
    bot.join_room(chatroom, nickname)
    bot.serve_forever()

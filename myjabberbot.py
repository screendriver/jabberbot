#!/usr/bin/env python
from jabberbot import JabberBot, botcmd
import json
import urllib2

class MyJabberBot(JabberBot):
    @botcmd
    def chuck_norris(self, mess, args):
        """Displays a random Chuck Norris joke from http://icndb.com"""
        data = urllib2.urlopen('http://api.icndb.com/jokes/random?escape=javascript')
        parsedJson = json.load(data)
        return parsedJson['value']['joke']


if __name__ == '__main__':
    username = ''
    password = ''
    nickname = ''
    chatroom = ''

    bot = MyJabberBot(username, password, command_prefix = '!')
    bot.join_room(chatroom, nickname)
    bot.serve_forever()

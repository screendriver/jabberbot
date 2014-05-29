#!/usr/bin/env python
from jabberbot import JabberBot, botcmd
import logging
import logging.handlers
import json
import urllib2
import htmllib

class MyJabberBot(JabberBot):
    def __init__(self, username, password, command_prefix = ''):
        super(MyJabberBot, self).__init__(username, password, command_prefix = command_prefix)
        self.log.addHandler(logging.StreamHandler())
        self.log.addHandler(logging.handlers.SysLogHandler(address = '/dev/log'))
        self.log.setLevel(logging.DEBUG)

    @botcmd
    def chuck_norris(self, mess, args):
        """Displays a random Chuck Norris joke from http://icndb.com"""
        data = urllib2.urlopen('http://api.icndb.com/jokes/random')
        parsedJson = json.load(data)
        parser = htmllib.HTMLParser(None)
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

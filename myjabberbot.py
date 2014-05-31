#!/usr/bin/env python
from jabberbot import JabberBot, botcmd
from HTMLParser import HTMLParser
import logging
import requests

class MyJabberBot(JabberBot):
    def __init__(self, username, password, shorturl_url, shorturl_signature):
        super(MyJabberBot, self).__init__(username, password, command_prefix = '!')
        self._shorturl_url = shorturl_url
        self._shorturl_signature = shorturl_signature
        self.PING_FREQUENCY = 300
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel(logging.DEBUG)

    @botcmd
    def chuck_norris(self, mess, args):
        """Displays a random Chuck Norris joke from http://icndb.com

You can optionally change the name of the main character by appending it as arguments: chuck_norris firstname lastname
        """
        params = None
        if args:
            names = args.split(' ')
            if len(names) != 2:
                return 'You must append a firstname *and* a lastname'
            params = {'firstName': names[0], 'lastName': names[1]}
        request = requests.get('http://api.icndb.com/jokes/random', params = params)
        joke = request.json()['value']['joke']
        return HTMLParser().unescape(joke)

    @botcmd
    def shorturl(self, mess, args):
        """Shorten a URL with the echooff URL shortener

shorturl http://myurl.com
        """
        if not args:
            return "You must provide a URL to shorten"
        params = {'signature': self._shorturl_signature,
                'url': args,
                'action': 'shorturl',
                'format': 'json'}
        request = requests.get(self._shorturl_url, params = params)
        if request.status_code == requests.codes.ok:
            json = request.json()
            return '%s: %s' % (json['title'], json['shorturl'])
        return 'Something went wrong :('

if __name__ == '__main__':
    username = ''
    password = ''
    shorturl_url = ''
    shorturl_signature = ''
    nickname = ''
    chatroom = ''

    bot = MyJabberBot(username, password, shorturl_url, shorturl_signature)
    bot.join_room(chatroom, nickname)
    bot.serve_forever()

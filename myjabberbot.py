#!/usr/bin/env python
from jabberbot import JabberBot, botcmd
from HTMLParser import HTMLParser
import logging
import requests

class MyJabberBot(JabberBot):
    _NO_VOTINGS_MESSAGE = 'No votings at the moment'

    def __init__(self, username, password, shorturl_url, shorturl_signature):
        super(MyJabberBot, self).__init__(username, password, command_prefix = '!')
        self._shorturl_url = shorturl_url
        self._shorturl_signature = shorturl_signature
        self._vote_subject = None
        self._votes_up = set()
        self._votes_down = set()
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

    @botcmd
    def vote_start(self, mess, args):
        """Starts a voting

You have to provide a subject: vote_start <the subject>
        """
        if (self._vote_subject):
            return 'A vote is already running'
        if (args == ''):
            return 'No subject given'
        self._vote_subject = args
        return 'Voting started'

    @botcmd
    def vote_up(self, mess, args):
        """Vote up for the current voting"""
        if not self._vote_subject:
            return self._NO_VOTINGS_MESSAGE
        jid = mess.getFrom().getResource()
        if jid in self._votes_up:
            return 'You already voted %s' % jid
        if jid in self._votes_down:
            self._votes_down.remove(jid)
        self._votes_up.add(jid)
        return 'Thank you for your vote %s' % jid

    @botcmd
    def vote_down(self, mess, args):
        """Vote down for the current voting"""
        if not self._vote_subject:
            return self._NO_VOTINGS_MESSAGE
        jid = mess.getFrom().getResource()
        if jid in self._votes_down:
            return 'You already voted down'
        if jid in self._votes_up:
            self._votes_up.remove(jid)
        self._votes_down.add(jid)
        return '%s voted down' % jid

    @botcmd
    def vote_stat(self, mess, args):
        """Displays statistics for the current voting"""
        if self._vote_subject:
            return 'Subject: "%s". Votes up: %d. Votes down: %d' % (
                    self._vote_subject,
                    len(self._votes_up),
                    len(self._votes_down))
        return self._NO_VOTINGS_MESSAGE

    @botcmd
    def vote_end(self, mess, args):
        """Ends the current voting and shows the result"""
        if not self._vote_subject:
            return self._NO_VOTINGS_MESSAGE
        result = 'Voting "%s" ended. %d votes up. %d votes down' % (
                self._vote_subject,
                len(self._votes_up),
                len(self._votes_down))
        self._vote_subject = None
        self._votes_up.clear()
        self._votes_down.clear()
        return result

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

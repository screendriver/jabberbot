#!/usr/bin/env python
from jabberbot import JabberBot, botcmd
from HTMLParser import HTMLParser
import logging
import requests
import slapper
import pyimgur

class MyJabberBot(JabberBot):
    _NO_VOTINGS_MESSAGE = 'No votings at the moment'

    def __init__(self, username, password, shorturl_url, shorturl_signature, imgur_client_id):
        super(MyJabberBot, self).__init__(username, password, command_prefix = '!')
        self._shorturl_url = shorturl_url
        self._shorturl_signature = shorturl_signature
        self._vote_subject = None
        self._votes_up = set()
        self._votes_down = set()
        self._slaps = ()
        self._imgur = pyimgur.Imgur(imgur_client_id)
        self.PING_FREQUENCY = 300
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel(logging.DEBUG)

    def bottom_of_help_message(self):
        return '\nSource code available at http://kurzma.ch/botsrc'

    @botcmd
    def help(self, mess, args):
        help_text = super(MyJabberBot, self).help(mess, args)
        self.send_simple_reply(mess, help_text, True)

    @botcmd
    def chuck(self, mess, args):
        """Displays a random Chuck Norris joke from http://icndb.com

You can optionally change the name of the main character by appending it as arguments: 
chuck_norris
firstname lastname
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
    def surl(self, mess, args):
        """Shorten a URL with the http://kurzma.ch URL shortener

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
    def vstart(self, mess, args):
        """Starts a voting

You have to provide a subject: vote_start <subject>
        """
        if self._vote_subject:
            return 'A vote is already running'
        if not args:
            return 'No subject given. Use vote_start <subject>'
        self._vote_subject = args
        return 'Voting started'

    @botcmd
    def vup(self, mess, args):
        """Vote up for the current voting"""
        if not self._vote_subject:
            return self._NO_VOTINGS_MESSAGE
        user = self.get_sender_username(mess)
        if user in self._votes_up:
            return 'You already voted %s' % user
        if user in self._votes_down:
            self._votes_down.remove(user)
        self._votes_up.add(user)
        return 'Thank you for your vote %s' % user

    @botcmd
    def vdown(self, mess, args):
        """Vote down for the current voting"""
        if not self._vote_subject:
            return self._NO_VOTINGS_MESSAGE
        user = self.get_sender_username(mess)
        if user in self._votes_down:
            return 'You already voted down'
        if user in self._votes_up:
            self._votes_up.remove(user)
        self._votes_down.add(user)
        return '%s voted down' % user

    @botcmd
    def vstat(self, mess, args):
        """Displays statistics for the current voting"""
        if self._vote_subject:
            return 'Subject: "%s". Votes up: %d. Votes down: %d' % (
                    self._vote_subject,
                    len(self._votes_up),
                    len(self._votes_down))
        return self._NO_VOTINGS_MESSAGE

    @botcmd
    def vend(self, mess, args):
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

    @botcmd
    def slap(self, mess, args):
        """Slaps the given user

Simply type: !slap <nick> an it will slap the person
        """
        try:
            return '/me ' + slapper.slap(args)
        except ValueError, e:
            return e.message

    @botcmd
    def imgur(self, mess, args):
        """Gets a random image from http://imgur.com"""
        image = self._imgur.get_random_gallery_image(limit = 1)[0]
        return '%s: %s' % (image.title, image.link)

    @botcmd
    def meal(self, mess, args):
        """Displays a 'enjoy your meal' message"""
        return 'Guten Appetit'

    @botcmd
    def hug(self, mess, args):
        """Hugs the given user"""
        return '/me hugs %s' % args

    @botcmd
    def kiss(self, mess, args):
        """Kisses the given user
        
You can optionally specify the part of the body: kiss <nick> <part of body>
        """
        arguments = args.split(' ')
        args_len = len(arguments)
        if args_len == 1:
            return '/me kisses %s :-*' % arguments[0]
        elif args_len == 2:
            return '/me kisses %s on the %s :-*' % (arguments[0], arguments[1])
        else:
            return 'Too many arguments'

if __name__ == '__main__':
    username = ''
    password = ''
    shorturl_url = ''
    shorturl_signature = ''
    imgur_client_id = ''
    nickname = ''
    chatroom = ''

    bot = MyJabberBot(username, password, shorturl_url, shorturl_signature, imgur_client_id)
    bot.join_room(chatroom, nickname)
    bot.serve_forever()

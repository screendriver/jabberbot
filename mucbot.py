#!/usr/bin/env python
import inspect
import logging
import os
import requests
from html.parser import HTMLParser

import slapper
from sleekxmpp import ClientXMPP

class MUCBot(ClientXMPP):
    _NO_VOTINGS_MESSAGE = 'No votings at the moment'
    _CMD_PREFIX = '!'

    def __init__(self, jid, password, shorturl_url, shorturl_signature,
                 imgur_client_id, room, nick):
        super().__init__(jid, password)
        self._shorturl_url = shorturl_url
        self._shorturl_signature = shorturl_signature
        self._vote_subject = None
        self._votes_up = set()
        self._votes_down = set()
        self._slaps = ()
        self._room = room
        self._nick = nick
        self._cmds = {'help': self._help,
                'chuck': self._chuck_norris,
                'surl': self._shorten_url}
        self._muc_cmds = {'help': self._help,
                'chuck': self._chuck_norris,
                'surl': self._shorten_url,
                'vstart': self._vote_start,
                'vup': self._vote_up,
                'vdown': self._vote_down,
                'vstat': self._vote_stat,
                'vend': self._vote_end,
                'slap': self._slap,
                'meal': self._meal,
                'hug': self._hug,
                'kiss': self._kiss}
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
        self.register_plugin('xep_0045')

    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self._room,
                self._nick,
                wait=True)

    def message(self, msg):
        body = msg['body']
        if not body.startswith(self._CMD_PREFIX):
            return
        msg_type = msg['type']
        cmd_args = body.strip().split(' ')
        # Strip command prefix
        cmd = cmd_args[0][len(self._CMD_PREFIX):]
        # MUC provides more commands as normal chat
        if msg_type in ('normal', 'chat'):
            cmds = self._cmds
        elif msg_type == 'groupchat':
            cmds = self._muc_cmds
        if cmd not in cmds:
            return
        resp = cmds[cmd](msg, cmd_args[1:])
        if msg_type in ('normal', 'chat'):
            msg.reply(resp).send()
        elif msg_type == 'groupchat':
            # Send help always as normal chat
            if cmd == 'help':
                self.send_message(mto=msg['from'],
                        mbody=resp,
                        mtype='chat')
            else:
                self.send_message(mto=msg['from'].bare,
                        mbody=resp,
                        mtype=msg_type)

    def _help(self, msg, args):
        """Returns a help string containing all commands"""
        msg_type = msg['type']
        # MUC provides more commands as normal chat
        if msg_type in ('normal', 'chat'):
            cmds = self._cmds
        elif msg_type == 'groupchat':
            cmds = self._muc_cmds
        docs = []
        if args: # help <command>
            cmd = args[0]
            if len(args) > 1 or cmd not in cmds:
                return
            doc = inspect.getdoc(cmds[cmd])
            docs.append(doc)
        else: # help
            docs.append('Available commands:{}'.format(os.linesep))
            for cmd in sorted(cmds.keys()):
                doc = inspect.getdoc(cmds[cmd])
                if cmd == 'help' or not doc:
                    continue
                lines = doc.splitlines()
                docs.append('{}{}: {}'.format(self._CMD_PREFIX, cmd, lines[0]))
            bottom = '{0}Type !help <command name> to get more info about that specific command.'.format(os.linesep)
            docs.append(bottom)
        src = 'Source code available at http://kurzma.ch/botsrc'
        docs.append(src)
        return os.linesep.join(docs)

    def _chuck_norris(self, msg, args):
        """Displays a random Chuck Norris joke from http://icndb.com

You can optionally change the name of the main character by appending him as arguments: 
chuck <firstname> <lastname>
        """
        params = None
        if args:
            if len(args) != 2:
                return 'You must append a firstname *and* a lastname'
            params = {'firstName': args[0], 'lastName': args[1]}
        request = requests.get('http://api.icndb.com/jokes/random', params = params)
        joke = request.json()['value']['joke']
        return HTMLParser().unescape(joke)

    def _shorten_url(self, mess, args):
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
            return '{}: {}'.format(json['title'], json['shorturl'])
        return 'Something went wrong :('

    def _vote_start(self, mess, args):
        """Starts a voting

You have to provide a subject: vstart <subject>
        """
        if self._vote_subject:
            return 'A vote is already running'
        if not args:
            return 'No subject given. Use vstart <subject>'
        self._vote_subject = ' '.join(args)
        return 'Voting started'

    def _vote_up(self, mess, args):
        """Vote up for the current voting"""
        if not self._vote_subject:
            return self._NO_VOTINGS_MESSAGE
        user = mess['from'].resource
        if user in self._votes_up:
            return 'You already voted {}'.format(user)
        if user in self._votes_down:
            self._votes_down.remove(user)
        self._votes_up.add(user)
        return '{} voted up'.format(user)

    def _vote_down(self, mess, args):
        """Vote down for the current voting"""
        if not self._vote_subject:
            return self._NO_VOTINGS_MESSAGE
        user = mess['from'].resource
        if user in self._votes_down:
            return 'You already voted down'
        if user in self._votes_up:
            self._votes_up.remove(user)
        self._votes_down.add(user)
        return '{} voted down'.format(user)

    def _vote_stat(self, mess, args):
        """Displays statistics for the current voting"""
        if self._vote_subject:
            return 'Subject: "{}". Votes up: {:d}. Votes down: {:d}'.format(
                    self._vote_subject,
                    len(self._votes_up),
                    len(self._votes_down))
        return self._NO_VOTINGS_MESSAGE

    def _vote_end(self, mess, args):
        """Ends the current voting and shows the result"""
        if not self._vote_subject:
            return self._NO_VOTINGS_MESSAGE
        result = 'Voting "{}" ended. {:d} votes up. {:d} votes down'.format(
                self._vote_subject,
                len(self._votes_up),
                len(self._votes_down))
        self._vote_subject = None
        self._votes_up.clear()
        self._votes_down.clear()
        return result

    def _slap(self, mess, args):
        """Slaps the given user

Simply type: !slap <nick> an it will slap the person
        """
        try:
            return '/me ' + slapper.slap(' '.join(args))
        except ValueError as e:
            return str(e)
        return '{}: {}'.format(image.title, image.link)

    def _meal(self, mess, args):
        """Displays a 'enjoy your meal' message"""
        return 'Guten Appetit'

    def _hug(self, mess, args):
        """Hugs the given user"""
        if args:
            return '/me hugs {}'.format(' '.join(args))
        else:
            return 'Who should I hug?'

    def _kiss(self, mess, args):
        """Kisses the given user

You can optionally specify the part of the body: kiss <nick> <part of body>
        """
        args_len = len(args)
        if not args:
            return 'Who should I kiss?'
        if args_len == 1:
            return '/me kisses {} :-*'.format(args[0])
        elif args_len == 2:
            return '/me kisses {} on the {} :-*'.format(args[0], args[1])
        else:
            return 'Too many arguments'

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR,
                        format='%(levelname)-8s %(message)s')
    jid = ''
    password = ''
    shorturl_url = ''
    shorturl_signature = ''
    imgur_client_id = ''
    room = ''
    nick = ''
    bot = MUCBot(jid, password, shorturl_url, shorturl_signature,
                 imgur_client_id, room, nick)
    bot.connect()
    bot.process(block=True)

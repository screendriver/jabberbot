#!/usr/bin/env python
import argparse
import importlib
import logging
import os
import pickle
import pkgutil
import random
import jabberbot.commands
from threading import Timer
from sleekxmpp import ClientXMPP

logger = logging.getLogger(__name__)


class MUCBot(ClientXMPP):
    _NO_VOTINGS_MESSAGE = 'No votings at the moment'
    cmd_prefix = '!'

    def __init__(self, jid, password, muc_room, muc_nick,
                 trans_client_id, trans_client_sec):
        super().__init__(jid, password)
        self.commands = {}
        self._muc_room = muc_room
        self._muc_nick = muc_nick
        cmdpath = jabberbot.commands.__path__
        for module_finder, name, ispkg in pkgutil.iter_modules(cmdpath):
            module = importlib.import_module('jabberbot.commands.' + name)
            if not hasattr(module, 'run_command'):
                continue
            module.trans_client_id = trans_client_id
            module.trans_client_sec = trans_client_sec
            module_name = module.__name__  # jabberbot.commands.foo
            command_name = module_name.rsplit('.', 1)[1]  # foo
            self.commands[command_name] = module
        self.register_plugin('xep_0045')
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('session_end', self.end)
        self.add_event_handler('message', self.message)
        self.add_event_handler('muc::{}::got_online'.format(muc_room),
                               self.muc_got_online)
        self._nicks_filename = 'subject_nicks'
        dirpath = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dirpath, self._nicks_filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w+b') as f:
                pickle.dump(set(), f)
        self._timer = Timer(random.randint(3600, 43200), self._change_subject)
        self._timer.start()

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.plugin['xep_0045'].joinMUC(self._muc_room,
                                        self._muc_nick,
                                        wait=True)

    def end(self, event):
        logger.debug('Cancelling timer')
        self._timer.cancel()

    def muc_got_online(self, presence):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dirpath, self._nicks_filename)
        with open(filepath, 'r+b') as f:
            nick = presence['muc']['nick']
            nicks = pickle.load(f)
            nicks.add(nick)
            f.seek(0)
            if nick not in nicks:
                logger.debug('Adding %s to %s', nick, self._nick_filename)
            pickle.dump(nicks, f)

    def message(self, msg):
        body = msg['body']
        if msg['type'] == 'groupchat' and body.startswith(self.cmd_prefix):
            cmd_args = body.strip().split(' ')
            # Strip command prefix e.g. !foo bar => foo
            cmd = cmd_args[0][len(self.cmd_prefix):]
            if cmd not in self.commands:
                logger.warning('Invalid command "%s"', cmd)
                return
            mtype, resp = self.commands[cmd].run_command(msg, *cmd_args[1:])
            msg_from = msg['from']
            if mtype == 'chat':
                mto = msg_from
            else:
                mto = msg_from.bare
            self.send_message(mto=mto,
                              mbody=resp,
                              mtype=mtype)

    def _change_subject(self):
        """Changes randomly the subject of the MUC"""
        dirpath = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dirpath, self._nicks_filename)
        with open(filepath, 'rb') as f:
            nicks = pickle.load(f)
        if nicks:
            nick = random.choice(list(nicks))
            subject = '{} ist ein Hengst'.format(nick)
            logger.debug('Changing MUC subject to "%s"', subject)
            self.send_message(mto=self._muc_room,
                              mbody=None,
                              msubject=subject,
                              mtype='groupchat')
        interval = random.randint(3600, 43200)
        logger.debug('Next MUC subject change in %d seconds', interval)
        self._timer = Timer(interval, self._change_subject)
        self._timer.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('jid',
                        help='the JID of the bot')
    parser.add_argument('pwd',
                        help='the password for the given JID')
    parser.add_argument('muc_room',
                        help='the MUC room to join')
    parser.add_argument('muc_nick',
                        help='the nick name that should be used')
    parser.add_argument('trans_client_id',
                        help='the translator client id')
    parser.add_argument('trans_client_sec',
                        help='the translator client secret')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')
    bot = MUCBot(args.jid, args.pwd, args.muc_room, args.muc_nick,
                 args.trans_client_id, args.trans_client_sec)
    bot.connect()
    bot.process(block=True)

#!/usr/bin/env python
import logging

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

class DevBot(ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        msg_type = msg['type']
        if msg_type in ('chat', 'normal'):
            msg.reply("/me says thank you for sending\n%(body)s" % msg).send()
        elif msg_type == 'groupchat':
            pass

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')
    username = 'devbot@jabber.echooff.de'
    password = '12345'
    bot = DevBot(username, password)
    bot.connect()
    bot.process(block=True)

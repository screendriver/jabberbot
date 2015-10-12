#!/usr/bin/env python
from jabberbot.mucbot import MUCBot

jid = ''
pwd = ''
muc_room = ''
muc_nick = ''
trans_client_id = ''
trans_client_sec = ''

bot = MUCBot(jid, pwd, muc_room, muc_nick, trans_client_id, trans_client_sec)
bot.connect()
bot.process(block=True)

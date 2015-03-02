import unittest
from unittest.mock import MagicMock
from jabberbot.mucbot import MUCBot


class TestMUCBot(unittest.TestCase):
    def setUp(self):
        self.bot = MUCBot(
            'foo@bar.org',
            'mypassword',
            'theroom@server.org',
            'itsme',
            'translator',
            'translator_sec'
        )

    def test_commands(self):
        commands = self.bot.commands
        self.assertEqual(len(commands), 1, 'expected 1 commands')
        self.assertTrue('chuck' in commands)

    def test_message(self):
        from_mock = MagicMock()
        call_count = 0

        def cmd(msg, *args):
            nonlocal call_count
            call_count += 1
        self.bot.commands['unittest'] = cmd
        msg = {'from': from_mock, 'type': 'message', 'body': 'cmd'}
        self.bot.message(msg)
        msg['type'] = 'groupchat'
        self.bot.message(msg)
        msg['type'] = 'message'
        msg['body'] = 'unittest'
        self.bot.message(msg)
        msg['type'] = 'groupchat'
        self.bot.message(msg)
        msg['body'] = '!notexist'
        self.bot.message(msg)
        msg['body'] = '!unittest'
        self.bot.message(msg)
        self.assertEqual(call_count, 1)

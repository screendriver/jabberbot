import unittest
from unittest.mock import MagicMock, patch, call
from mucbot import MUCBot


class TestMUCBot(unittest.TestCase):
    def setUp(self):
        self.nicknames = set()
        patcher = patch('builtins.open')
        self.addCleanup(patcher.stop)
        patcher.start()
        patcher = patch('random.randint', return_value=123)
        self.addCleanup(patcher.stop)
        self.mock_randint = patcher.start()
        patcher = patch('pickle.load', return_value=self.nicknames)
        self.addCleanup(patcher.stop)
        patcher.start()
        patcher = patch('mucbot.Timer')
        self.addCleanup(patcher.stop)
        self.mock_timer = patcher.start()
        patcher = patch.object(MUCBot, 'register_plugin')
        self.addCleanup(patcher.stop)
        patcher.start()
        patcher = patch.object(MUCBot, 'add_event_handler')
        self.addCleanup(patcher.stop)
        patcher.start()
        patcher = patch.object(MUCBot, 'send_message')
        self.addCleanup(patcher.stop)
        patcher.start()
        self.bot = MUCBot(
            'foo@bar.org',
            'mypassword',
            'theroom@server.org',
            'itsme',
            'translator',
            'translator_sec')

    def test_commands(self):
        commands = self.bot.commands
        self.assertEqual(len(commands), 3, 'expected 3 commands')
        self.assertTrue('chuck' in commands)

    def test_registered_plugins(self):
        self.assertIn(call('xep_0045'), self.bot.register_plugin.mock_calls)

    def test_add_event_handler(self):
        self.bot.add_event_handler.assert_has_calls([
            call('session_start', self.bot.start),
            call('session_end', self.bot.end),
            call('message', self.bot.message)
        ])

    def test_automatic_subject_change(self):
        self.mock_timer.assert_called_once_with(123, self.bot._change_subject)
        self.mock_timer.return_value.start.assert_called_once_with()
        # empty nicknames
        self.bot._change_subject()
        self.nicknames.add('test')
        self.bot._change_subject()
        # should only be called once. If there are no nicknames it should
        # not be called
        self.bot.send_message.assert_called_once_with(
            mto='theroom@server.org',
            mbody=None,
            msubject='test ist ein Hengst',
            mtype='groupchat')
        self.assertEqual(self.mock_randint.call_count, 3)
        self.mock_randint.assert_has_calls([
            call(3600, 43200),
            call(3600, 43200),
            call(3600, 43200)
        ])
        self.assertEqual(self.mock_timer.call_count, 3)
        self.assertEqual(self.mock_timer.return_value.start.call_count, 3)

    def test_start(self):
        self.bot.send_presence = MagicMock(name='send_presence')
        self.bot.get_roster = MagicMock(name='get_roster')
        self.bot.plugin = MagicMock(name='xep_0045')
        self.bot.start(None)
        self.assertTrue(self.bot.send_presence.called)
        self.assertTrue(self.bot.get_roster.called)
        self.bot.plugin['xep_0045'].joinMUC.assert_called_once_with(
            'theroom@server.org',
            'itsme',
            wait=True)

    def test_end(self):
        self.bot.end(None)
        self.mock_timer.return_value.cancel.assert_called_once_with()

    def test_message_type_not_groupchat(self):
        msg = {'body': None, 'type': 'chat'}
        self.bot.message(msg)
        msg['type'] = 'foo'
        self.bot.message(msg)
        msg['type'] = None
        self.bot.message(msg)
        self.assertFalse(self.bot.send_message.called)

    def test_message_no_command_prefix(self):
        self.bot.commands['help'] = MagicMock(name='help')
        msg = {'body': '', 'type': 'groupchat'}
        self.bot.message(msg)
        msg['body'] = 'foo'
        self.bot.message(msg)
        msg['body'] = 'help'
        self.bot.message(msg)
        self.assertFalse(self.bot.send_message.called)

    def test_message_command_not_found(self):
        self.bot.commands['help'] = MagicMock(name='help')
        msg = {'body': '!foo', 'type': 'groupchat'}
        self.bot.message(msg)
        self.assertFalse(self.bot.send_message.called)

    def test_message_to_groupchat(self):
        self.bot.commands['help'] = MagicMock(
            name='help',
            return_value=('groupchat', 'message body'))
        msg = {'from': MagicMock(), 'type': 'groupchat', 'body': '!help'}
        self.bot.message(msg)
        self.bot.send_message.assert_called_once_with(
            mto=msg['from'].bare,
            mbody='message body',
            mtype='groupchat')

    def test_message_to_chat(self):
        self.bot.commands['help'] = MagicMock(
            name='help',
            return_value=('chat', 'message body'))
        msg = {'from': MagicMock(), 'type': 'groupchat', 'body': '!help'}
        self.bot.message(msg)
        self.bot.send_message.assert_called_once_with(
            mto=msg['from'],
            mbody='message body',
            mtype='chat')

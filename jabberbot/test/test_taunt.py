import unittest
from io import StringIO
from unittest.mock import patch
from commands import taunt


class TestTauntCommand(unittest.TestCase):
    def setUp(self):
        self.jokes = ['{nick} first taunt.', '{nick} second taunt.']
        self.stringio = StringIO('hmm')
        self.stringio.write(self.jokes[0] + '\n')
        self.stringio.write(self.jokes[1])
        self.stringio.seek(0)
        patcher = patch('builtins.open')
        self.addCleanup(patcher.stop)
        self.mock_open = patcher.start()
        self.mock_open.return_value = self.stringio

    def tearDown(self):
        self.stringio.close()

    def test_with_nickname(self):
        mtype, resp = taunt.run_command(None, 'nickname')
        self.assertEqual(mtype, 'groupchat')
        formatted = [joke.format(nick="nickname's") for joke in self.jokes]
        self.assertIn(resp, formatted)

    def test_without_nickname(self):
        mtype, resp = taunt.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        formatted = [joke.format(nick='Deine') for joke in self.jokes]
        self.assertIn(resp, formatted)

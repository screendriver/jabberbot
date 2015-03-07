import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch
from jabberbot.commands import taunt


class TestTauntCommand(unittest.TestCase):
    def setUp(self):
        self.taunts = ['{nick} first taunt.', '{nick} second taunt.']
        self.stringio = StringIO()
        self.stringio.write(self.taunts[0] + '\n')
        self.stringio.write(self.taunts[1])
        self.stringio.seek(0)
        patcher = patch('builtins.open')
        self.addCleanup(patcher.stop)
        self.mock_open = patcher.start()
        self.mock_open.return_value = self.stringio

    def tearDown(self):
        self.stringio.close()

    def test_textfile_exist(self):
        path = Path('jabberbot/commands/mother_jokes.txt')
        self.assertTrue(path.exists())
        self.assertTrue(path.is_file())

    def test_with_nickname(self):
        mtype, resp = taunt.run_command(None, 'nickname')
        self.assertEqual(mtype, 'groupchat')
        formatted = [t.format(nick="nickname's") for t in self.taunts]
        self.assertIn(resp, formatted)

    def test_without_nickname(self):
        mtype, resp = taunt.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        formatted = [t.format(nick='Deine') for t in self.taunts]
        self.assertIn(resp, formatted)

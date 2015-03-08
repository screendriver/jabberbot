import unittest
from jabberbot.commands import hug


class TestHugCommand(unittest.TestCase):
    def test_run_command_without_args(self):
        mtype, resp = hug.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'Who should I hug?')

    def test_run_command_with_args(self):
        mtype, resp = hug.run_command(None, 'foo')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, '/me hugs foo')

import unittest
from jabberbot.commands import matt


class TestMatttCommand(unittest.TestCase):
    def test_run_command(self):
        mtype, resp = matt.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'Matt Damon!')

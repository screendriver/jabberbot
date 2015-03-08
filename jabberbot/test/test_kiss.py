import unittest
from jabberbot.commands import kiss


class TestKissCommand(unittest.TestCase):
    def test_run_command_without_args(self):
        mtype, resp = kiss.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'Who should I kiss?')

    def test_run_command_without_one_arg(self):
        mtype, resp = kiss.run_command(None, 'foo')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, '/me kisses foo :-*')

    def test_run_command_without_two_args(self):
        mtype, resp = kiss.run_command(None, 'foo', 'bar')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, '/me kisses foo on the bar :-*')

    def test_run_command_without_three_arg(self):
        mtype, resp = kiss.run_command(None, 'foo', 'bar', 'hello')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'Too many arguments')

import unittest
from io import StringIO
from unittest.mock import patch
from jabberbot.commands import slap


@patch('builtins.open')
class TestSlapCommand(unittest.TestCase):
    def test_run_command_without_nick(self, mock_open):
        mtype, resp = slap.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'You have to provide a nick name')

    def test_run_command(self, mock_open):
        slaps = ['slap {nick} once', 'slap {nick} twice']
        stringio = StringIO()
        stringio.write(slaps[0] + '\n')
        stringio.write(slaps[1])
        stringio.seek(0)
        mock_open.return_value = stringio
        mtype, resp = slap.run_command(None, 'foo')
        self.assertEqual(mtype, 'groupchat')
        self.assertIn(resp, ['/me ' + s.format(nick='foo') for s in slaps])

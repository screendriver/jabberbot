import unittest
from commands import joke
from io import StringIO
from unittest.mock import patch


@patch('builtins.open')
class TestJokeCommand(unittest.TestCase):
    def test_run_command(self, mock_open):
        jokes = ['first joke.', 'second joke.']
        stringio = StringIO()
        stringio.write(jokes[0] + '\n')
        stringio.write(jokes[1])
        stringio.seek(0)
        mock_open.return_value = stringio
        mtype, resp = joke.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        self.assertIn(resp, jokes)
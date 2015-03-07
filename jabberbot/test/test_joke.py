import unittest
from pathlib import Path
from io import StringIO
from unittest.mock import patch
from jabberbot.commands import joke


@patch('builtins.open')
class TestJokeCommand(unittest.TestCase):
    def test_textfile_exist(self, mock_open):
        path = Path('jabberbot/commands/jokes.txt')
        self.assertTrue(path.exists())
        self.assertTrue(path.is_file())

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

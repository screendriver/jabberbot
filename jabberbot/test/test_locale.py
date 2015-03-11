import unittest
import random
from io import StringIO
from pathlib import Path
from unittest.mock import patch
from jabberbot import locale


class TestLocale(unittest.TestCase):
    def test_text_file_exist(self):
        path = Path('jabberbot/lang_codes.txt')
        self.assertTrue(path.exists())
        self.assertTrue(path.is_file())

    @patch('builtins.open')
    @patch.object(random, 'choice')
    def test_random(self, mock_rchoice, mock_open):
        mock_rchoice.return_value = 'en'
        with StringIO() as stringio:
            stringio.write('de;German\n')
            stringio.write('en;English\n')
            stringio.write('fr;French')
            stringio.seek(0)
            mock_open.return_value = stringio
            lang_code, country = locale.random()
        self.assertEqual(lang_code, 'en')
        self.assertEqual(country, 'English')
        # args = /path/to/lang_codes.txt
        args, kwargs = mock_open.call_args
        self.assertIn('lang_codes.txt', args[0])

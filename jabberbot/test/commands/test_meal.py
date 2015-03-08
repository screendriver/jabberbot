import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch
from jabberbot.commands import meal


class TestMealCommand(unittest.TestCase):
    def setUp(self):
        meal.trans_client_id = 'foo'
        meal.trans_client_sec = 'bar'

    def test_textfile_exist(self):
        path = Path('jabberbot/commands/lang_codes.txt')
        self.assertTrue(path.exists())
        self.assertTrue(path.is_file())

    @patch('builtins.open')
    @patch('random.choice')
    @patch('jabberbot.commands.meal.Translator')
    def test_run_command(self, mock_translator, mock_rchoice, mock_open):
        choice_return_value = 'en'
        translated = 'unit test'
        mock_translator.return_value.translate.return_value = translated
        mock_rchoice.return_value = choice_return_value
        with StringIO() as stringio:
            stringio.write('en;English')
            stringio.seek(0)
            mock_open.return_value = stringio
            mtype, resp = meal.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, '{} (translated to English)'.format(translated))
        mock_translator.assert_called_once_with('foo', 'bar')
        mock_translator.return_value.translate.assert_called_once_with(
            'Enjoy your meal',
            choice_return_value)
        # args = /path/to/lang_codes.txt
        args, kwargs = mock_open.call_args
        self.assertIn('lang_codes.txt', args[0])

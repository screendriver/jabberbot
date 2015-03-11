import unittest
from jabberbot import locale
from unittest.mock import patch
from jabberbot.commands import meal


class TestMealCommand(unittest.TestCase):
    def setUp(self):
        meal.trans_client_id = 'foo'
        meal.trans_client_sec = 'bar'

    @patch.object(locale, 'random')
    @patch('jabberbot.commands.meal.Translator')
    def test_run_command(self, mock_translator, mock_random):
        translated = 'unit test'
        mock_random.return_value = 'en', 'English'
        mock_translator.return_value.translate.return_value = translated
        mtype, resp = meal.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, '{} (translated to English)'.format(translated))
        mock_translator.assert_called_once_with('foo', 'bar')
        mock_translator.return_value.translate.assert_called_once_with(
            'Enjoy your meal',
            'en')

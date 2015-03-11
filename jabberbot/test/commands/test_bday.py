import unittest
import jabberbot.locale
from unittest.mock import patch
from jabberbot.commands import bday


@patch.object(jabberbot.locale, 'random')
@patch('jabberbot.commands.bday.Translator')
class TestBirthdayCommand(unittest.TestCase):
    def setUp(self):
        bday.trans_client_id = 'foo'
        bday.trans_client_sec = 'bar'

    def test_run_command_with_nickname(self, mock_translator, mock_random):
        mock_random.return_value = 'en', 'English'
        mock_translator.return_value.translate.return_value = 'unit test'
        mtype, resp = bday.run_command(None, 'mynick')
        mock_translator.assert_called_once_with('foo', 'bar')
        mock_translator.return_value.translate.assert_called_once_with(
            'Happy birthday to you',
            'en')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'unit test @mynick (translated to English)')

    def test_run_command_without_nickname(self, mock_translator, mock_random):
        mock_random.return_value = 'en', 'English'
        mock_translator.return_value.translate.return_value = 'unit test'
        mtype, resp = bday.run_command(None)
        mock_translator.assert_called_once_with('foo', 'bar')
        mock_translator.return_value.translate.assert_called_once_with(
            'Happy birthday to you',
            'en')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'unit test (translated to English)')

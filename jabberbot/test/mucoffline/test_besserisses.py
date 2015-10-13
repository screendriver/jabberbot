from datetime import datetime, timedelta
import random
import unittest
from unittest.mock import patch
from jabberbot.mucoffline import besserisses


@patch.object(random, 'choice')
@patch.object(besserisses, 'datetime')
class TestBesserIsses(unittest.TestCase):
    def test_timedelta(self, mock_datetime, mock_choice):
        self.assertEqual(besserisses.min_delta, timedelta(hours=1))

    def test_muc_got_offline_after_30_minutes(self, mock_datetime,
                                              mock_choice):
        now = datetime.now() + timedelta(minutes=30)
        mock_datetime.now.side_effect = lambda: now
        message = besserisses.muc_got_offline('foo')
        self.assertIsNone(message)

    def test_muc_got_offline_after_65_minutes(self, mock_datetime,
                                              mock_choice):
        old_start = besserisses.start
        now = datetime.now() + timedelta(minutes=65)
        mock_datetime.now.return_value = now
        messages = iter(besserisses.messages)
        mock_choice.side_effect = lambda msgs: next(messages)
        message = besserisses.muc_got_offline('foo')
        self.assertEqual(message, 'foo hat den Raum verlassen? Besser isses!')
        besserisses.start = old_start
        message = besserisses.muc_got_offline('foo')
        self.assertEqual(message, 'Zum Glück ist foo freiwillig gegangen')
        besserisses.start = old_start
        message = besserisses.muc_got_offline('foo')
        self.assertEqual(message, 'Endlich hat foo den Raum verlassen')
        besserisses.start = old_start
        message = besserisses.muc_got_offline('foo')
        self.assertEqual(message, 'Pfiat di foo')
        besserisses.start = old_start
        message = besserisses.muc_got_offline('foo')
        self.assertEqual(message,
                         'foo ist gerade noch so einem Kick entkommen')
        self.assertEqual(besserisses.start, now)

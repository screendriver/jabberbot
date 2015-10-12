from datetime import datetime, timedelta
import unittest
from unittest.mock import patch
from jabberbot.mucoffline import besserisses


@patch.object(besserisses, 'datetime')
class TestBesserIsses(unittest.TestCase):
    def test_timedelta(self, mock_datetime):
        self.assertEqual(besserisses.min_delta, timedelta(hours=1))

    def test_muc_got_offline_after_30_minutes(self, mock_datetime):
        now = datetime.now() + timedelta(minutes=30)
        mock_datetime.now.side_effect = lambda: now
        message = besserisses.muc_got_offline('foo')
        self.assertIsNone(message)

    def test_muc_got_offline_after_65_minutes(self, mock_datetime):
        now = datetime.now() + timedelta(minutes=65)
        mock_datetime.now.side_effect = lambda: now
        message = besserisses.muc_got_offline('foo')
        self.assertEqual(message, 'foo hat den Raum verlassen? Besser isses')
        self.assertEqual(besserisses.start, now)

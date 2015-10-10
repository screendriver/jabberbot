import random
import unittest
from unittest.mock import patch
from jabberbot.mucoffline import besserisses


@patch.object(random, 'choice')
class TestBesserIsses(unittest.TestCase):
    def test_muc_got_offline(self, mock_random):
        mock_random.return_value = True
        message = besserisses.muc_got_offline('foo')
        self.assertEqual(message, 'foo hat den Raum verlassen? Besser isses')

        mock_random.return_value = False
        message = besserisses.muc_got_offline('foo')
        self.assertIsNone(message)

import unittest
from jabberbot.mucbot import MUCBot


class TestMUCBot(unittest.TestCase):
    def setUp(self):
        self.bot = MUCBot()
        print(self.bot)

    def test_command_loader(self):
        self.assertEqual(True, True)

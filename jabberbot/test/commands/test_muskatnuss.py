import unittest
from jabberbot.commands import muskatnuss


class TestMuskatnussCommand(unittest.TestCase):
    def test_run_command_without_name(self):
        mtype, resp = muskatnuss.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'Muskatnuss! Muskatnuss!!! \'err Müller')

    def test_run_command_with_name(self):
        mtype, resp = muskatnuss.run_command(None, 'foo')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'Muskatnuss! Muskatnuss!!! \'err foo')

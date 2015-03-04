import unittest
import requests
from unittest.mock import patch
from commands import chuck


class TestChuckCommand(unittest.TestCase):
    def setUp(self):
        jokes = {'value': {'joke': '&gt;the joke&lt;'}}
        patcher = patch.object(requests, 'get', spec_set=dict)
        self.addCleanup(patcher.stop)
        self.mock_request = patcher.start()
        json = self.mock_request.return_value.json
        json.return_value.__getitem__.side_effect = lambda name: jokes[name]

    def test_run_command_without_args(self):
        mtype, resp = chuck.run_command(None)
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, '>the joke<')
        self.mock_request.assert_called_once_with(
            'http://api.icndb.com/jokes/random',
            params=None)

    def test_run_command_with_to_few_args(self):
        mtype, resp = chuck.run_command(None, 'firstname')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'You must append a firstname *and* a lastname')
        self.assertFalse(self.mock_request.called)

    def test_run_command_with_to_many_args(self):
        mtype, resp = chuck.run_command(None, 'firstname', 'lastname', 'other')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, 'You must append a firstname *and* a lastname')
        self.assertFalse(self.mock_request.called)

    def test_run_command_with_first_and_lastname(self):
        mtype, resp = chuck.run_command(None, 'firstname', 'lastname')
        self.assertEqual(mtype, 'groupchat')
        self.assertEqual(resp, '>the joke<')
        self.mock_request.assert_called_once_with(
            'http://api.icndb.com/jokes/random',
            params={'firstName': 'firstname', 'lastName': 'lastname'})

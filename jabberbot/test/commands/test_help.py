import importlib
import pkgutil
import unittest
from unittest.mock import patch
from jabberbot.commands import help


class TestHelpCommand(unittest.TestCase):
    def setUp(self):
        patcher = patch.object(pkgutil, 'iter_modules')
        self.addCleanup(patcher.stop)
        mock_iter_modules = patcher.start()
        generator = ((None, 'help_test', None) for num in range(1))
        mock_iter_modules.return_value = generator
        patcher = patch.object(importlib, 'import_module')
        self.addCleanup(patcher.stop)
        mock_import_module = patcher.start()
        name = 'jabberbot.commands.test_command'
        mock_import_module.return_value.__name__ = name

    def test_run_command_with_command_not_found(self):
        mtype, resp = help.run_command(None, 'foo')
        self.assertEqual(mtype, 'chat')
        self.assertEqual(resp, 'Command not found')

    def test_run_command_with_command(self):
        mtype, resp = help.run_command(None, 'test_command')
        self.assertEqual(mtype, 'chat')
        self.assertNotIn('Available commands', resp)
        self.assertIn(('MagicMock is a subclass of Mock '
                       'with default implementations'), resp)
        self.assertIn(('Source code available at '
                       'https://github.com/ScreenDriver/jabberbot'), resp)

    def test_run_command_without_command(self):
        mtype, resp = help.run_command(None)
        self.assertEqual(mtype, 'chat')
        self.assertIn('Available commands', resp)
        self.assertIn(('Type !help <command name> to get more info '
                       'about that specific command.'), resp)
        self.assertIn(('Source code available at '
                       'https://github.com/ScreenDriver/jabberbot'), resp)

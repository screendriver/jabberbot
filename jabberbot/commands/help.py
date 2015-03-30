import importlib
import inspect
import jabberbot
import pkgutil
import os
from jabberbot.mucbot import MUCBot


def run_command(msg, *args):
    """Returns a help string containing all commands"""
    docs = {}
    cmdpath = jabberbot.commands.__path__
    for module_finder, name, ispkg in pkgutil.iter_modules(cmdpath):
        module = importlib.import_module('jabberbot.commands.' + name)
        if not hasattr(module, 'run_command'):
            continue
        doc = inspect.getdoc(module.run_command)
        if not doc:
            continue
        module_name = module.__name__  # jabberbot.commands.foo
        command_name = module_name.rsplit('.', 1)[1]  # foo
        docs[command_name] = doc
    message = []
    if args:  # help <command>
        cmd = args[0]
        if len(args) > 1 or cmd not in docs:
            return 'chat', 'Command not found'
        message.append(docs[cmd])
    else:  # help
        message.append('Available commands:{}'.format(os.linesep))
        for cmd in sorted(docs.keys()):
            if cmd == 'help':
                continue
            doc = docs[cmd]
            lines = doc.splitlines()
            message.append('{}{}: {}'.format(MUCBot.cmd_prefix,
                                             cmd,
                                             lines[0]))
        bottom = ('{0}Type !help <command name> to get more info '
                  'about that specific command.').format(os.linesep)
        message.append(bottom)
    src = 'Source code available at https://github.com/ScreenDriver/jabberbot'
    message.append(src)
    return 'chat', os.linesep.join(message)

jabberbot [![Build Status](https://travis-ci.org/screendriver/jabberbot.svg?branch=master)](https://travis-ci.org/screendriver/jabberbot)
==========

A Jabber Bot for my XMPP service. Written in [Python](https://www.python.org).

## Prerequisites

  - [Python 3.4](https://www.python.org)
  - optional [Vagrant](https://www.vagrantup.com)
  - if you use Vagrant: [rsync](https://rsync.samba.org)
  - if you use Vagrant und Windows: [cygwin](http://www.cygwin.com)

## Setup

The environment is based on [Vagrant](https://www.vagrantup.com). But this is
optional. You still can test und run everything without it but with Vagrant
you don't have to care about anything. Just type a simple

```bash
$ vagrant up
```

and everything will be set up for you. After that you can ssh into the VM

```bash
$ vagrant ssh
```

After that you can run all Python related commands within the VM. All
dependencies and environment variables are already set for you. Now you
can modify and add any file on the **host** just like in any development
environment. If you are done you can synchronize your changes to the **guest**
manually

```bash
$ vagrant rsync
```

If you want to synchronize automatically every change you can do

```bash
$ vagrant rsync-auto
```

in a separate terminal window.

## Commands

All commands are defined in the ```jabberbot.commands``` package. If you want
to add a command to the bot you add a Python module with the name the command
should be. For example if you add the module ```foo.py``` to the
```jabberbot.commands``` package the command will be available as ```!foo```.
In ```foo.py``` you can make everything you want and everything you can do with
Python. The only thing that must exist is a function with the signature

```python
def run_command(msg, *args):
  return 'groupchat', 'hello world'
```

This function will be called if a user wrote the command to the chat room. The
first argument ```msg``` is the raw XMPP message. The second argument
```*args``` is a tuple with optional arguments. For example the user can call
a command without arguments like ```!help``` or with arguments like
```!help foo bar```.

```run_command``` must return a tuple with two items. The first item defines
where the response should be sent. Either to the ```groupchat``` or as private
```chat```. The second item is the message as a string.

## Unit tests

All [unit tests](https://docs.python.org/3/library/unittest.html) run without
any plugins. Everything is shipped with the Python standard library.
Just run it with a simple

```bash
$ python -m unittest
```

## Test in a chat room

If you want to test your command in a real world environment, a chat room, and
not only in unit tests you can use the provided
[chatroom_test.py](chatroom_test.py) script. Just fill all predefined variables
and run your script

```bash
$ python chatroom_test.py
```

#!/usr/bin/env python3

import discord
import asyncio
import os
from threading import Thread

import database
import config

client = discord.Client()


@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print('------')

    # start the web app in a seperate thread so it doesn't lock up this one
    thread = Thread(target=database.app.run)
    thread.start()


@client.event
async def on_message(message):
    author, authorid = str(message.author).split('#')

    # if the author of the message is the bot itself do nothing
    if author == client.user.name:
        return

    # add the author to the database if they're not already there
    users = database.User.query.all()
    if int(authorid) not in [user.usernum for user in users]:
        database.db.session.add(database.User(author, authorid))
        database.db.session.commit()
        print('Added {} to the database'.format(author))

    # run a command if one is issued in the message
    if message.content.startswith(config.COMMAND_SYMBOL):
        print('{} issued command {}'.format(author, message.content))
        command, _, args = message.content[1:].partition(' ')

        # find the function and minimum permission level for the command
        command_func, min_permissionlevel = COMMANDS.get(
            command,
            # if the command is not found in COMMANDS
            (lambda _: 'Command not found', 0))

        # fetch the author's permission level from the database
        author_permissionlevel = database.User.query.filter(database.User.usernum == authorid)\
                                 .first().permissions

        # check if the author has enough permissions to use the command
        if author_permissionlevel >= min_permissionlevel:
            await client.send_message(message.channel, command_func(args))
        else:
            await client.send_message(message.channel,
                                      'You do not have enough permissions to use ' + command)


def test_command(_):
    """Test if the bot is responding"""
    return 'Appears to work!'


def help_command(_):
    """List all available commands"""
    msg = '```{:<12} {:<40} {:>20}\n'.format('command', 'function', 'required permissions')
    for k, v in COMMANDS.items():
        msg += '{:<12} {:<40} {:>20}\n'.format(k, v[0].__doc__, v[1])
    return msg + '```'


def list_users(_):
    """List all users in the database"""
    users = database.User.query.all()
    msg = '```{:<4} {:<30} {:<12} {}\n'.format('id', 'name', 'usernum', 'permissionlevel')
    for u in users:
        msg += '{:<4} {:<30} {:<12} {}\n'.format(u.id, u.name, u.usernum, u.permissions)
    return msg + '```'


COMMANDS = {
    # command: (function_it_points_to, minimum_permissionlevel)
    'test': (test_command, 0),
    'help': (help_command, 0),
    'users': (list_users, 20),
}

client.run(config.DISCORD_TOKEN)
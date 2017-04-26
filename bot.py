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
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    # start the web app in a seperate thread so it doesn't lock up this one
    thread = Thread(target=database.run)
    thread.start()

@client.event
async def on_message(message):
    author, authorid = str(message.author).split('#')
    if author == client.user.name: # bot doesn't read its own messages, that would be silly
        return

    users = database.User.query.all()
    if int(authorid) not in [user.usernum for user in users]:
        database.db.session.add(database.User(author, authorid))
        database.db.session.commit()
        print('Added {} to the database'.format(author))

    if message.content.startswith(config.COMMAND_SYMBOL):
        command, _, args = message.content[1:].partition(' ')
        # command_func points to the function that corresponds to the command
        command_func, min_permissionlevel, _ = COMMANDS.get(command, (notfound, 0, None))
        author_permissionlevel = database.User.query.filter(database.User.usernum == authorid)\
                                 .first().permissions
        if author_permissionlevel >= min_permissionlevel:
            await client.send_message(message.channel, command_func(args))
        else:
            await client.send_message(message.channel,
                                      'You do not have enough permissions to use ' + command)

def notfound(_):
    return 'Unknown command'

def test_command(_):
    return 'Appears to work!'

def help_command(_):
    msg = '```{:<12} {:<40} {:>20}\n'.format('command', 'function', 'required permissions')
    for k, v in COMMANDS.items():
        msg += '{:<12} {:<40} {:>20}\n'.format(k, v[2], v[1])
    return msg + '```'

def list_users(_):
    users = database.User.query.all()
    msg = '```{:<4} {:<30} {:<12} {}\n'.format('id', 'name', 'usernum', 'permissionlevel')
    for u in users:
        msg += '{:<4} {:<30} {:<12} {}\n'.format(u.id, u.name, u.usernum, u.permissions)
    return msg + '```'

COMMANDS = {
    # command: (function_it_points_to, minimum_permissionlevel, documentation)
    'test': (test_command, 0, 'Testing command'),
    'help': (help_command, 0, 'List all commands'),
    'users': (list_users, 20, 'List all users who are in the database'),
}

client.run(config.DISCORD_TOKEN)

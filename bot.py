import asyncio
import os
from functools import reduce

import discord

import config
import app

client = discord.Client()


def run():
    """Run the bot"""
    print("Hello?")
    client.run(config.DISCORD_TOKEN)


@client.event
async def on_ready():
    print('Connected to Discord!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)


@client.event
async def on_message(message):
    async def send(data):
        """Send text or files the correct way"""
        try:
            await client.send_file(message.channel, data)
        except:
            # split the data to multiple messages if it's too long
            if data.startswith('```'):
                data, md = data.replace('```', ''), '```'
            else:
                md = ''
            m = data.splitlines()
            for i in range(0, len(m), 30):
                await client.send_message(message.channel, md + '\n'.join(m[i:i+30]) + md)

    author, authorid = str(message.author).split('#')

    # if the author of the message is the bot itself do nothing
    if author == client.user.name:
        return

    # add the author to the database if they're not already there
    users = app.User.query.all()
    if int(authorid) not in [user.usernum for user in users]:
        app.db.session.add(app.User(author, authorid))
        app.db.session.commit()
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
        author_permissionlevel = app.User.query.filter(app.User.usernum == authorid)\
                                 .first().permissions

        # check if the author has enough permissions to use the command
        if author_permissionlevel >= min_permissionlevel:
            await send(command_func(args))
        else:
            await send('You do not have enough permissions to use ' + command)


# these are the functions corresponding to the bot's commands
# they all require one parameter so I'm using _ here as a throwaway one


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
    users = app.User.query.all()
    msg = '```{:<4} {:<30} {:<12} {}\n'.format('id', 'name', 'usernum', 'permissionlevel')
    for u in users:
        msg += '{:<4} {:<30} {:<12} {}\n'.format(u.id, u.name, u.usernum, u.permissions)
    return msg + '```'


def list_files(_):
    """List all files uploaded"""
    return reduce((lambda a, b: a + ', ' + b), app.list_files())


def get_file(filename):
    """Get a file"""
    return app.get_file(filename)


COMMANDS = {
    # command: (function_it_points_to, minimum_permissionlevel)
    'test': (test_command, 0),
    'help': (help_command, 0),
    'users': (list_users, 20),
    'files': (list_files, 30),
    'getfile': (get_file, 30),
}

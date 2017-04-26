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
        await client.send_message(message.channel, {
            'test': test,
            'users': list_users,
        }.get(command, notfound)(args))

def notfound(_):
    return 'Unknown command'

def test(_):
    return 'Appears to work!'

def list_users(_):
    users = database.User.query.all()
    msg = ''
    for user in users:
        msg += 'id: {} name: {} usernum: {} permissionlevel: {}\n'.format(
            user.id, user.name, user.usernum, user.permissions)
    return msg

client.run(config.DISCORD_TOKEN)

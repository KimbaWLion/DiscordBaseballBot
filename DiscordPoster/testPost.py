#!/usr/bin/env python

"""
testing out this discord.py thing
"""

import discord
import time
import asyncio
from discord.ext.commands import Bot

TOKEN = 'TOKEN'
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
GAME_THREAD_CHANNEL_ID = 'GAME_THREAD_CHANNEL_ID'

import discord
import asyncio

client = discord.Client()

async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = discord.Object(id=GAME_THREAD_CHANNEL_ID)
    while not client.is_closed:
        counter += 1
        await client.send_message(channel, counter)
        await asyncio.sleep(60) # task runs every 60 seconds

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.loop.create_task(my_background_task())
client.run(TOKEN)

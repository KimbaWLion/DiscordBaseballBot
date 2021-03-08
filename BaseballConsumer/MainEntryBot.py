#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main entry point for the bot.

This module performs the start-up, login and reads out the settings to configure
the bot.
"""
import json
import discord
from BaseballConsumerV2 import BaseballUpdaterBotV2

SETTINGS_FILE = './discordSettings.doNotUpload.json'

client = discord.Client()
# logging.basicConfig(level=logging.DEBUG)

def read_settings():
    error_msg = []
    with open(SETTINGS_FILE) as data:
        settings = json.load(data)

        global DISCORD_CLIENT_ID
        DISCORD_CLIENT_ID = settings.get('DISCORD_CLIENT_ID')
        if DISCORD_CLIENT_ID == None: error_msg.append("Missing DISCORD_CLIENT_ID")

        global DISCORD_CLIENT_SECRET
        DISCORD_CLIENT_SECRET = settings.get('DISCORD_CLIENT_SECRET')
        if DISCORD_CLIENT_SECRET == None: error_msg.append("Missing DISCORD_CLIENT_SECRET")

        global DISCORD_TOKEN
        DISCORD_TOKEN = settings.get('DISCORD_TOKEN')
        if DISCORD_TOKEN == None: error_msg.append("Missing DISCORD_TOKEN")

        global DISCORD_GAME_THREAD_CHANNEL_ID
        DISCORD_GAME_THREAD_CHANNEL_ID = settings.get('DISCORD_GAME_THREAD_CHANNEL_ID')
        if DISCORD_GAME_THREAD_CHANNEL_ID == None: error_msg.append("Missing DISCORD_GAME_THREAD_CHANNEL_ID")
    if error_msg:
        for error in error_msg: print(error)
        exit("Exiting due to missing setting")
    return 0

async def my_background_task():
    baseballUpdaterBotV2 = BaseballUpdaterBotV2()

    await client.wait_until_ready()
    counter = 0

    channel = client.get_channel(int(DISCORD_GAME_THREAD_CHANNEL_ID))
    while not client.is_closed():
        await baseballUpdaterBotV2.run(client, channel)
        # sleep exists in run() method


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

error_msg = read_settings()

client.loop.create_task(my_background_task())
client.run(DISCORD_TOKEN)

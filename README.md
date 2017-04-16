# DiscordBaseballBot
Posts baseball game updates to a discord channel

This is a working project to create a baseball updater bot to post game updates in a Discord channel.
This will rely heavily from the [reddit baseball updater bot](https://github.com/mattabullock/Baseball-GDT-Bot)
that posted to reddit threads. It will also rely on python discord bots that already exist.  

Please do not expect tests or regular updates, this is a pet project moreso as a proof of concept than 
anything well maintained.  If there is interest in it, I will expand it out to make it customizable
and easier to use for all major league teams.

# How it works
The bot queries http://gd2.mlb.com/components/game/mlb/ every 10 seconds and obtains all game events for the day in game_thread.now.  The bot compares the IDs from gd2.mlb.com with what it has already logged in game_thread.now.  If there is an ID which was not there before, the bot posts to discord and appends the game event to the game_thread.now log.

# How to use
1. [Create a discord bot and add it to your server](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
2. Edit DiscordPoster/settings.json to have the tokens/ids/team codes you desire
3. Create a file BaseballConsumer/logs/game_thread.now
4. run MainEntryBot.py

# Files
TBD

# Changelog
4-16-17
  The bot works!  Currently posts all game events, and when the game starts/ends
3-11-17
  Starting a new project, only a readme.  Goal #1 is to get this to post to a discord server of my choosing.

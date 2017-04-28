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
3. Create a blank file BaseballConsumer/logs/game_thread.now
4. run MainEntryBot.py

# Files
* DiscordPoster/\_\_init\_\_.py
  * Dunno if this is needed
* DiscordPoster/settings.json
  * The settings of the bot: The server ID, bot Token, and team code
* DiscordPoster/testPost.py
  * A file to test posting to Discord.  Scheduled for removal
* BaseballConsumer/\_\_init_\_\.py
  * Needed to be able to import other files in the directory I think...
* BaseballConsumer/MainEntryBot.py
  * Run this to run the bot.  Want to move it to the DiscordPoster directory, but need to be able to import BaseballConsumer.py.  I don't know how to import across directories in Python
* BaseballConsumer/BaseballConsumer.py
  * The controller for checking if there is a game event update.  It finds the URL for the game on gameday, then calls  	game_events_parser.py to parse the data from gd2.mlb.com.  If there is an update, it posts it to discord and logs the event.
* BaseballConsumer/game_events_parser.py
  * Parses the game events (atbats and actions) from gd2.mlb.com/.../game_events.json
* BaseballConsumer/linescore_parser.py
  * Parses the linescore (team name/runs/hits/errors) from gd2.mlb.com/.../linescore.json
* BaseballConsumer/timecheck.py
  * Not used, but supposed to be used to determine when a day ends to change the URL searched for.

# Changelog
* 4-27-17
  * Added bases status to the linescore
  * Fixed the "Game started" message since it was only tracking the Warm Up.  Now there's a "Game about to start" and "Game started" message
  * Make sure that the linescore and game event are in sync.  Checking this by checking if the batter is the same.  Probably could fail with a stolen base attempt or wild pitch.
  * Fixed team records in win/loss message
  * MIKE TROUT BOT - Turned the bot into Mike Trout Bot where the bot fawns over how wonderful Mike Trout
* 4-23-17
  * Added team records to the game ended embed
* 4-16-17
  * The bot works!  Currently posts all game events, and when the game starts/ends
* 3-11-17
  * Starting a new project, only a readme.  Goal #1 is to get this to post to a discord server of my choosing.

# Buglog
* 4-27-17
  * Managers' challenges break the bot (if they overturn the call) for some reason.  I put it in a try catch that ignores the exception in these cases.  No clue why it's failing.

# DiscordBaseballBot
Posts baseball game updates to a discord channel in near real time

![Image of game updates](https://i.imgur.com/or2syfZ.png)

Image of game updates with K-tracker
![Image of strikeout updates with flair](http://i.imgur.com/uXE0i5d.png)

Image of RBI emoji and end of the game
![Image of RBI emoji and end of the game](https://i.imgur.com/1asf2Gg.png)


This is a working project to create a baseball updater bot to post game updates in a Discord channel.

V2 leverages https://pypi.org/project/MLB-StatsAPI/ for getting near real time updates of MLB games, it also relies on
python discord bots that already exist.

Please do not expect tests or regular updates, this is a pet project moreso as a proof of concept than 
anything well maintained.  If there is interest in it, I will expand it out to make it customizable
and easier to use for all major league teams.

# How it works
The bot queries https://pypi.org/project/MLB-StatsAPI/ every 10 seconds to get game event and stat information.
The bot compares the IDs for each new event with what it has already logged in game_thread.now.
If there is an ID which was not there before, the bot posts to discord and appends the game event to the game_thread.now log.

# How to use
1. [Create a discord bot and add it to your server](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
2. Put the token information in the file discordSettings.doNotUpload.json
2. Edit settings.json to have the TEAM_ID that you desire (Lookup the TEAM_ID values for your preferred team in the table below).
3. Create a blank file BaseballConsumer/logs/game_thread.now
4. Make sure to download discord.py (v0.16.17), aiohttp.py (v1.0.5), asyncio.py, MLB-StatsAPI (v0.1.8) packages
5. Make sure you are running a python interpretter version 3.6.  If you're running not (3.5- or 3.7+),
 [asyncio will not work](https://stackoverflow.com/questions/43948454/python-invalid-syntax-with-async-def).
  (If you are running on a mac and python 3.6, you need to install the certificates.
  Follow the instructions [here](https://github.com/Rapptz/discord.py/issues/423))
6. run MainEntryBot.py

# Team code and abbreviation table
|     TEAM     | TEAM_ID |
| ------------ |:---------:|
| Arizona Diamondbacks     |    109    |
| Atlanta Braves           |    144    |
| Baltimore Orioles        |    110    |
| Boston Red Sox           |    111    |
| Chicago White Sox        |    145    |
| Chicago Cubs             |    112    |
| Cincinnati Reds          |    113    |
| Cleveland Indians        |    114    |
| Colorado Rockies         |    115    |
| Detroit Tigers           |    116    |
| Houston Astros           |    117    |
| Kansas City Royals       |    118    |
| Los Angeles Angels       |    108    |
| Los Angeles Dodgers      |    119    |
| Miami Marlins            |    146    |
| Milwaukee Brewers        |    158    |
| Minnesota Twins          |    142    |
| New York Yankees         |    147    |
| New York Mets            |    121    |
| Oakland Athletics        |    133    |
| Philadelphia Phillies    |    143    |
| Pittsburgh Pirates       |    134    |
| San Diego Padres         |    135    |
| San Francisco Giants     |    137    |
| Seattle Mariners         |    136    |
| St. Louis Cardinals      |    138    |
| Tampa Bay Rays           |    139    |
| Texas Rangers            |    140    |
| Toronto Blue Jays        |    141    |
| Washington Nationals     |    120    |

# Files
* settings.json
  * The settings of the bot: The server ID, bot Token, team code, and more
* BaseballConsumer/\_\_init_\_\.py
  * Needed to be able to import other files in the directory I think...
* BaseballConsumer/MainEntryBot.py
  * Run this to run the bot.  Want to move it to the DiscordPoster directory, but need to be able to import BaseballConsumer.py.  I don't know how to import across directories in Python
* BaseballConsumer/BaseballConsumerConstants.py
  * Contains configurable constants like emoji or game status updates or 7th inning stretch

# FAQ
* How come when I play the bot for a previous game, it doesn't post things such as wild pitches or pitching changes?
  * Limitation of the API.  Wild pitches, Substitutions, and some other events don't have their own event item in the response from the API,
   as such, they will not show up in a replay of events form the game

# Changelog
* 3-11-21
  * Strikeout Tracker is back baby!
  * RBI and Homerun tracker is back as well!
* 3-10-21
  * Added "No Game Today" as a possible game status
* 3-7-21
  * Game statuses now get posted
* 3-6-21
  * Bot is now updated to version 2.0, using new MLB stats API
  * Updated README to be correct
* 5-15-19
  * Bot now states that it is catching up if it is behind in the game
  * Fixed Grand slam emotes
  * Code is now more robust so it will not break if there is a null value for any higher level object
  * Doesn't post if there is no description anymore
* 4-4-19
  * Unearned runs now have their own emoji if there are no RBIs during the play
  * Turned globalLinescoreStatus into a dictionary
  * Fixed a couple of errors that sometimes crash the bot
* 3-6-19
  * Bot now calls mlb.com asynchonously
* 4-28-18
  * We now use BeautifulSoup to parse the HTML, fixing an html parsing bug
  * Fixed the infinite loop on offdays bug, allowing the bot to continue posting through a long period of time
  * Fixed the bug for only certain teams where the bot would fail due to other directories containing the team's TEAM_CODE
* 3-26-18
  * The bot now changes the date automatically so it doesn't need to be run every day
  * The HTML from mlb.com is now split by ' ' instead of '\n'.  This is a temporary fix to get the URL I need for the games.  I should still use beautiful soup for this in a future fix
  * Personnel changes are easier to read because it won't display the linescore
* 3-8-18
  * Put all the constants for BaseballConsumer at the top of the file
  * Changed MikeTroutisms to PlayerQuips
  * Removed player nicknames (will put this in again player weekend)
  * Fixed the newly broken runnerOnBaseStatus by adding the new runnerOnBase attributes
  * Adding an opponents strike tracker now
  * Added more baseStatusChanging events
  * Added more game statuses 
* 8-26-17
  * Turned emotes into constants to make it easier to change them
  * Use player nicknames for players weekend
  * Opponent batting RBIs now post an emote
  * Base changing status actions now correctly change the base status
* 7-10-17
  * Changed Mike Trout bot into Chase Utley bot
  * Grand slam salami emoji
  * pregame probable pitchers
  * RBI emoji
  * fixed beginning of inning bug
* 5-21-17
  * Making sure stolen bases wait for the linescore to update before publishing them 
* 5-15-17
  * Now posts a divider at the end of innings
  * Added K-tracker for the favorite team (using Mets flairs for the time being)
  * Bug fix on when favorite team is batting
  * bug fix on when game actions post before the the atbats that happen before them
  * bug fix on when favoirte team is winning
  * bug fix actions repeating when their linescore info changes (for unknown reasons on mlb.com)
* 5-8-17
  * Fixed race condition of game actions happening before atbats when the linescore's "batterId" doesn't update quickly.  Since game events do not wait for the batterId to change, they update before the atbat does
  * Combined the gameStatusChecker into a single function
  * Made it more configurable with "FavoriteTeam" functions rather that hardcoding Mets values
  * Added spots to add emoji
  * Reverted Mike Trout bot
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
* 3-12-18
  * Stolen bases/pickoffs/caugh stealing/wild pitch aren't their own event, so if the bot is behind (even by 1 play), it doesn't do the stolen base

# Future Features

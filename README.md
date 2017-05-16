# DiscordBaseballBot
Posts baseball game updates to a discord channel

![Image of game updates](http://i.imgur.com/xLfqaUW.png)

Image of game updates with flair
![Image of strikeout updates with flair](http://i.imgur.com/zhKYNmH.png)

This is a working project to create a baseball updater bot to post game updates in a Discord channel.
This will rely heavily from the [reddit baseball updater bot](https://github.com/mattabullock/Baseball-GDT-Bot)
that posted to reddit threads. It will also rely on python discord bots that already exist.  

Please do not expect tests or regular updates, this is a pet project moreso as a proof of concept than 
anything well maintained.  If there is interest in it, I will expand it out to make it customizable
and easier to use for all major league teams.

# How it works
The bot queries http://gd2.mlb.com/components/game/mlb/ every 10 seconds to get game event and stat information.  The bot compares the IDs from gd2.mlb.com with what it has already logged in game_thread.now.  If there is an ID which was not there before, the bot posts to discord and appends the game event to the game_thread.now log.

# How to use
1. [Create a discord bot and add it to your server](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
2. Edit settings.json to have the tokens/ids/team codes you desire (Lookup the TEAM_ABBREV and TEAM_CODE values for your preferred team in the table below)
3. Create a blank file BaseballConsumer/logs/game_thread.now
4. in BaseballConsumer/BaseballConsumer.py, change line 27 to the path of the game_thread.now file.  (i.e. 'C:\Users...\game_thread.now')
5. Make sure to download discord.py, aiohttp.py, asyncio.py packages
4. run MainEntryBot.py the day of the game
5. When game is finished, wait until the next day and run MainEntryBot.py again

# Team code and abbreviation table
|     TEAM     | TEAM_ABBREV | TEAM_CODE |
| ------------ |:-----------:|:---------:|
| Diamondbacks |     ARI     |    ari    |
| Braves       |     ATL     |    atl    |
| Orioles      |     BAL     |    bal    |
| Red Sox      |     BOS     |    bos    |
| White Sox    |     CWS     |    cha    |
| Cubs         |     CHC     |    chn    |
| Reds         |     CIN     |    cin    |
| Indians      |     CLE     |    cle    |
| Rockies      |     COL     |    col    |
| Tigers       |     DET     |    det    |
| Astros       |     HOU     |    hou    |
| Royals       |     KC      |    kca    |
| Angels       |     LAA     |    ana    |
| Dodgers      |     LAD     |    lan    |
| Marlins      |     MIA     |    mia    |
| Brewers      |     MIL     |    mil    |
| Twins        |     MIN     |    min    |
| Yankees      |     NYY     |    nya    |
| Mets         |     NYM     |    nyn    |
| Athletics    |     OAK     |    oak    |
| Phillies     |     PHI     |    phi    |
| Pirates      |     PIT     |    pit    |
| Padres       |     SD      |    sdn    |
| Giants       |     SF      |    sfn    |
| Mariners     |     SEA     |    sea    |
| Cardinals    |     STL     |    sln    |
| Rays         |     TB      |    tba    |
| Rangers      |     TEX     |    tex    |
| Blue Jays    |     TOR     |    tor    |
| Nationals    |     WSH     |    was    |

# Files
* DiscordPoster/\_\_init\_\_.py
  * Dunno if this is needed
* settings.json
  * The settings of the bot: The server ID, bot Token, team code, and more
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
* 5-8-17
  * ~~There are race conditions when there game actions (not atbats).  In order to make sure the linescore was accurate, I do not have the bot post the next atbat until the currentBatterId in both linescore.json and game_events.json match.  However, if there is a game event, it doesn't mention currentBatterId and as such posts immediately.  So sometimes there is "Coaching visit to the mound" followed by "grand slam" rather than the other way around. Another race condition, if there is a stolen base, it the linescore often does not reflect the stolen base in update.~~  
    * 5-8-17 - This should be fixed now with the globalLinescoreStatus update
* 4-27-17
  * Managers' challenges break the bot (if they overturn the call) for some reason.  I put it in a try catch that ignores the exception in these cases.  No clue why it's failing.

# Future Features
* ~~Fix race conditions~~
  * 5-8-17 - Completed
* Leverage Mike Trout revision to be able to post uniquely for every player. (i.e. post Thor's hammer whenever Syndergaard gets a hit)
* Allow the bot to change over the date itself so that you can leave it running instead of needing to restart it every day

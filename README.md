# DiscordBaseballBot
Posts baseball game updates to a discord channel

![Image of game updates](https://i.imgur.com/or2syfZ.png)

Image of game updates with K-tracker
![Image of strikeout updates with flair](http://i.imgur.com/uXE0i5d.png)

Image of RBI emoji and end of the game
![Image of RBI emoji and end of the game](https://i.imgur.com/1asf2Gg.png)


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
2. Edit settings.json to have the tokens/ids/team codes you desire (Lookup the TEAM_ABBREV and TEAM_CODE values for your preferred team in the table below).
3. Create a blank file BaseballConsumer/logs/game_thread.now
4. Make sure to download discord.py (v0.16.17), aiohttp.py (v1.0.5), asyncio.py, beautifulsoup4 (v4.6.0) packages
5. Make sure you are running a python interpretter version 3.6.  If you're running not (3.5- or 3.7+), [asyncio will not work](https://stackoverflow.com/questions/43948454/python-invalid-syntax-with-async-def).  (If you are running on a mac and python 3.6, you need to install the certificates.  Follow the instructions [here](https://github.com/Rapptz/discord.py/issues/423))
6. run MainEntryBot.py the day of the game
7. When game is finished, wait until the next day and run MainEntryBot.py again

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
* 4-28-18
  * ~~Infinite loop on offdays.  The bot doesn't search for new URLs after offdays, making the bot get stuck in an infinite loop and not search for the next days' games.~~
    * 4-28-18 - fixed, added a break out based on the current date
  * ~~TEAM_CODE exists in more than one directory on the index page.  'pit' (TEAM_CODE for pittsburgh) exists int he directory 'pitchers', breaking the bot.~~
    * 4-28-18 - fixed, now the bot searches for TEAM_CODE+'mlb', not just the TEAM_CODE, fixing this issue
  * ~~After the 3rd out of an inning, the bot lags behind for the rest of the game.~~
    * 4-28-18 - The global linescore status was not being initialized correctly at the end of an inning because of the new runnerOnBaseStatus fields that I added.  I added in more initializations and now it works fine :)
* 3-8-18
  * ~~MLB.com changed how they use `runner_on_base_status` in the linescore.  Before it used to be a number 0-7 that said whether there were men on the bases, where 1 meant man on first, 3 meant man on third, 4 meant men on first and second, and 7 mean bases loaded.  Now there are attributes `runner_on_1b`, `runner_on_2b`, and `runner_on_3b`, which lists which player_id is on each bag.~~
    * I fixed this by calling tracking runner_on_1b instead of runner_on_base_status
  * ~~The urls are not splitting anymore by '\n'.  I have no clue why, but it's messing with actually finding the URLs of the game, and splitting by a single space (' ') doesn't seem to be working.~~  
    * ~~I should use beautiful soup to parse out the HTML~~
    * 4-28-18 - I used BeautifulSoup to parse it out and it works :)
* 8-26-17
  * ~~If a game event happens but there is no RBI, bot does not post an emoji about a run scored.  An example of this is if a wild pitch scores a runner.  The gameEvents JSON has "score: T", and I should try to find a way to use that to post when there are runs scored, not just when there are RBIs~~
    * 4-04-19 - fixed, now there are new emoji's for non-RBI runs
* 5-8-17
  * ~~There are race conditions when there game actions (not atbats).  In order to make sure the linescore was accurate, I do not have the bot post the next atbat until the currentBatterId in both linescore.json and game_events.json match.  However, if there is a game event, it doesn't mention currentBatterId and as such posts immediately.  So sometimes there is "Coaching visit to the mound" followed by "grand slam" rather than the other way around. Another race condition, if there is a stolen base, it the linescore often does not reflect the stolen base in update.~~  
    * ~~5-8-17 - This should be fixed now with the globalLinescoreStatus update~~
    * ~~5-21-17 - linescore still is sometimes out of sync, but mostly okay~~
    * This is fixed :)
* 4-27-17
  * Managers' challenges break the bot (if they overturn the call) for some reason.  I put it in a try catch that ignores the exception in these cases.  No clue why it's failing.

# Future Features
* ~~Fix race conditions~~
  * 5-8-17 - Completed
* Leverage Mike Trout revision to be able to post uniquely for every player. (i.e. post Thor's hammer whenever Syndergaard gets a hit)
* ~~Allow the bot to change over the date itself so that you can leave it running instead of needing to restart it every day~~
  * 3-26-18 - Completed
* Add in emoji for Stolen bases
* ~~Add in shruggy emoji for runs scored but not an RBI for favorite team~~
  * 4-04-19 - Completed
* Add in no-hitter/perfect game celebrations
* ~~Do not show the linescore or onBaseStatus when the bot lags behinds and is catching up (since they are 100% out of sync)~~
  * 4-04-19 - Completed
* Add emoji or bot comment for ejections
* Add delayed start as a game status
* ~~When catching up from previous innings, do not show linescore/onBaseStatus~~
  * 4-04-19 - Completed
* Fix the debugger to be more descriptive
* If mlb.com services are down, instead of crashing the bot, be able to handle "endpoint request timed out"

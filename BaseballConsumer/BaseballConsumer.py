
'''

BASEBALL GAME THREAD BOT

Originally written by:
/u/DetectiveWoofles
/u/avery_crudeman

Editted for Discord by KimbaWLion

Please contact us on Reddit or Github if you have any questions.

'''

from datetime import datetime ,timedelta
from game_events_parser import GameEventsParser
from linescore_parser import LinescoreParser
import time
import json
import logging
import aiohttp
import discord
import random
import asyncio

GAME_THREAD_LOG = r'<Path to game_thread.now>'
SETTINGS_FILE = '../settings.json'

class BaseballUpdaterBot:

    def __init__(self):
        self.BOT_TIME_ZONE = None
        self.TEAM_TIME_ZONE = None
        self.TEAM_CODE = None

    def read_settings(self):
        with open(SETTINGS_FILE) as data:
            settings = json.load(data)

            self.DISCORD_CLIENT_ID = settings.get('DISCORD_CLIENT_ID')
            if self.DISCORD_CLIENT_ID == None: return "Missing DISCORD_CLIENT_ID"

            self.DISCORD_CLIENT_SECRET = settings.get('DISCORD_CLIENT_SECRET')
            if self.DISCORD_CLIENT_SECRET == None: return "Missing DISCORD_CLIENT_SECRET"

            self.DISCORD_TOKEN = settings.get('DISCORD_TOKEN')
            if self.DISCORD_TOKEN == None: return "Missing DISCORD_TOKEN"

            self.DISCORD_GAME_THREAD_CHANNEL_ID = settings.get('DISCORD_GAME_THREAD_CHANNEL_ID')
            if self.DISCORD_GAME_THREAD_CHANNEL_ID == None: return "Missing DISCORD_GAME_THREAD_CHANNEL_ID"

            self.BOT_TIME_ZONE = settings.get('BOT_TIME_ZONE')
            if self.BOT_TIME_ZONE == None: return "Missing BOT_TIME_ZONE"

            self.TEAM_TIME_ZONE = settings.get('TEAM_TIME_ZONE')
            if self.TEAM_TIME_ZONE == None: return "Missing TEAM_TIME_ZONE"

            self.TEAM_CODE = settings.get('TEAM_CODE')
            if self.TEAM_CODE == None: return "Missing TEAM_CODE"

            self.TEAM_ABBREV = settings.get('TEAM_ABBREV')
            if self.TEAM_ABBREV == None: return "Missing TEAM_ABBREV"

        return 0

    def getTime(self):
        today = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        return today

    def formatAtBatLineForLog(self, atbat):
        return "{} {} | B:{} S:{} O:{}; Result: {}; Description: {}".format(
            atbat['topOrBot'], atbat['inning'], atbat['balls'], atbat['strikes'],
            atbat['outs'] ,atbat['result'], atbat['description'])

    def hasMikeTrout(self, gameEvent):
        if "Mike Trout" in gameEvent['description']: return True
        return False

    def formatMikeTroutisms(self, description):
        if "Mike Trout" in description:
            mikeTroutism = [
                "Isn't Mike Trout just like, the cutest?",
                "<3 Mike Trout <3",
                "OMG, did you see Mike run?  He's like, so fast!",
                "I could lay down and listen to Mike tell me the weather for hours...",
                "Fuck, Marry, Kill.  Mike Trout, Mike Trout, and not Mike Trout.  Go",
                "I'd swim upstream to spawn with Mike Trout.",
                ":) Trout-y :)",
                "Seeing Mike Trout play makes me feel everything is right with the world.",
                "No one hits like Mike Trout, matches wits like Mike Trout, in a spitting match nobody spits like Mike Trout...",
                "It's a bird!  It's a plane!  No, it's Mike Trout!",
                "I just wanna hug Mike Trout, he looks so squishy.",
                "9 out of 10 destists recommend Mike Trout.",
                "Mike Trout allows children to eat ice cream for breakfast.",
                "Mike Trout's like my favorite player ever.",
                "Gimme a M-I-K-E!  Gimme a T-R-O-U-T!  What does that spell?!?!?",
                "Mike Trout always tips his taxi drivers",
                "Mike Trout 2020!",
                "Mike Trout always did his chores and made his bed before playing video games as a kid.",
                "Did you know that tuortekim is Mike Trout backwards?",
                "Robbing homeruns and catches at his shoestrings,\nScoring RBIs guaranteed with one swing,\nNot being injured from shoddy hamstrings,\nMike Trout does a few of my favorite things."
            ]
            return random.choice(mikeTroutism)
        return ""


    def formatGameEventForDiscord(self, gameEvent, linescore):
        # return "|!{}|testNYM|!{}|testHits|testErrors|  \n  |!{} Outs |testPHI|!{}|testHits|testErrors|\n \n" \
        #        "Last Play:  On a !{}-!{} count, !{} \n \n !{} Use atbat[result] to play around with the result." \
        #        "If it's a Mets pitcher strikeout, post KKKKK.  If it's a Mets home run, praise Kevin Long. Animal facts, etc...".format(
        #     atbat['topOrBot'] ,atbat['awayTeamRuns'] ,atbat['outs'] ,atbat['homeTeamRuns'] ,atbat['balls'],
        #     atbat['strikes'], atbat['description'],"ExtraSpaceAddingThisIn")
        #     #,self.differentFlairsForDifferentResults(atbat['topOrBot'] ,atbat['result']))
        #
        return "```" \
               "{}\n" \
               "{}{}" \
               "```\n" \
               "{}".format(self.formatLinescoreForDiscord(gameEvent, linescore),
                           self.formatPitchCount(gameEvent['gameEvent'], gameEvent['balls'], gameEvent['strikes']),
                           gameEvent['description'],
                           self.playerismsAndEmoji(gameEvent, linescore))

    def formatLinescoreForDiscord(self, atbat, linescore):
        return "{} {:>2}   ┌───┬──┬──┬──┐\n" \
               "   {}     |{:<3}│{:>2}│{:>2}│{:>2}│\n" \
               "  {} {}    ├───┼──┼──┼──┤\n" \
               "{}   │{:<3}│{:>2}│{:>2}│{:>2}│\n" \
               "         └───┴──┴──┴──┘".format(
            atbat['topOrBot'], atbat['inning'],
            self.formatSecondBase(linescore['status']['runnerOnBaseStatus']),
            linescore['away_team_name']['team_abbrev'], linescore['away_team_stats']['team_runs'],
            linescore['away_team_stats']['team_hits'], linescore['away_team_stats']['team_errors'],
            self.formatThirdBase(linescore['status']['runnerOnBaseStatus']), self.formatFirstBase(linescore['status']['runnerOnBaseStatus']),
            self.formatOuts(atbat['outs']),
            linescore['home_team_name']['team_abbrev'], linescore['home_team_stats']['team_runs'],
            linescore['home_team_stats']['team_hits'], linescore['home_team_stats']['team_errors']
        )

    def formatOuts(self, outs):
        outOrOuts = " Outs"
        if outs is "1": outOrOuts = "  Out"
        return "".join([outs, outOrOuts])

    def formatSecondBase(self, runnerOnBaseStatus):
        return self.formatBase(runnerOnBaseStatus in ("2", "4", "6", "7"))

    def formatThirdBase(self, runnerOnBaseStatus):
        return self.formatBase(runnerOnBaseStatus in ("3", "5", "6", "7"))

    def formatFirstBase(self, runnerOnBaseStatus):
        return self.formatBase(runnerOnBaseStatus in ("1", "4", "5", "7"))

    def formatBase(self, baseOccupied):
        if baseOccupied:
            return "●"
        return "○"

    def formatPitchCount(self, gameEvent, balls, strikes):
        if gameEvent is 'atbat': return "On a {}-{} count, ".format(balls, strikes)
        elif gameEvent is 'action': return ""
        raise Exception("gameEvent not recognized")

    def playerismsAndEmoji(self, gameEvent, linescore):
        event = gameEvent['event']
        if self.favoriteTeamIsBatting(gameEvent, linescore):
            if "Home Run" in event:
                return "<:ITSOUTTAHERE:257607350133719040>"
        else:
            if "Strikeout" in event:
                if "strikes out" in gameEvent['description']:
                    return "<:Strikeout:257620664209506304>"
                if "called out on strike" in gameEvent['description']:
                    return "<:Strikeout2:257620669527883777>"
        return ""


    def favoriteTeamIsBatting(self, gameEvent, linescore):
        return self.favoriteTeamIsHomeTeam(linescore) and gameEvent['topOrBot'] == "BOT"

    def getEventIdsFromLog(self):
        idsFromLog = []
        with open(GAME_THREAD_LOG) as log:
            for line in log:
                splitLine = line.split(" ")
                id = splitLine[2][1:-1]
                idsFromLog.append(id)
        log.close()
        return idsFromLog

    def printToLog(self, atbat):
        with open(GAME_THREAD_LOG, "a") as log:
            id = atbat['id'] if atbat['id'] is not None else "NoIdInJSONFile"
            log.write("[{}] [{}] | {}\n".format(self.getTime(), id, self.formatAtBatLineForLog(atbat)))
        log.close()
        print("[{}] New atBat: {}".format(self.getTime(), self.formatAtBatLineForLog(atbat)))

    def printGameStatusToLog(self, id, gameStatus):
        with open(GAME_THREAD_LOG, "a") as log:
            log.write("[{}] [{}] | Game Status: {}\n".format(self.getTime(), id, gameStatus))
        log.close()
        print("[{}] Game Status: {}".format(self.getTime(), gameStatus))

    def commentOnDiscord(self, gameEvent, linescore):
        comment = self.formatGameEventForDiscord(gameEvent, linescore)
        return comment

    async def run(self, client, channel):
        error_msg = self.read_settings()
        if error_msg != 0:
            print(error_msg)
            return

        # timechecker = timecheck.TimeCheck(time_before)
        gameEventsParser = GameEventsParser()
        linescoreParser = LinescoreParser()

        # This list will be what is compared against to see if anything new popped up in the game_events feed
        idsOfPrevEvents = self.getEventIdsFromLog()

        # initialize the globalLinescoreStatus variable
        global globalLinescoreStatus
        globalLinescoreStatus = None

        response = None
        directories = []
        while True:
            todaysGame = datetime.now() - timedelta(hours = 5)

            # if response.time is not todaysGame, response = None, directories = []

            url = "http://gd2.mlb.com/components/game/mlb/"
            url = url + "year_" + todaysGame.strftime("%Y") + "/month_" + todaysGame.strftime \
                ("%m") + "/day_" + todaysGame.strftime("%d") + "/"

            while not response:
                print("[{}] Searching for day's URL...".format(self.getTime()))
                try:
                    # If it returns a 404, try again
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as resp:
                            if resp.status == 200:
                                print("[{}] Found day's URL: {}".format(self.getTime(), url))
                                response = await resp.text()

                                html = response.split('\n')

                                # Get the gid directory based on team code (NYM is nyn)
                                for v in html:
                                    if self.TEAM_CODE in v:
                                        v = v[v.index("\"") + 1:len(v)]
                                        v = v[0:v.index("\"")]
                                        directories.append(url + v)
                                        print("[{}] Found game directory for team {}: {}".format(self.getTime(),
                                                                                                 self.TEAM_CODE,
                                                                                                 directories))
                except:
                    print("[{}] Couldn't find URL \"{}\", trying again...".format(self.getTime(), url))
                    time.sleep(20)

            try:
                for d in directories:

                    # Comment out this line to hard code a directory
                    #d = "http://gd2.mlb.com/components/game/mlb/year_2017/month_04/day_26/gid_2017_04_26_oakmlb_anamlb_1/"
                    print("[{}] Searching the URL directory for updates : {}".format(self.getTime(), d))

                    linescore_url = "".join([d ,"linescore.json"])
                    #print("[{}] Searching the linescore URL for updates: {}".format(self.getTime(), linescore_url))
                    if not await linescoreParser.doesJSONExistYet(linescore_url):
                        print("[{}] Game has not started".format(self.getTime()))
                        continue
                    linescoreJSON = await linescoreParser.getJSONFromURL(linescore_url)
                    linescore = linescoreParser.parseGameDataIntoMap(linescoreJSON)

                    game_events_url = "".join([d ,"game_events.json"])
                    #print("[{}] Searching the game URL for updates: {}".format(self.getTime(), game_events_url))
                    if not await gameEventsParser.doesJSONExistYet(game_events_url):
                        print("[{}] Game has not started".format(self.getTime()))
                        continue
                    gameEventsJSON = await gameEventsParser.getJSONFromURL(game_events_url)
                    if not gameEventsParser.gameHasStarted(gameEventsParser.getInnings(gameEventsJSON)):
                        print("[{}] Game has not started yet".format(self.getTime()))
                        continue
                    listOfGameEvents = gameEventsParser.getListOfGameEvents(gameEventsParser.getInnings(gameEventsJSON))

                    # Check if new game event
                    for gameEvent in listOfGameEvents:
                        id = (gameEvent['id'] if gameEvent['id'] is not None else "NoIdInJSONFile")
                        if id == "NoIdInJSONFile": print("A game event ID is None, figure out why") # to help debug
                        if id not in idsOfPrevEvents and self.linescoreAndGameEventsInSync(linescore, gameEvent):# and self.hasMikeTrout(gameEvent):
                            self.updateGlobalLinescoreStatus(linescore)
                            self.printToLog(gameEvent)
                            await client.send_message(channel, self.commentOnDiscord(gameEvent, linescore))
                            idsOfPrevEvents = self.getEventIdsFromLog()

                    # Check if game status changed
                    gameStatusTuple = self.checkGameStatus(linescore, idsOfPrevEvents)
                    if gameStatusTuple is not None:
                        await client.send_message(channel, embed=gameStatusTuple[0])
                        await client.send_message(channel, gameStatusTuple[1])

                    # Refresh the eventIds
                    idsOfPrevEvents = self.getEventIdsFromLog()
            except Exception as ex:
                logging.exception("Exception occured")
                await client.send_message(channel, "Bot encountered an error.  Was there a review on the field?")

            time.sleep(10)

        print("/*------------- End of Bot.run() -------------*/")

    def linescoreAndGameEventsInSync(self, linescore, gameEvent):
        if linescore['currentPlayers'] is None:
            return True
        if (gameEvent['batterId'] != linescore['currentPlayers']['batter']['id']):
            return True
        if self.linescoreStatusHasChanged(linescore):
            return True
        return False

    def linescoreStatusHasChanged(self, linescore):
        global globalLinescoreStatus
        newLinescoreStatus = self.getLinescoreStatus(linescore)
        if globalLinescoreStatus != newLinescoreStatus:
            globalLinescoreStatus = newLinescoreStatus
            return True
        return False

    def getLinescoreStatus(self, linescore):
        # Outs, Base status, Home runs, Home hits, Home errors, Away run, Away hits, Away errors
        return (linescore['status']['outs'], linescore['status']['runnerOnBaseStatus'],
                linescore['home_team_stats']['team_runs'], linescore['home_team_stats']['team_hits'], linescore['home_team_stats']['team_errors'],
                linescore['away_team_stats']['team_runs'], linescore['away_team_stats']['team_hits'], linescore['away_team_stats']['team_errors'])

    def updateGlobalLinescoreStatus(self, linescore):
        newLinescoreStatus = self.getLinescoreStatus(linescore)
        global globalLinescoreStatus
        globalLinescoreStatus = newLinescoreStatus

    def checkGameStatus(self, linescore, idsOfPrevEvents):
        id = linescore['status']['game_status_id']
        gameStatus = linescore['status']['game_status']
        if (gameStatus == "Warmup") and (id not in idsOfPrevEvents):
            self.printGameStatusToLog(id, gameStatus)
            em = self.warmupStatus()
            return em
        if (gameStatus == "In Progress") and (id not in idsOfPrevEvents):
            self.printGameStatusToLog(id, gameStatus)
            em = self.gameStartedStatus()
            return em
        if (gameStatus == "Postponed") and (id not in idsOfPrevEvents):
            self.printGameStatusToLog(id, gameStatus)
            em = (discord.Embed(title='Game is postponed', description='To be made up later'), "Rain delay stats?")
            return em
        if (gameStatus == "Game Over") and (id not in idsOfPrevEvents):
            self.printGameStatusToLog(id, gameStatus)
            em = self.gameEndedStatus(linescore)
            return em
        return None

    def warmupStatus(self):
        return (discord.Embed(title='Game\'s about to start, everyone get in here!', description='HYPE HYPE HYPE HYPE.'),
                "<:Raccoon:257616622599143424> <:Parakeet:257615994569228300>")

    def gameStartedStatus(self):
        return (discord.Embed(title='Play ball!', description='Mets game has started.'), "<:Flamingo:257617918395809792>")

    def checkIfRainDelay(self):
        pass

    def gameEndedStatus(self, linescore):
        favoriteTeamWLRecord = self.getFavoriteTeamWLRecord(linescore)
        otherTeamWLRecord = self.getOtherTeamWLRecord(linescore)
        if self.isFavoriteTeamWinning(linescore):
            # TCB url 'https://www.youtube.com/watch?v=mmwic9kFx2c'
            title = 'Put it in the books!'
            description = '{} ({}-{}) beat the {} ({}-{}) by a score of {}-{}!'.format(
                favoriteTeamWLRecord[0], favoriteTeamWLRecord[1], favoriteTeamWLRecord[2],
                otherTeamWLRecord[0], otherTeamWLRecord[1], otherTeamWLRecord[2],
                linescore['away_team_stats']['team_runs'], linescore['home_team_stats']['team_runs']
            )
            em = (discord.Embed(title=title, description=description),
                  'https://www.youtube.com/watch?v=mmwic9kFx2c')
        else:
            title = 'Mets defeated'
            description = '{} ({}-{}) were defeated by the {} ({}-{}) by a score of {}-{}'.format(
                favoriteTeamWLRecord[0], favoriteTeamWLRecord[1], favoriteTeamWLRecord[2],
                otherTeamWLRecord[0], otherTeamWLRecord[1], otherTeamWLRecord[2],
                linescore['away_team_stats']['team_runs'], linescore['home_team_stats']['team_runs']
            )
            em = (discord.Embed(title=title, description=description),
                  'Better luck next time!')
        return em

    def isFavoriteTeamWinning(self, linescore):
        homeTeamRuns = linescore['home_team_stats']['team_runs']
        awayTeamRuns = linescore['away_team_stats']['team_runs']
        favoriteTeamIsHomeTeam = self.favoriteTeamIsHomeTeam(linescore)
        return (favoriteTeamIsHomeTeam and (homeTeamRuns > awayTeamRuns)) or \
               (not favoriteTeamIsHomeTeam and (homeTeamRuns < awayTeamRuns))

    def getFavoriteTeamWLRecord(self, linescore):
        return self.getWLRecord(linescore, self.favoriteTeamIsHomeTeam(linescore))

    def getOtherTeamWLRecord(self, linescore):
        return self.getWLRecord(linescore, not self.favoriteTeamIsHomeTeam(linescore))

    def getWLRecord(self, linescore, homeOrAway):
        if homeOrAway:
            return (linescore['home_team_name']['team_name'],
                    linescore['home_team_record']['team_wins'], linescore['home_team_record']['team_losses'])
        else:
            return (linescore['away_team_name']['team_name'],
                    linescore['away_team_record']['team_wins'], linescore['away_team_record']['team_losses'])

    def favoriteTeamIsHomeTeam(self, linescore):
        return linescore['home_team_name']['team_abbrev'] == self.TEAM_ABBREV

if __name__ == '__main__':
    baseballUpdaterBot = BaseballUpdaterBot()
    baseballUpdaterBot.run()

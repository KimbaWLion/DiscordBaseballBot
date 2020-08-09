'''
@DEPRECATED
'''
'''

BASEBALL GAME THREAD BOT

Originally written by:
/u/DetectiveWoofles
/u/avery_crudeman

Editted for Discord by KimbaWLion

Please contact us on Reddit or Github if you have any questions.

'''

from datetime import datetime, timedelta
from game_events_parser import GameEventsParser
from linescore_parser import LinescoreParser
import asyncio
import json
import logging
import aiohttp
import discord
import random
import bs4

SETTINGS_FILE = './settings.json'

# Emotes
EMOTE_STRIKEOUT = "<:strikeout:345303176704032770>"
EMOTE_STRIKEOUT_LOOKING = "<:strikeout2:345303176792113152>"
EMOTE_RBI = "<:ribbies:345468637617848321>"
EMOTE_EARNED_RUN = "<:nymLogo:419221359357460480>"
EMOTE_UNEARNED_RUN: "¯\_(ツ)_/¯"
EMOTE_HOMERUN = "<:ITSOUTTAHERE:345303176955822080>"
EMOTE_GRAND_SLAM = "<:salami:345303176636792832>"
EMOTE_OTHER_TEAM_RBI = ":("
EMOTE_OTHER_TEAM_EARNED_RUN = "<:tired_face:562192847575580692>"
EMOTE_OTHER_TEAM_UNEARNED_RUN = "<:rage:562189976343805963>"
EMOTE_OTHER_TEAM_STRIKEOUT = "K"
EMOTE_OTHER_TEAM_STRIKEOUT_LOOKING = "ꓘ"
EMOTE_STOLEN_BASE = "<:stolen:432072292013572097>"

# Game Status Constants
WARMUP_TITLE = 'Game\'s about to start, everyone get in here!'
WARMUP_DESCRIPTION = "Let's go win this one!" # Meet the Mets, meet the Mets.  Step right up and greet the Mets...
WARMUP_BODY_ALTERNATIVE = "https://www.youtube.com/watch?v=6GsCmnZnllk" # MTM https://www.youtube.com/watch?v=6GsCmnZnllk

GAMESTARTED_TITLE = 'Play ball!'
GAMESTARTED_DESCRIPTION = 'HYPE HYPE HYPE HYPE HYPE HYPE HYPE'
GAMESTARTED_BODY = "Let's go Mets!"

RAINDELAY_TITLE = 'Rain Delay'
RAINDELAY_DESCRIPTION = 'Rain delay stats?'
RAINDELAY_BODY = 'Rain rain, go away.  Come on back another day.'

POSTPONED_TITLE = 'Game Postponed'
POSTPONED_DESCRIPTION = "Game's over, makeup to be played later"
POSTPONED_BODY = 'On the bright side, we didn\'t lose'

COMPLETEDEARLY_TITLE = 'Game Completed Early'
COMPLETEDEARLY_DESCRIPTION = 'Magic 8 ball, will this game resume sometime tonight?'
COMPLETEDEARLY_BODY = '8-ball: "No chance in hell!"'

GAMEENDED_WIN_TITLE = 'Put it in the books!'
GAMEENDED_WIN_BODY = 'https://www.youtube.com/watch?v=mmwic9kFx2c' ## (TCB) 'https://www.youtube.com/watch?v=mmwic9kFx2c'
GAMEENDED_LOSS_TITLE = 'Mets defeated' # Mets defeated
GAMEENDED_LOSS_BODY = 'https://cdn.discordapp.com/attachments/411210054591578122/465340387037544448/killme.png' # We will get \'em next time  ## (dolphin) 'https://cdn.discordapp.com/attachments/411210054591578122/465340387037544448/killme.png')

SEVENTH_INNING_STRETCH = 'SEVENTH INNING STRETCH TIME!\nhttps://youtu.be/Tg3C0nvenro' # (Lazy Mary) https://youtu.be/Tg3C0nvenro

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

            self.GAME_THREAD_LOG = settings.get('GAME_THREAD_LOG')
            if self.GAME_THREAD_LOG == None: return "Missing GAME_THREAD_LOG"

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

    def hasPlayerQuip(self, gameEvent):
        if "Chase Utley" in gameEvent['description']: return True
        return False

    def formatPlayerQuips(self, description):
        if "Chase Utley" in description:
            playerQuips = [
                "Fuck Chase Utley",
                "uck-Fay ase_Utley-Chay"
            ]
            return random.choice(playerQuips)
        return ""

    def usePlayerNickNames(self, description):
        newDesc = description
        #    .replace("Pete Alonso", "POLAR BEAR")\
        #    .replace("Aaron Altherr", "A-A-RON")\
        #    .replace("Luis Avilan", "AVI")\
        #    .replace("Robinson Cano", "NOLO")\
        #    .replace("Yoenis Cespedes", "LA POTENCIA")\
        #    .replace("Michael Conforto", "FORTO")\
        #    .replace("J.D. Davis", "DIZZLE")\
        #    .replace("Jacob deGrom", "deGROM")\
        #    .replace("Edwin Diaz", "SUGAR")\
        #    .replace("Jeurys Familia", "YAGUATE")\
        #    .replace("Todd Frazier", "TODDFATHER")\
        #    .replace("Robert Gsellman", "G")\
        #    .replace("Luis Guillorme", "LUISMI")\
        #    .replace("Donnie Hart", "D.HART")\
        #    .replace("Adeiny Hechavarria", "LA PANTERA UUFF")\
        #    .replace("Juan Lagares", "JUAN JR")\
        #    .replace("Walter Lockett", "🔒")\
        #    .replace("Seth Lugo", "QUARTERRICAN")\
        #    .replace("Steven Matz", "MATZY")\
        #    .replace("Chris Mazza", "MAZZ")\
        #    .replace("Jeff McNeil", "FLYING SQUIRREL")\
        #    .replace("Tomas Nido", "NEEDZ")\
        #    .replace("Brandon Nimmo", "TATER")\
        #    .replace("Wilson Ramos", "BUFFALO")\
        #    .replace("Amed Rosario", "ROSIE")\
        #    .replace("Dominic Smith", "SUG")\
        #    .replace("Marcus Stroman", "HDMH")\
        #    .replace("Zack Wheeler", "WHEELS")\
        #    .replace("Justin Wilson", "J WILLY")\
        #    .replace("Joe Panik", "J. P.")
        return newDesc

    def formatGameEventForDiscord(self, gameEvent, linescore):
        return "```" \
               "{}\n" \
               "{}{}\n" \
               "```\n" \
               "{}" \
               "{}".format(self.formatLinescoreForDiscord(gameEvent, linescore)
                                          if not self.gameEventInningBeforeCurrentLinescoreInning(linescore, gameEvent)
                                          else self.formatLinescoreCatchingUpForDiscord(gameEvent, linescore),
                           self.formatPitchCount(gameEvent['gameEvent'], gameEvent['balls'], gameEvent['strikes']),
                           self.usePlayerNickNames(gameEvent['description']),
                           self.playerismsAndEmoji(gameEvent, linescore),
                           self.endOfInning(gameEvent))

    def formatPlayerChangeForDiscord(self, gameEvent, linescore):
        return "```" \
               "{}\n" \
               "```\n" \
               "{}" \
               "{}".format(self.usePlayerNickNames(gameEvent['description']),
                           self.playerismsAndEmoji(gameEvent, linescore),
                           self.endOfInning(gameEvent))

    def formatLinescoreForDiscord(self, gameEvent, linescore):
        return "{}   ┌───┬──┬──┬──┐\n" \
               "   {}     │{:<3}│{:>2}│{:>2}│{:>2}│\n" \
               "  {} {}    ├───┼──┼──┼──┤\n" \
               "{}   │{:<3}│{:>2}│{:>2}│{:>2}│\n" \
               "         └───┴──┴──┴──┘".format(
            self.formatInning(gameEvent),
            self.formatSecondBase(linescore['status']['runner_on_2b']),
            linescore['away_team_name']['team_abbrev'], linescore['away_team_stats']['team_runs'],
            linescore['away_team_stats']['team_hits'], linescore['away_team_stats']['team_errors'],
            self.formatThirdBase(linescore['status']['runner_on_3b']), self.formatFirstBase(linescore['status']['runner_on_1b']),
            self.formatOuts(gameEvent['outs']),
            linescore['home_team_name']['team_abbrev'], linescore['home_team_stats']['team_runs'],
            linescore['home_team_stats']['team_hits'], linescore['home_team_stats']['team_errors']
        )

    def formatLinescoreCatchingUpForDiscord(self, gameEvent, linescore):
        return "{}\n" \
               "\n" \
               "  BOT         CATCHING\n" \
               " BEHIND          UP\n" \
               "".format(
            self.formatInning(gameEvent)
        )

    def formatInning(self, gameEvent):
        return "{} {:>2}".format(gameEvent['topOrBot'], gameEvent['inning'])

    def formatOuts(self, outs):
        outOrOuts = " Outs"
        if outs is "1": outOrOuts = "  Out"
        return "".join([outs, outOrOuts])

    def formatFirstBase(self, runnerOnBaseStatus):
        return self.formatBase(runnerOnBaseStatus)

    def formatSecondBase(self, runnerOnBaseStatus):
        return self.formatBase(runnerOnBaseStatus)

    def formatThirdBase(self, runnerOnBaseStatus):
        return self.formatBase(runnerOnBaseStatus)

    def formatBase(self, baseOccupied):
        if baseOccupied:
            return "●"
        return "○"

    def formatPitchCount(self, gameEvent, balls, strikes):
        if gameEvent is 'atbat': return "On a {}-{} count, ".format(balls, strikes)
        elif gameEvent is 'action': return ""
        raise Exception("gameEvent not recognized")

    def endOfInning(self, gameEvent):
        if gameEvent['outs'] == "3":
            endOfInningString = "```------ End of {} ------```".format(self.formatInning(gameEvent))
            if gameEvent['inning'] == "7" and gameEvent['topOrBot'] == "TOP":
                endOfInningString = "{}\n{}".format(endOfInningString, SEVENTH_INNING_STRETCH)
            return endOfInningString
        return ""

    def playerismsAndEmoji(self, gameEvent, linescore):
        playerism = ""
        event = gameEvent['event']
        if self.favoriteTeamIsBatting(gameEvent, linescore):
            # Favorite team batting
            if "Home Run" in event and len(gameEvent['rbi']) == 4: playerism = ''.join([playerism, EMOTE_GRAND_SLAM, "\n"])
            elif "Home Run" in event and len(gameEvent['rbi']) != 4: playerism = ''.join([playerism, EMOTE_HOMERUN, "\n"])
            for RBIMap in gameEvent['rbi']:
                if RBIMap['rbi']: playerism = ''.join([playerism, EMOTE_RBI, " "])
                elif RBIMap['score'] and RBIMap['earned']:  playerism = ''.join([playerism, EMOTE_EARNED_RUN, " "])
                elif RBIMap['score'] and not RBIMap['earned']:  playerism = ''.join([playerism, EMOTE_UNEARNED_RUN, " "])
            if "Strikeout" in event:
                global otherTeamKTrackerTuple
                if "strikes out" in gameEvent['description']:
                    otherTeamKTrackerTuple = ("".join([otherTeamKTrackerTuple[0], EMOTE_OTHER_TEAM_STRIKEOUT]), otherTeamKTrackerTuple[1] + 1, otherTeamKTrackerTuple[2])
                if "called out on strike" in gameEvent['description']:
                    otherTeamKTrackerTuple = ("".join([otherTeamKTrackerTuple[0], EMOTE_OTHER_TEAM_STRIKEOUT_LOOKING]), otherTeamKTrackerTuple[1], otherTeamKTrackerTuple[2] + 1)

                if otherTeamKTrackerTuple[1] == 3 and otherTeamKTrackerTuple[2] == 0:
                    playerism = "".join(["Strikeout tracker: 3 ", EMOTE_OTHER_TEAM_STRIKEOUT, "s"])
                else:
                    playerism = "".join(["Strikeout tracker: ", otherTeamKTrackerTuple[0]])
        else:
            # Favorite team pitching
            if "Strikeout" in event:
                global favTeamKTrackerTuple
                if "strikes out" in gameEvent['description']:
                    favTeamKTrackerTuple = ("".join([favTeamKTrackerTuple[0], EMOTE_STRIKEOUT]), favTeamKTrackerTuple[1] + 1, favTeamKTrackerTuple[2])
                if "called out on strike" in gameEvent['description']:
                    favTeamKTrackerTuple = ("".join([favTeamKTrackerTuple[0], EMOTE_STRIKEOUT_LOOKING]), favTeamKTrackerTuple[1], favTeamKTrackerTuple[2] + 1)

                if favTeamKTrackerTuple[1] == 3 and favTeamKTrackerTuple[2] == 0:
                    playerism = "".join(["Strikeout tracker: 3 ", EMOTE_STRIKEOUT, "s"])
                else:
                    playerism = "".join(["Strikeout tracker: ", favTeamKTrackerTuple[0]])

            # Opponents batting
            for RBIMap in gameEvent['rbi']:
                if RBIMap['score'] and not RBIMap['earned']:  playerism = ''.join([playerism, EMOTE_OTHER_TEAM_UNEARNED_RUN, " "])
                elif RBIMap['rbi']: playerism = ''.join([playerism, EMOTE_OTHER_TEAM_RBI, " "])
                elif RBIMap['score'] and RBIMap['earned']:  playerism = ''.join([playerism, EMOTE_OTHER_TEAM_EARNED_RUN, " "])

        playerism = ''.join([playerism, "\n"])
        if self.hasPlayerQuip(gameEvent):
            playerism = "".join([playerism, self.formatPlayerQuips(gameEvent['description'])])
        return playerism

    def favoriteTeamIsBatting(self, gameEvent, linescore):
        return (self.favoriteTeamIsHomeTeam(linescore) and gameEvent['topOrBot'] == "BOT" or not self.favoriteTeamIsHomeTeam(linescore) and gameEvent['topOrBot'] == "TOP")

    def getEventIdsFromLog(self):
        idsFromLog = []
        with open(self.GAME_THREAD_LOG) as log:
            for line in log:
                splitLine = line.split(" ")
                id = splitLine[2][1:-1]
                idsFromLog.append(id)
        log.close()
        return idsFromLog

    def printToLog(self, atbat, linescore):
        with open(self.GAME_THREAD_LOG, "a") as log:
            id = atbat['id'] if atbat['id'] is not None else "NoIdInJSONFile"
            log.write("[{}] [{}] | {}\n".format(self.getTime(), id, self.formatAtBatLineForLog(atbat)))
        log.close()
        print("[{}] New atBat: {} {}".format(self.getTime(), self.formatAtBatLineForLog(atbat), self.getLinescoreStatus(linescore)))

    def printGameStatusToLog(self, id, gameStatus):
        with open(self.GAME_THREAD_LOG, "a") as log:
            log.write("[{}] [{}] | Game Status: {}\n".format(self.getTime(), id, gameStatus))
        log.close()
        print("[{}] Game Status: {}".format(self.getTime(), gameStatus))

    def commentOnDiscord(self, gameEvent, linescore):
        if self.gameUpdateIsPlayerChange(gameEvent):
            comment = self.formatPlayerChangeForDiscord(gameEvent, linescore)
        else:
            comment = self.formatGameEventForDiscord(gameEvent, linescore)
        return comment

    def gameUpdateIsPlayerChange(self, gameEvent):
        isPlayerChange = False
        if 'Pitching Substitution' in gameEvent['event']: isPlayerChange = True
        if 'Defensive Sub' in gameEvent['event']: isPlayerChange = True
        if 'Defensive Switch' in gameEvent['event']: isPlayerChange = True
        if 'Offensive Sub' in gameEvent['event']: isPlayerChange = True
        if 'Game Advisory' in gameEvent['event']: isPlayerChange = True
        if 'Umpire Substitution' in gameEvent['event']: isPlayerChange = True
        return isPlayerChange

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
        newGameLinescoreStatus = {'outs':"0", 'runnerOnBaseStatus':"0", 'runner_on_1b':False, 'runner_on_2b':False, 'runner_on_3b':False,
                                 'home_team_runs':"0", 'home_team_hits':"0", 'home_team_errors':"0",
                                 'away_team_runs':"0", 'away_team_hits':"0", 'away_team_errors':"0"}
        globalLinescoreStatus = newGameLinescoreStatus
        # initialize favTeamKTrackerTuple variable: string, swinging Ks, looking Ks
        global favTeamKTrackerTuple
        favTeamKTrackerTuple = ("", 0, 0)
        global otherTeamKTrackerTuple
        otherTeamKTrackerTuple = ("", 0, 0)

        response = None
        directories = []

        todaysGame = datetime.now() - timedelta(hours=5)

        while True:
            # If it's a new day, start a new game!
            if todaysGame.day is not (datetime.now()-timedelta(hours=5)).day:
                todaysGame = datetime.now() - timedelta(hours=5)
                favTeamKTrackerTuple = ("", 0, 0)
                otherTeamKTrackerTuple = ("", 0, 0)
                response = None
                directories = []
                globalLinescoreStatus = newGameLinescoreStatus
                print("[{}] New Day".format(self.getTime()))

            url = "http://gd2.mlb.com/components/game/mlb/"
            url = url + "year_" + todaysGame.strftime("%Y") + "/month_" + todaysGame.strftime \
                ("%m") + "/day_" + todaysGame.strftime("%d")

            while not response:
                # If need this here so bot doesn't get stuck on off days
                if todaysGame.day is not (datetime.now() - timedelta(hours=5)).day:
                    break

                print("[{}] Searching for day's URL...".format(self.getTime()))
                print(url)
                try:
                    # If it returns a 404, wait and try again
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as resp:
                            if resp.status == 200:
                                print("[{}] Found day's URL: {}".format(self.getTime(), url))
                                response = await resp.text()

                                soup = bs4.BeautifulSoup(response, 'html.parser')

                                # Get the gid directory based on team code (NYM is nyn)
                                for listitem in soup.find_all('li'):
                                    possibleGameId = listitem.get_text().strip()
                                    if (self.TEAM_CODE+'mlb') in possibleGameId:
                                        directories.append(url + "/" + possibleGameId)
                                        print("[{}] Found game directory for team {}: {}".format(self.getTime(),
                                                                                                 self.TEAM_CODE,
                                                                                                 directories))
                            await asyncio.sleep(20)
                except:
                    print("[{}] Couldn't find URL \"{}\", trying again...".format(self.getTime(), url))
                    await asyncio.sleep(20)

            try:
                for d in directories:

                    # Comment out this line to hard code a directory
                    #d = "http://gd2.mlb.com/components/game/mlb/year_2017/month_04/day_26/gid_2017_04_26_oakmlb_anamlb_1/"
                    print("[{}] Searching the URL directory for updates : {}".format(self.getTime(), d))

                    linescore_url = "".join([d ,"linescore.json"])
                    if not await linescoreParser.doesJSONExistYet(linescore_url):
                        print("[{}] Game has not started".format(self.getTime()))
                        continue
                    linescoreJSON = await linescoreParser.getJSONFromURL(linescore_url)
                    linescore = linescoreParser.parseGameDataIntoMap(linescoreJSON)

                    game_events_url = "".join([d ,"game_events.json"])
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
                        id = gameEvent['id']
                        if id not in idsOfPrevEvents:
                            if not self.linescoreAndGameEventsInSync(linescore, gameEvent):
                                break
                            self.updateGlobalLinescoreStatus(linescore)
                            self.printToLog(gameEvent, linescore)
                            await client.send_message(channel, self.commentOnDiscord(gameEvent, linescore))
                            self.resetOutsGlobalLinescoreStatus()
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
                #await client.send_message(channel, "Bot encountered an error.  Was there a review on the field?")

            await asyncio.sleep(1000)

        print("/*------------- End of Bot.run() -------------*/")

    def gameEventInningBeforeCurrentLinescoreInning(self, linescore, gameEvent):
        return True if int(gameEvent['inning']) < int(linescore['status']['currentInning']) else False

    def linescoreAndGameEventsInSync(self, linescore, gameEvent):
        if self.gameEventInningBeforeCurrentLinescoreInning(linescore, gameEvent): # if bot posting is behind, let it catch up
            return True
        if self.linescoreStatusHasChanged(linescore):
            return True
        if self.baseStatusChangingGameAction(gameEvent):
            return True
        return False

    def baseStatusChangingGameAction(self, gameEvent):
        actionIsBaseStatusChanging = False
        if 'Stolen Base' in gameEvent['event']: actionIsBaseStatusChanging = True
        if 'Balk' in gameEvent['event']: actionIsBaseStatusChanging = True
        if 'Wild Pitch' in gameEvent['event']: actionIsBaseStatusChanging = True
        if 'Defensive Indiff' in gameEvent['event']: actionIsBaseStatusChanging = True
        if 'Pickoff' in gameEvent['event']: actionIsBaseStatusChanging = True
        if 'Passed Ball' in gameEvent['event']: actionIsBaseStatusChanging = True
        if 'Caught Stealing' in gameEvent['event']: actionIsBaseStatusChanging = True
        if 'Picked off stealing' in gameEvent['event']: actionIsBaseStatusChanging = True
        return gameEvent['gameEvent'] == 'action' and not actionIsBaseStatusChanging

    def linescoreStatusHasChanged(self, linescore):
        global globalLinescoreStatus
        newLinescoreStatus = self.getLinescoreStatus(linescore)
        if globalLinescoreStatus != newLinescoreStatus:
            globalLinescoreStatus = newLinescoreStatus
            return True
        return False

    def getLinescoreStatus(self, linescore):
        # Outs, Base status, runner on 1b, runner on 2b, runner on 3b, Home runs, Home hits, Home errors, Away run, Away hits, Away errors
        return {'outs':linescore['status']['outs'], 'runnerOnBaseStatus':linescore['status']['runnerOnBaseStatus'],
                'runner_on_1b':linescore['status']['runner_on_1b'], 'runner_on_2b':linescore['status']['runner_on_2b'], 'runner_on_3b':linescore['status']['runner_on_3b'],
                'home_team_runs':linescore['home_team_stats']['team_runs'], 'home_team_hits':linescore['home_team_stats']['team_hits'], 'home_team_errors':linescore['home_team_stats']['team_errors'],
                'away_team_runs':linescore['away_team_stats']['team_runs'], 'away_team_hits':linescore['away_team_stats']['team_hits'], 'away_team_errors':linescore['away_team_stats']['team_errors']}

    def updateGlobalLinescoreStatus(self, linescore):
        newLinescoreStatus = self.getLinescoreStatus(linescore)
        global globalLinescoreStatus
        globalLinescoreStatus = newLinescoreStatus

    def resetOutsGlobalLinescoreStatus(self):
        global globalLinescoreStatus
        if globalLinescoreStatus['outs'] == "3": # Make sure to reset outs to 0 if outs = 3 (NOTE: will be out of sync from file's current linescore status)
            globalLinescoreStatus['outs'] = "0"

    def checkGameStatus(self, linescore, idsOfPrevEvents): #rain delay?
        id = linescore['status']['game_status_id']
        gameStatus = linescore['status']['game_status']
        if (gameStatus == "Warmup") and (id not in idsOfPrevEvents):
            self.printGameStatusToLog(id, gameStatus)
            em = self.warmupStatus(linescore)
            return em
        if (gameStatus == "In Progress") and (id not in idsOfPrevEvents):
            self.printGameStatusToLog(id, gameStatus)
            em = self.gameStartedStatus()
            return em
        if (gameStatus == "Delayed") and (id not in idsOfPrevEvents):
            self.printGameStatusToLog(id, gameStatus)
            em = self.gameDelayedStatus()
            return em
        if (gameStatus == "Postponed") and (id not in idsOfPrevEvents):
            self.printGameStatusToLog(id, gameStatus)
            em = self.gamePostponedStatus()
            return em
        if (gameStatus == "Completed Early") and (id not in idsOfPrevEvents):
            self.printGameStatusToLog(id, gameStatus)
            em = self.gameCompletedEarlyStatus()
            return em
        if (gameStatus == "Game Over") and (id not in idsOfPrevEvents):
            self.printGameStatusToLog(id, gameStatus)
            em = self.gameEndedStatus(linescore)
            return em
        return None

    def warmupStatus(self, linescore):
        if linescore['probableStartingPitchers'] is None:
            pregamePost = WARMUP_BODY_ALTERNATIVE
        else:
            pregamePost = "{:<3}: {} {} ({}-{} {})\n" \
                          "{:<3}: {} {} ({}-{} {})".format(
                linescore['away_team_name']['team_abbrev'], linescore['probableStartingPitchers']['away_pitcher']['throwinghand'],
                linescore['probableStartingPitchers']['away_pitcher']['name'], linescore['probableStartingPitchers']['away_pitcher']['wins'],
                linescore['probableStartingPitchers']['away_pitcher']['losses'], linescore['probableStartingPitchers']['away_pitcher']['era'],
                linescore['home_team_name']['team_abbrev'], linescore['probableStartingPitchers']['home_pitcher']['throwinghand'],
                linescore['probableStartingPitchers']['home_pitcher']['name'], linescore['probableStartingPitchers']['home_pitcher']['wins'],
                linescore['probableStartingPitchers']['home_pitcher']['losses'], linescore['probableStartingPitchers']['home_pitcher']['era'])
        return (discord.Embed(title=WARMUP_TITLE, description=WARMUP_DESCRIPTION),
                pregamePost)

    def gameStartedStatus(self): # Start of game post
        return (discord.Embed(title=GAMESTARTED_TITLE, description=GAMESTARTED_DESCRIPTION), GAMESTARTED_BODY)

    def gameDelayedStatus(self):
        em = (discord.Embed(title=RAINDELAY_TITLE, description=RAINDELAY_DESCRIPTION),
              RAINDELAY_BODY)
        return em

    def gamePostponedStatus(self):
        em = (discord.Embed(title=POSTPONED_TITLE, description=POSTPONED_DESCRIPTION),
              POSTPONED_BODY)
        return em

    def gameCompletedEarlyStatus(self):
        em = (discord.Embed(title=COMPLETEDEARLY_TITLE, description=COMPLETEDEARLY_DESCRIPTION),
              COMPLETEDEARLY_BODY)
        return em

    def gameEndedStatus(self, linescore):
        favoriteTeamWLRecord = self.getFavoriteTeamWLRecord(linescore)
        otherTeamWLRecord = self.getOtherTeamWLRecord(linescore)
        if self.isFavoriteTeamWinning(linescore):
            # TCB url 'https://www.youtube.com/watch?v=mmwic9kFx2c'
            title = GAMEENDED_WIN_TITLE
            description = '{} ({}-{}) beat the {} ({}-{}) by a score of {}-{}!'.format(
                favoriteTeamWLRecord[0], favoriteTeamWLRecord[1], favoriteTeamWLRecord[2],
                otherTeamWLRecord[0], otherTeamWLRecord[1], otherTeamWLRecord[2],
                linescore['away_team_stats']['team_runs'], linescore['home_team_stats']['team_runs']
            )
            em = (discord.Embed(title=title, description=description),
                  GAMEENDED_WIN_BODY)
        else:
            title = GAMEENDED_LOSS_TITLE
            description = '{} ({}-{}) were defeated by the {} ({}-{}) by a score of {}-{}'.format(
                favoriteTeamWLRecord[0], favoriteTeamWLRecord[1], favoriteTeamWLRecord[2],
                otherTeamWLRecord[0], otherTeamWLRecord[1], otherTeamWLRecord[2],
                linescore['away_team_stats']['team_runs'], linescore['home_team_stats']['team_runs']
            )
            em = (discord.Embed(title=title, description=description),
                  GAMEENDED_LOSS_BODY)
        return em

    def isFavoriteTeamWinning(self, linescore):
        homeTeamRuns = linescore['home_team_stats']['team_runs']
        awayTeamRuns = linescore['away_team_stats']['team_runs']
        favoriteTeamIsHomeTeam = self.favoriteTeamIsHomeTeam(linescore)
        return (favoriteTeamIsHomeTeam and (int(homeTeamRuns) > int(awayTeamRuns))) or \
               (not favoriteTeamIsHomeTeam and (int(homeTeamRuns) < int(awayTeamRuns)))

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

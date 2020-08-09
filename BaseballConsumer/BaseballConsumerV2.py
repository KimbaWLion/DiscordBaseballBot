'''

BASEBALL GAME THREAD BOT

Written by:
/u/KimbaWLion

Please contact us on Reddit or Github if you have any questions.

'''

import statsapi
from datetime import datetime, timedelta
import asyncio
import discord
import json

SETTINGS_FILE = './settings.json'

# Game Status Constants
WARMUP_TITLE = 'Game\'s about to start, everyone get in here!'
WARMUP_DESCRIPTION = "Let's go win this one!" # Meet the Mets, meet the Mets.  Step right up and greet the Mets...
WARMUP_BODY_ALTERNATIVE = "https://www.youtube.com/watch?v=6GsCmnZnllk" # MTM https://www.youtube.com/watch?v=6GsCmnZnllk

GAMESTARTED_TITLE = 'Play ball!'
GAMESTARTED_DESCRIPTION = 'HYPE HYPE HYPE HYPE HYPE HYPE HYPE'
GAMESTARTED_BODY = "Let's go Mets!"

GAMEENDED_WIN_TITLE = 'Put it in the books!'
GAMEENDED_WIN_BODY = 'https://www.youtube.com/watch?v=mmwic9kFx2c' ## (TCB) 'https://www.youtube.com/watch?v=mmwic9kFx2c'
GAMEENDED_LOSS_TITLE = 'Mets defeated' # Mets defeated
GAMEENDED_LOSS_BODY = 'https://cdn.discordapp.com/attachments/411210054591578122/465340387037544448/killme.png' # We will get \'em next time  ## (dolphin) 'https://cdn.discordapp.com/attachments/411210054591578122/465340387037544448/killme.png')

SEVENTH_INNING_STRETCH = 'SEVENTH INNING STRETCH TIME!\nhttps://youtu.be/Tg3C0nvenro' # (Lazy Mary) https://youtu.be/Tg3C0nvenro

class BaseballUpdaterBotV2:

    async def run(self, client, channel):
        error_msg = self.read_settings()
        if error_msg != 0:
            print(error_msg)
            return

        print('in BaseballUpdaterBotV2.run()')

        while True:
            todaysGame = (datetime.now() - timedelta(hours=5))


            sched = statsapi.schedule(date=todaysGame.strftime("%m/%d/%Y"),team=self.TEAM_ID)
            if not sched:
                print("[{}] No game today".format(self.getTime()))
                await asyncio.sleep(1000)
            for game in sched:
                if game['status'] == 'Scheduled':
                    print("[{}] Game is Scheduled".format(self.getTime()))
                    await asyncio.sleep(300)
                if game['status'] == 'Pre-Game':
                    print("[{}] Game is Pre-Game".format(self.getTime()))
                    await asyncio.sleep(60)
                if game['status'] == 'Warmup':
                    print("[{}] Game is Warmup".format(self.getTime()))
                    # self.warmupStatus(info)
                    await asyncio.sleep(60)
                if game['status'] == 'In Progress':
                    print("[{}] Game is in Progress".format(self.getTime()))
                    gameInfo = statsapi.get('game', {'gamePk': game['game_id']})
                    liveData = gameInfo['liveData']
                    plays = liveData['plays']['allPlays']
                    linescore = liveData['linescore']
                    for play in plays:
                        if not 'description' in play['result'].keys():
                            continue

                        # Get info from plays
                        info = {}
                        info['startTime'] = play['about']['startTime']
                        info['inning'] = str(play['about']['inning'])
                        info['inningHalf'] = play['about']['halfInning']
                        info['balls'] = str(play['count']['balls'])
                        info['strikes'] = str(play['count']['strikes'])
                        info['outs'] = str(play['count']['outs'])
                        info['homeScore'] = str(play['result']['homeScore'])
                        info['awayScore'] = str(play['result']['awayScore'])
                        info['description'] = play['result']['description']
                        info['rbi'] = play['result']['rbi']
                        info['playType'] = play['result']['type']
                        info['manOnFirst'] = True if 'postOnFirst' in play['matchup'] else False
                        info['manOnSecond'] = True if 'postOnSecond' in play['matchup'] else False
                        info['manOnThird'] = True if 'postOnThird' in play['matchup'] else False
                        info['runsScored'] = 0
                        info['rbis'] = 0
                        info['runsEarned'] = 0
                        for runner in play['runners']:
                            info['runsScored'] += 1 if runner['details']['isScoringEvent'] else 0
                            info['rbis'] += 1 if runner['details']['rbi'] else 0
                            info['runsEarned'] += 1 if runner['details']['earned'] else 0

                        # Get info from linescore
                        info['outs_linescore'] = linescore['outs']
                        info['homeStats_linescore'] = linescore['teams']['home'] #runs, hits, errors, lefOnBase
                        info['awayStats_linescore'] = linescore['teams']['away']
                        info['currentInning_linescore'] = linescore['currentInning']
                        info['inningState_linescore'] = linescore['inningState'] # Middle or End
                        info['inningHalf_linescore'] = linescore['inningHalf']

                        info['id'] = ''.join([info['startTime'],';',info['outs'],';',info['inning'],';',info['homeScore'],';',info['awayScore'],';',info['description'].replace(" ", "")])
                        idsOfPrevEvents = self.getEventIdsFromLog()
                        if info['id'] not in idsOfPrevEvents:
                            self.printToLog(info)
                            await channel.send(self.commentOnDiscord(info))
                            if 'Status Change' in info['description']: print(play)

                if game['status'] == 'Game Over':
                    print("[{}] Game is Over".format(self.getTime()))
                    await asyncio.sleep(60)
                if game['status'] == 'Final':
                    print("[{}] Game is Final".format(self.getTime()))
                    await asyncio.sleep(300)
            await asyncio.sleep(10)
        print("/*------------- End of Bot.run() -------------*/")

    def read_settings(self):
        with open(SETTINGS_FILE) as data:
            settings = json.load(data)

            self.GAME_THREAD_LOG = settings.get('GAME_THREAD_LOG')
            if self.GAME_THREAD_LOG == None: return "Missing GAME_THREAD_LOG"

            self.TEAM_ID = settings.get('TEAM_ID')
            if self.TEAM_ID == None: return "Missing TEAM_ID"

        return 0

    def getTime(self):
        today = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
        return today

    def printToLog(self, info):
        with open(self.GAME_THREAD_LOG, "a") as log:
            log.write("[{}] [{}] | {}\n".format(self.getTime(), info['id'], info['description']))
        log.close()
        print("[{}] New atBat: {}".format(self.getTime(), info['description']))

    def getEventIdsFromLog(self):
        idsFromLog = []
        with open(self.GAME_THREAD_LOG) as log:
            for line in log:
                splitLine = line.split(" ")
                id = splitLine[2][1:-1]
                idsFromLog.append(id)
        log.close()
        return idsFromLog

    def commentOnDiscord(self, info):
        if info['playType'] == 'atBat':
            comment = self.formatGameEventForDiscord(info)
        else:
            comment = self.formatPlayerChangeForDiscord(info)
        return comment

    def formatGameEventForDiscord(self, info):
        return "```" \
               "{}\n" \
               "{}{}\n" \
               "```\n" \
               "{}" \
               "{}".format(self.formatLinescoreForDiscord(info)
                                          if not self.gameEventInningBeforeCurrentLinescoreInning(info)
                                          else self.formatLinescoreCatchingUpForDiscord(info),
                           self.formatPitchCount(info), info['description'],
                           "", #self.playerismsAndEmoji(gameEvent, linescore)
                           self.endOfInning(info))

    def formatLinescoreForDiscord(self, info):
        return "{}   ┌───┬──┬──┬──┐\n" \
               "   {}     │{:<3}│{:>2}│{:>2}│{:>2}│\n" \
               "  {} {}    ├───┼──┼──┼──┤\n" \
               "{}   │{:<3}│{:>2}│{:>2}│{:>2}│\n" \
               "         └───┴──┴──┴──┘".format(
            self.formatInning(info),
            self.formatSecondBase(info['manOnSecond']),
            "AWA", info['awayStats_linescore']['runs'],info['awayStats_linescore']['hits'], info['awayStats_linescore']['errors'],
            self.formatThirdBase(info['manOnThird']), self.formatFirstBase(info['manOnFirst']),
            self.formatOuts(info['outs']),
            "HOM", info['homeStats_linescore']['runs'],info['homeStats_linescore']['hits'], info['homeStats_linescore']['errors']
        )

    def gameEventInningBeforeCurrentLinescoreInning(self, info):
        return True if int(info['inning']) < int(info['currentInning_linescore']) else False

    def formatLinescoreCatchingUpForDiscord(self, info):
        return "{}\n" \
               "\n" \
               "  BOT         CATCHING\n" \
               " BEHIND          UP\n" \
               "".format(
            self.formatInning(info)
        )

    def formatInning(self, info):
        return "{} {:>2}".format(info['inningHalf'].upper()[0:3], info['inning'])

    def formatOuts(self, outs):
        outOrOuts = " Outs"
        if outs == "1": outOrOuts = "  Out"
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

    def formatPitchCount(self, info):
        if info['playType'] == 'atBat': return "On a {}-{} count, ".format(info['balls'], info['strikes'])
        else: return ""

    def endOfInning(self, info):
        if info['outs'] == "3":
            endOfInningString = "```------ End of {} ------```".format(self.formatInning(info))
            if info['inning'] == "7" and info['inningHalf'] == "Top":
                endOfInningString = "{}\n{}".format(endOfInningString, SEVENTH_INNING_STRETCH)
            return endOfInningString
        return ""

    def formatPlayerChangeForDiscord(self, info):
        return "```" \
               "{}\n" \
               "```\n" \
               "{}" \
               "{}".format(info['description'],
                           "", #self.playerismsAndEmoji(gameEvent, linescore),
                           self.endOfInning(info))

    def warmupStatus(self, info):
        pregamePost = "{:<3}: {} {} ({}-{} {})\n" \
                      "{:<3}: {} {} ({}-{} {})".format(
            "away team", "away pitcher throwing hand",
            "away pitcher name", "away pitcher wins",
            "away pitcher losses", "away pitcher era",
            "home team", "home pitcher throwing hand",
            "home pitcher name", "home pitcher wins",
            "home pitcher losses", "home pitcher era")
        return (discord.Embed(title=WARMUP_TITLE, description=WARMUP_DESCRIPTION),
                pregamePost)

    def gameStartedStatus(self): # Start of game post
        return (discord.Embed(title=GAMESTARTED_TITLE, description=GAMESTARTED_DESCRIPTION), GAMESTARTED_BODY)


if __name__ == '__main__':
    baseballUpdaterBot = BaseballUpdaterBotV2()
    baseballUpdaterBot.run()

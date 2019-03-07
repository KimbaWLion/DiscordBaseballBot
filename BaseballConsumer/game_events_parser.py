'''

Editted by:
KimbaWLion

Please contact us on Reddit or Github if you have any questions.

'''

# from urllib.request import urlopen
import sys
import json
import time
import aiohttp

class GameEventsParser:
    def __init__(self):
        self.TEST = None

    def openfile(self,filename):
        while True:
            try:
                fo = open(filename, "r")
                break
            except: #Normally this has a wait and then goes back into the loop.  Exitting for testing purposes
                print("Couldn't find read file, exiting...")
                time.sleep(20)
                exit(1)
        return fo

    def getJSONFromFile(self,filename):
        fo = self.openfile(filename)
        return json.load(fo)

    async def doesJSONExistYet(self,url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        return True
            return False
        except:
            e = sys.exc_info()[0]
            print("Exception occurred: {}".format(e))
            return False

    async def getJSONFromURL(self,url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()

    def getInnings(self, json):
        return json.get('data').get('game').get('inning')

    def getCurrentBatter(self, json):
        return json.get('data').get('game').get('atBat').get('pid')

    def getInningNumber(self, inning):
        return inning.get('num')

    def getHalfInningAtBats(self, inning, topOrBottom):
        atbats = []
        if type(inning) is str: return atbats
        atbats = inning.get(topOrBottom).get('atbat')
        if atbats is None: atbats = [] # If no at bats, return empty list to make sure the loop doesn't fail
        return atbats

    def getTopHalfInningAtBats(self, inning):
        return self.getHalfInningAtBats(inning, 'top')

    def getBottomHalfInningAtBats(self, inning):
        return self.getHalfInningAtBats(inning, 'bottom')

    def getHalfInningActions(self, inning, topOrBottom):
        actions = []
        if type(inning) is str: return actions
        actions = inning.get(topOrBottom).get('action')
        if actions is None: actions = []
        if type(actions) is dict: actions = [actions]
        return actions

    def getTopHalfInningActions(self, inning):
        return self.getHalfInningActions(inning, 'top')

    def getBottomHalfInningActions(self, inning):
        return self.getHalfInningActions(inning, 'bottom')

    def printAtBats(self ,atBats):
        for indx_top, atbat in enumerate(atBats):
            print(atbat.get('des'))

    def getGameEventsMap(self, gameEvent, inningNum, inningTopOrBot):
        gameEventMap = {}
        gameEventMap['result'] = gameEvent.get('event')
        gameEventMap['description'] = gameEvent.get('des')
        gameEventMap['balls'] = gameEvent.get('b')
        gameEventMap['strikes'] = gameEvent.get('s')
        gameEventMap['outs'] = gameEvent.get('o')
        gameEventMap['homeTeamRuns'] = gameEvent.get('home_team_runs')
        gameEventMap['awayTeamRuns'] = gameEvent.get('away_team_runs')
        gameEventMap['batterId'] = gameEvent.get('batter')
        gameEventMap['event'] = gameEvent.get('event')
        gameEventMap['id'] = self.getId(gameEvent)
        gameEventMap['rbi'] = gameEvent.get('rbi')
        #gameEventMap['playNumber'] = atbat.get('num')
        #gameEventMap['time'] = atbat.get('start_tfs')
        gameEventMap['inning'] = inningNum
        gameEventMap['topOrBot'] = inningTopOrBot
        return gameEventMap

    def getId(self, gameEvent):
        id = gameEvent.get('play_guid')
        return id

    def getAtBatMap(self, atbat, inningNum, inningTopOrBot):
        atbatMap = self.getGameEventsMap(atbat, inningNum, inningTopOrBot)
        #atbatMap['playNumber'] = atbat.get('num')
        #atbatMap['time'] = atbat.get('start_tfs')
        if atbatMap['id'] is None: atbatMap['id'] = ''.join(["NoIdInJSONFile", atbat.get('start_tfs_zulu')])
        atbatMap['gameEvent'] = 'atbat'
        return atbatMap

    def getActionsMap(self, action, inningNum, inningTopOrBot):
        actionMap = self.getGameEventsMap(action, inningNum, inningTopOrBot)
        if actionMap['id'] is None: actionMap['id'] = ''.join(["NoIdInJSONFile",action.get('tfs_zulu'),actionMap['description'].replace(" ","")])
        #if actionMap['batterId'] is None: actionMap['batterId'] = action.get('player')
        actionMap['gameEvent'] = 'action'
        return actionMap

    def getAtBats(self, halfInning, inningNum, inningTopOrBot):
        atBatList = []
        try:
            if not isinstance(halfInning, list): # First atbat of the inning is not in a list due to mlb.com bad coding
                atBatList.append(self.getAtBatMap(halfInning, inningNum, inningTopOrBot))
            else:
                for atbat in halfInning:
                    atBatList.append(self.getAtBatMap(atbat, inningNum, inningTopOrBot))
        except AttributeError:
            print("Exception in getAtBats (str has no get attr) --> why is it not a dict?")
            e = sys.exc_info()[0]
            print("Exception occurred, getAtBats is not a list yet, it only has one at bat: {}".format(e))
            pass
        return atBatList

    def getActions(self, halfInning, inningNum, inningTopOrBot):
        actionsList = []
        for action in halfInning:
            actionsList.append(self.getActionsMap(action, inningNum, inningTopOrBot))
        return actionsList

    def getListOfGameEvents(self,innings):
        gameEventList = []
        if type(innings) is not list:
            topAtBats = self.getTopHalfInningAtBats(innings)
            topActions = self.getTopHalfInningActions(innings)
            botAtBats = self.getBottomHalfInningAtBats(innings)
            botActions = self.getBottomHalfInningActions(innings)
            gameEventList.extend(self.getAtBats(topAtBats, innings.get('num'), 'TOP'))
            gameEventList.extend(self.getActions(topActions, innings.get('num'), 'TOP'))
            gameEventList.extend(self.getAtBats(botAtBats, innings.get('num'), 'BOT'))
            gameEventList.extend(self.getActions(botActions, innings.get('num'), 'BOT'))
        else:
            for inning in innings:
                topAtBats = self.getTopHalfInningAtBats(inning)
                topActions = self.getTopHalfInningActions(inning)
                botAtBats = self.getBottomHalfInningAtBats(inning)
                botActions = self.getBottomHalfInningActions(inning)
                gameEventList.extend(self.getAtBats(topAtBats, inning.get('num'), 'TOP'))
                gameEventList.extend(self.getActions(topActions, inning.get('num'), 'TOP'))
                gameEventList.extend(self.getAtBats(botAtBats, inning.get('num'), 'BOT'))
                gameEventList.extend(self.getActions(botActions, inning.get('num'), 'BOT'))
        return gameEventList

    def printInnings(self,innings):
        for inning in innings:
            top = self.getTopHalfInningAtBats(inning)
            bot = self.getBottomHalfInningAtBats(inning)
            self.printAtBats(top)
            self.printAtBats(bot)

    def gameHasStarted(self,innings):
        if type(innings) is not list:
            checkList = self.getTopHalfInningAtBats(innings)
            if checkList is not []:
                return True
        else:
            for inning in innings:
                checkList = self.getTopHalfInningAtBats(inning)
                if checkList is not []:
                    return True
        return False

    def getListOfActions(self, inning):
        pass

    def testfile(self,filename):
        json = self.getJSONFromFile(filename)
        innings = self.getInnings(json)
        self.printInnings(innings)

    def testurl(self,url):
        json = self.getJSONFromURL(url)
        innings = self.getInnings(json)
        self.printInnings(innings)

    def testfile1(self):
        filename =  "../testing_jsons/testfile1.json"
        self.testfile(filename)

    def testfile2(self):
        filename = "../testing_jsons/testfile2.json"
        self.testfile(filename)

    def testurl1(self):
        url = "http://gd2.mlb.com/components/game/mlb/year_2016/month_05/day_24/gid_2016_05_24_nynmlb_wasmlb_1/game_events.json"
        self.testurl(url)

if __name__ == '__main__':
    program = GameEventsParser()
    program.testurl1()

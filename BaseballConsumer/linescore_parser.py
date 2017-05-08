'''

Written by:
KimbaWLion

Please contact us on Reddit or Github if you have any questions.

'''

# from urllib.request import urlopen
import sys
import json
import time
import aiohttp
import asyncio


class LinescoreParser:
    def __init__(self):
        self.TEST = None

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

    def getGameData(self,json):
        return json.get('data').get('game')

    def parseGameDataIntoMap(self,json):
        data = self.getGameData(json)
        dataMap = {}
        dataMap['home_team_name'] = self.getTeamName("HOME", data)
        dataMap['away_team_name'] = self.getTeamName("AWAY", data)
        dataMap['home_team_record'] = self.getTeamRecord("HOME", data)
        dataMap['away_team_record'] = self.getTeamRecord("AWAY", data)
        dataMap['home_team_stats'] = self.getTeamStats("HOME", data)
        dataMap['away_team_stats'] = self.getTeamStats("AWAY", data)
        dataMap['inning_data'] = self.getInningData(data)
        dataMap['specialty_info'] = self.getSpecialtyInfo(data)
        dataMap['status'] = self.getGameStatusInfo(data)
        dataMap['currentPlayers'] = self.getCurrentPlayers(data)
        return dataMap

    def getTeamName(self, homeOrAway, data):
        teamMap = {}
        if homeOrAway is "HOME":
            team_name = 'home_team_name'
            team_city = 'home_team_city'
            team_abbrev = 'home_name_abbrev'
        if homeOrAway is "AWAY":
            team_name = 'away_team_name'
            team_city = 'away_team_city'
            team_abbrev = 'away_name_abbrev'
        teamMap['team_name'] = data.get(team_name)
        teamMap['team_city'] = data.get(team_city)
        teamMap['team_abbrev'] = data.get(team_abbrev)
        teamMap['team_full_name'] = '{} {}'.format(team_city, team_name)
        return teamMap

    def getTeamRecord(self, homeOrAway, data):
        recordMap = {}
        if homeOrAway is "HOME":
            team_wins = 'home_win'
            team_losses = 'home_loss'
        if homeOrAway is "AWAY":
            team_wins = 'away_win'
            team_losses = 'away_loss'
        recordMap['team_wins'] = data.get(team_wins)
        recordMap['team_losses'] = data.get(team_losses)
        return recordMap

    def getTeamStats(self, homeOrAway, data):
        statsMap = {}
        if homeOrAway is "HOME":
            team_runs = 'home_team_runs'
            team_hits = 'home_team_hits'
            team_errors = 'home_team_errors'
        if homeOrAway is "AWAY":
            team_runs = 'away_team_runs'
            team_hits = 'away_team_hits'
            team_errors = 'away_team_errors'
        statsMap['team_runs'] = data.get(team_runs)
        statsMap['team_hits'] = data.get(team_hits)
        statsMap['team_errors'] = data.get(team_errors)
        return statsMap

    def getInningData(self, data):
        inningsMap = {}
        linescore = data.get('linescore')
        if linescore is None: return inningsMap
        if type(linescore) is not list:
            inningMap = {}
            inningMap['home_runs'] = linescore.get('home_inning_runs')
            inningMap['away_runs'] = linescore.get('away_inning_runs')
            inningsMap[linescore.get('inning')] = inningMap
        else :
            for inning in linescore:
                inningMap = {}
                inningMap['home_runs'] = inning.get('home_inning_runs')
                inningMap['away_runs'] = inning.get('away_inning_runs')
                inningsMap[inning.get('inning')] = inningMap
        return inningsMap

    def getSpecialtyInfo(self, data):
        specialtyInfoMap = {}
        specialtyInfoMap['is_no_hitter'] = (data.get('is_no_hitter') is 'Y')
        specialtyInfoMap['is_perfect_game'] = (data.get('is_no_hitter') is 'Y')
        return specialtyInfoMap

    def getGameStatusInfo(self, data):
        statusInfoMap = {}
        statusInfoMap['game_status'] = data.get('status')
        statusInfoMap['game_status_id'] = "".join([data.get('id'), statusInfoMap['game_status'].replace(" ", "")])
        statusInfoMap['runnerOnBaseStatus'] = data.get('runner_on_base_status')
        statusInfoMap['outs'] = data.get('outs')
        return statusInfoMap

    def getCurrentPlayers(self, data):
        currentPlayersMap = {}
        batterMap = {}
        pitcherMap = {}
        if data.get('current_batter') is None: return None
        batterMap['name'] = ' '.join([data.get('current_batter').get('first_name'),data.get('current_batter').get('last_name')])
        batterMap['id'] = data.get('current_batter').get('id')
        pitcherMap['name'] = ' '.join([data.get('current_pitcher').get('first_name'),data.get('current_pitcher').get('last_name')])
        pitcherMap['id'] = data.get('current_pitcher').get('id')
        currentPlayersMap['pitcher'] = pitcherMap
        currentPlayersMap['batter'] = batterMap
        return currentPlayersMap

    def isGameStarted(self, data):
        statusInfo = self.getStatusInfo(data)
        if statusInfo['game_status'] is "In Progress":
            return statusInfo
        return None

    def isGameOver(self, data):
        statusInfo = self.getStatusInfo(data)
        if statusInfo['game_status'] is "Game Over":
            return statusInfo
        return None

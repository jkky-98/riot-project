import requests
import json
import time
import pandas as pd
from tqdm import tqdm
from .models import UserMatch, Participant

API_KEY = "RGAPI-386d379c-ff98-45c4-9d3b-f0f36ca0d24b"

class RiotAPI:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.header = {"X-Riot-Token": API_KEY,
                       "count": "100",
                       }

    def get_puuid_from_summonerName(self, summonerName):
        url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}"
        response = requests.get(url, headers=self.header)
        return response.json()['puuid']
    
    def get_matchid_lst_from_puuid(self, puuid):
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?"
        option = 'type=ranked&start=0&count=100'
        url_f = url + option
        response = requests.get(url_f, headers=self.header)
        return response.json()
    
    def get_match_matchId(self, matchId):
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}"
        response = requests.get(url, headers=self.header)
        return response.json()             

    def get_match_Full(self, summonerName):
        puuid = self.get_puuid_from_summonerName(summonerName)
        matchid_lst = self.get_matchid_lst_from_puuid(puuid)
        match_lst = []
        for matchId in tqdm(matchid_lst):
            match_lst.append(self.get_match_matchId(matchId))
            time.sleep(0.1)
        return match_lst
    
    def authenticate_RiotID(self, riotID):
        try:
            self.get_puuid_from_summonerName(riotID)
            return True
        except:
            return False
        
    def get_user_profile(self, puuid):
        url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        response = requests.get(url, headers=self.header)
        return response.json()
        

class MatchData:
    def __init__(self, metadata, info):
        self.dataVersion = metadata.get('dataVersion', '')
        self.match_id = metadata.get('matchId', '')
        self.endofGameResult = info.get('gameMode', '')
        self.gameCreation = info.get('gameCreation', '')
        self.gameDuration = info.get('gameDuration', '')
        self.gameEndTimestamp = info.get('gameEndTimestamp', '')
        self.gameId = info.get('gameId', '')
        self.gameMode = info.get('gameMode', '')
        self.gameName = info.get('gameName', '')
        self.mapId = info.get('mapId', '')

def update_matches(new_matches):
    for match in new_matches:
        metadata = match.get('metadata', {})
        info = match.get('info', {})
        match_data = MatchData(metadata, info)
        # 중복 여부를 확인하고 데이터베이스에 저장하는 로직을 수행합니다.
        try:
            match = UserMatch.objects.get(match_id=match_data.match_id)
        except UserMatch.DoesNotExist:
            # 데이터베이스에 존재하지 않는 경우 새로운 매치 데이터를 저장합니다.
            match = UserMatch.objects.create(
                dataVersion=match_data.dataVersion,
                match_id=match_data.match_id,
                endofGameResult=match_data.endofGameResult,
                gameCreation=match_data.gameCreation,
                gameDuration=match_data.gameDuration,
                gameEndTimestamp=match_data.gameEndTimestamp,
                gameId=match_data.gameId,
                gameMode=match_data.gameMode,
                gameName=match_data.gameName,
                mapId=match_data.mapId,
            )
            match.save()
            print("Match saved successfully {}".format(match_data.match_id))
            # 참가자 정보를 저장합니다.
            participants = info.get('participants', []) # lst
            for participant in participants:
                # 참가자 정보가 이미 존재하는지 확인합니다.
                try:
                    par_entry = Participant.objects.get(user_match=match, puuid=participant.get('puuid', ''))
                except Participant.DoesNotExist:
                    par_entry = Participant.objects.create(
                        user_match = match,
                        assists = participant.get('assists', 0),
                        bountyGold = participant.get("challenges").get('bountyGold', 0),
                        controlWardsPlaced = participant.get("challenges").get('controlWardsPlaced', 0),
                        damagePerMinute = participant.get("challenges").get('damagePerMinute', 0),
                        damageTakenOnTeamPercentage = participant.get("challenges").get('damageTakenOnTeamPercentage', 0),
                        deathsByEnemyChamps =  participant.get("challenges").get('deathsByEnemyChamps', 0),
                        earlyLaningPhaseGoldExpAdvantage = participant.get("challenges").get('earlyLaningPhaseGoldExpAdvantage', 0),
                        epicMonsterKillsNearEnemyJungler = participant.get("challenges").get('epicMonsterKillsNearEnemyJungler', 0),
                        epicMonsterSteals = participant.get("challenges").get('epicMonsterSteals', 0),
                        epicMonsterStolenWithoutSmite = participant.get("challenges").get('epicMonsterStolenWithoutSmite', 0),
                        firstTurretKilled = participant.get("challenges").get('firstTurretKilled', False),
                        firstTurretKilledTime = participant.get("challenges").get('firstTurretKilledTime', 0),
                        gameLength = participant.get("challenges").get('gameLength', 0),
                        goldPerMinute = participant.get("challenges").get('goldPerMinute', 0),
                        immobilizeAndKillWithAlly = participant.get("challenges").get('immobilizeAndKillWithAlly', 0),
                        initialBuffCount = participant.get("challenges").get('initialBuffCount', 0),
                        initialCrabCount = participant.get("challenges").get('initialCrabCount', 0),
                        jungleCsBefore10Minutes = participant.get("challenges").get('jungleCsBefore10Minutes', 0),
                        kTurretsDestroyedBeforePlatesFall = participant.get("challenges").get('kTurretsDestroyedBeforePlatesFall', 0),
                        kda = participant.get("challenges").get('kda', 0),
                        killAfterHiddenWithAlly = participant.get("challenges").get('killAfterHiddenWithAlly', 0),
                        killParticipation = participant.get("challenges").get('killParticipation', 0),
                        killingSprees = participant.get('killingSprees', 0),
                        killsNearEnemyTurret = participant.get("challenges").get('killsNearEnemyTurret', 0),
                        killsOnOtherLanesEarlyJungleAsLaner = participant.get("challenges").get('killsOnOtherLanesEarlyJungleAsLaner', 0),
                        killsUnderOwnTurret = participant.get("challenges").get('killsUnderOwnTurret', 0),
                        knockEnemyIntoTeamAndKill = participant.get("challenges").get('knockEnemyIntoTeamAndKill', 0),
                        laneMinionsFirst10Minutes = participant.get("challenges").get('laneMinionsFirst10Minutes', 0),
                        laningPhaseGoldExpAdvantage = participant.get("challenges").get('laningPhaseGoldExpAdvantage', 0),
                        legendaryCount = participant.get("challenges").get('legendaryCount', 0),
                        maxCsAdvantageOnLaneOpponent = participant.get("challenges").get('maxCsAdvantageOnLaneOpponent', 0),
                        maxLevelLeadLaneOpponent = participant.get("challenges").get('maxLevelLeadLaneOpponent', 0),
                        moreEnemyJungleThanOpponent = participant.get("challenges").get('moreEnemyJungleThanOpponent', 0),
                        multikills = participant.get("challenges").get('multikills', 0),
                        multikillsAfterAggressiveFlash = participant.get("challenges").get('multikillsAfterAggressiveFlash', 0),
                        outerTurretExecutesBefore10Minutes = participant.get("challenges").get('outerTurretExecutesBefore10Minutes', 0),
                        outnumberedKills = participant.get("challenges").get('outnumberedKills', 0),
                        scuttleCrabKills = participant.get("challenges").get('scuttleCrabKills', 0),
                        skillshotsDodged = participant.get("challenges").get('skillshotsDodged', 0),
                        soloKills = participant.get("challenges").get('soloKills', 0),
                        stealthWardsPlaced = participant.get("challenges").get('stealthWardsPlaced', 0),
                        takedownOnFirstTurret = participant.get("challenges").get('takedownOnFirstTurret', 0),
                        takedowns = participant.get("challenges").get('takedowns', 0),
                        takedownsFirstXMinutes = participant.get("challenges").get('takedownsFirstXMinutes', 0),
                        teamDamagePercentage = participant.get("challenges").get('teamDamagePercentage', 0),
                        teleportTakedowns = participant.get("challenges").get('teleportTakedowns', 0),
                        turretPlatesTaken = participant.get("challenges").get('turretPlatesTaken', 0),
                        turretTakedowns = participant.get("challenges").get('turretTakedowns', 0),
                        visionScorePerMinute = participant.get("challenges").get('visionScorePerMinute', 0),
                        wardTakedowns = participant.get("challenges").get('wardTakedowns', 0),
                        wardTakedownsBefore20M = participant.get("challenges").get('wardTakedownsBefore20M', 0),
                        wardsGuarded = participant.get("challenges").get('wardsGuarded', 0),
                        
                        championName = participant.get('championName', ''),
                        detectorWardsPlaced = participant.get('detectorWardsPlaced', 0),
                        deaths = participant.get('deaths', 0),
                        doubleKills = participant.get('doubleKills', 0),
                        kills = participant.get('kills', 0),
                        puuid = participant.get('puuid', ''),
                        timePlayed = participant.get('timePlayed', 0),
                        tripleKills = participant.get('tripleKills', 0),
                        totalDamageDealt = participant.get('totalDamageDealt', 0),
                        totalDamageDealtToChampions = participant.get('totalDamageDealtToChampions', 0),
                        totalDamageTaken = participant.get('totalDamageTaken', 0),
                        win = participant.get('win', False),
                        teamId = participant.get('teamId', 0),
                        teamPosition = participant.get('teamPosition', ''),
                        participantId = participant.get('participantId', -1),
                        champExperience = participant.get('champExperience', 0),
                        champLevel = participant.get('champLevel', 0),
                        championId = participant.get('championId', 0),

                        # totalDamageDealt / totalDamageTaken 
                        dpt = participant.get('totalDamageDealt', 0.0001) / participant.get('totalDamageTaken', 0.0001),
                        # damagePerMinute / goldPerMinute 
                        dpg = participant.get("challenges").get('damagePerMinute', 0.0001) / participant.get("challenges").get('goldPerMinute', 0.0001),
                        # totalTimeSpentDead / timePlayed
                        ddpt = participant.get('totalTimeSpentDead', 0.0001) / participant.get('timePlayed', 0.0001),
                        # skillshotsDodged / timePlayed
                        dgpt = participant.get("challenges").get('skillshotsDodged', 0.0001) / participant.get('timePlayed', 0.0001),
                                        )
                    # 데이터베이스에 저장합니다.
                    par_entry.save()
                    print("Participant saved successfully {}".format(participant.get('puuid', '')))
        else:
            participants = info.get('participants', []) # lst
            for participant in participants:
                # 참가자 정보가 이미 존재하는지 확인합니다.
                try:
                    par_entry = Participant.objects.get(user_match=match, puuid=participant.get('puuid', ''))
                except Participant.DoesNotExist:
                    par_entry = Participant.objects.create(
                        user_match = match,
                        assists = participant.get('assists', 0),
                        bountyGold = participant.get("challenges").get('bountyGold', 0),
                        controlWardsPlaced = participant.get("challenges").get('controlWardsPlaced', 0),
                        damagePerMinute = participant.get("challenges").get('damagePerMinute', 0),
                        damageTakenOnTeamPercentage = participant.get("challenges").get('damageTakenOnTeamPercentage', 0),
                        deathsByEnemyChamps =  participant.get("challenges").get('deathsByEnemyChamps', 0),
                        earlyLaningPhaseGoldExpAdvantage = participant.get("challenges").get('earlyLaningPhaseGoldExpAdvantage', 0),
                        epicMonsterKillsNearEnemyJungler = participant.get("challenges").get('epicMonsterKillsNearEnemyJungler', 0),
                        epicMonsterSteals = participant.get("challenges").get('epicMonsterSteals', 0),
                        epicMonsterStolenWithoutSmite = participant.get("challenges").get('epicMonsterStolenWithoutSmite', 0),
                        firstTurretKilled = participant.get("challenges").get('firstTurretKilled', False),
                        firstTurretKilledTime = participant.get("challenges").get('firstTurretKilledTime', 0),
                        gameLength = participant.get("challenges").get('gameLength', 0),
                        goldPerMinute = participant.get("challenges").get('goldPerMinute', 0),
                        immobilizeAndKillWithAlly = participant.get("challenges").get('immobilizeAndKillWithAlly', 0),
                        initialBuffCount = participant.get("challenges").get('initialBuffCount', 0),
                        initialCrabCount = participant.get("challenges").get('initialCrabCount', 0),
                        jungleCsBefore10Minutes = participant.get("challenges").get('jungleCsBefore10Minutes', 0),
                        kTurretsDestroyedBeforePlatesFall = participant.get("challenges").get('kTurretsDestroyedBeforePlatesFall', 0),
                        kda = participant.get("challenges").get('kda', 0),
                        killAfterHiddenWithAlly = participant.get("challenges").get('killAfterHiddenWithAlly', 0),
                        killParticipation = participant.get("challenges").get('killParticipation', 0),
                        killingSprees = participant.get('killingSprees', 0),
                        killsNearEnemyTurret = participant.get("challenges").get('killsNearEnemyTurret', 0),
                        killsOnOtherLanesEarlyJungleAsLaner = participant.get("challenges").get('killsOnOtherLanesEarlyJungleAsLaner', 0),
                        killsUnderOwnTurret = participant.get("challenges").get('killsUnderOwnTurret', 0),
                        knockEnemyIntoTeamAndKill = participant.get("challenges").get('knockEnemyIntoTeamAndKill', 0),
                        laneMinionsFirst10Minutes = participant.get("challenges").get('laneMinionsFirst10Minutes', 0),
                        laningPhaseGoldExpAdvantage = participant.get("challenges").get('laningPhaseGoldExpAdvantage', 0),
                        legendaryCount = participant.get("challenges").get('legendaryCount', 0),
                        maxCsAdvantageOnLaneOpponent = participant.get("challenges").get('maxCsAdvantageOnLaneOpponent', 0),
                        maxLevelLeadLaneOpponent = participant.get("challenges").get('maxLevelLeadLaneOpponent', 0),
                        moreEnemyJungleThanOpponent = participant.get("challenges").get('moreEnemyJungleThanOpponent', 0),
                        multikills = participant.get("challenges").get('multikills', 0),
                        multikillsAfterAggressiveFlash = participant.get("challenges").get('multikillsAfterAggressiveFlash', 0),
                        outerTurretExecutesBefore10Minutes = participant.get("challenges").get('outerTurretExecutesBefore10Minutes', 0),
                        outnumberedKills = participant.get("challenges").get('outnumberedKills', 0),
                        scuttleCrabKills = participant.get("challenges").get('scuttleCrabKills', 0),
                        skillshotsDodged = participant.get("challenges").get('skillshotsDodged', 0),
                        soloKills = participant.get("challenges").get('soloKills', 0),
                        stealthWardsPlaced = participant.get("challenges").get('stealthWardsPlaced', 0),
                        takedownOnFirstTurret = participant.get("challenges").get('takedownOnFirstTurret', 0),
                        takedowns = participant.get("challenges").get('takedowns', 0),
                        takedownsFirstXMinutes = participant.get("challenges").get('takedownsFirstXMinutes', 0),
                        teamDamagePercentage = participant.get("challenges").get('teamDamagePercentage', 0),
                        teleportTakedowns = participant.get("challenges").get('teleportTakedowns', 0),
                        turretPlatesTaken = participant.get("challenges").get('turretPlatesTaken', 0),
                        turretTakedowns = participant.get("challenges").get('turretTakedowns', 0),
                        visionScorePerMinute = participant.get("challenges").get('visionScorePerMinute', 0),
                        wardTakedowns = participant.get("challenges").get('wardTakedowns', 0),
                        wardTakedownsBefore20M = participant.get("challenges").get('wardTakedownsBefore20M', 0),
                        wardsGuarded = participant.get("challenges").get('wardsGuarded', 0),
                        
                        championName = participant.get('championName', ''),
                        detectorWardsPlaced = participant.get('detectorWardsPlaced', 0),
                        deaths = participant.get('deaths', 0),
                        doubleKills = participant.get('doubleKills', 0),
                        kills = participant.get('kills', 0),
                        puuid = participant.get('puuid', ''),
                        timePlayed = participant.get('timePlayed', 0),
                        tripleKills = participant.get('tripleKills', 0),
                        totalDamageDealt = participant.get('totalDamageDealt', 0),
                        totalDamageDealtToChampions = participant.get('totalDamageDealtToChampions', 0),
                        totalDamageTaken = participant.get('totalDamageTaken', 0),
                        win = participant.get('win', False),
                        teamId = participant.get('teamId', 0),
                        teamPosition = participant.get('teamPosition', ''),
                        participantId = participant.get('participantId', -1),
                        champExperience = participant.get('champExperience', 0),
                        champLevel = participant.get('champLevel', 0),
                        championId = participant.get('championId', 0),
                        
                        # totalDamageDealt / totalDamageTaken 
                        dpt = participant.get('totalDamageDealt', 0.0001) / participant.get('totalDamageTaken', 0.0001),
                        # damagePerMinute / goldPerMinute 
                        dpg = participant.get("challenges").get('damagePerMinute', 0.0001) / participant.get("challenges").get('goldPerMinute', 0.0001),
                        # totalTimeSpentDead / timePlayed
                        ddpt = participant.get('totalTimeSpentDead', 0.0001) / participant.get('timePlayed', 0.0001),
                        # skillshotsDodged / timePlayed
                        dgpt = participant.get("challenges").get('skillshotsDodged', 0.0001) / participant.get('timePlayed', 0.0001),
                                        )
                    # 데이터베이스에 저장합니다.
                    par_entry.save()
                    print("Participant saved successfully {}".format(participant.get('puuid', '')))
import requests
import json
import time
import pandas as pd
from tqdm import tqdm
from .models import UserMatch, Participant, ParticipantCompare
from rest_framework.response import Response
from django.db.models import Q, F, Sum
from rest_framework import status
API_KEY = "RGAPI-7d629a47-b1ff-4d8a-91d8-dc6319c2e854s"
class RiotAPI:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.header = {"X-Riot-Token": API_KEY
                       }

    def get_puuid_from_summonerName(self, summonerName):
        url = "https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
        # ex) 용 엣#KR1 -> 용엣 + # + KR1
        name = summonerName.split('#')[0]
        tag = summonerName.split('#')[1]
        url_f = str(url+name+'/'+tag)
        response = requests.get(url_f, headers=self.header)
        return response.json()['puuid']
    
    def get_summonerId_from_puuid(self, encryptedPUUID):
        url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}"
        response = requests.get(url, headers=self.header)
        return response.json()['id']
    
    def get_matchid_lst_from_puuid(self, puuid):
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?"
        option = 'type=ranked&start=0&count=100'
        url_f = url + option
        response = requests.get(url_f, headers=self.header)
        return response.json()
    
    def get_matchid_lst_from_puuid_2(self, puuid, start, count, endTime=None):
        # 현재 에폭 시간
        if endTime == None:
            endTime = int(time.time() * 1000)

        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?"
        option = 'type=ranked&start='+str(start)+'&count='+str(count)+'&endTime='+str(endTime)
        url_f = url + option
        response = requests.get(url_f, headers=self.header)
        return response.json()
    
    def get_match_matchId(self, matchId):
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}"
        response = requests.get(url, headers=self.header)
        return response.json()

    def get_match_Full(self, summonerName):
        puuid = self.get_puuid_from_summonerName(summonerName)
        summonerId = self.get_summonerId_from_puuid(puuid)
        league = self.get_league(summonerId)
        for item in league:
            if item.get('queueType') == 'RANKED_SOLO_5x5':
                league = item
                break
        total = int(league.get('wins') + league.get('losses'))
        matchid_lst = []
        last_match_time = None
        start = 0
        while total != 0:
            if total <= 100:
                matchid_lst_tmp = self.get_matchid_lst_from_puuid_2(puuid, start, total, last_match_time)
                matchid_lst.extend(matchid_lst_tmp)
                start = start + total
                total = 0
            else:
                matchid_lst_tmp = self.get_matchid_lst_from_puuid_2(puuid, start, 100, last_match_time)
                # 마지막 매치의 시간 확인
                last_match_100 = self.get_match_matchId(matchid_lst_tmp[-1])
                last_match_time = last_match_100.get('info').get('gameEndTimestamp')
                matchid_lst.extend(matchid_lst_tmp)
                start = start + 100
                total = total - 100
        matchid_lst_f = []
        for i in matchid_lst:
            try:
                UserMatch.objects.get(match_id=i)
                matchid_lst.remove(i)
            except:
                matchid_lst_f.append(i)


        match_lst = []
        for matchId in tqdm(matchid_lst_f):
            match_lst.append(self.get_match_matchId(matchId))
            time.sleep(1)
        
        # 100전 이상의 경우
        summonerId = self.get_summonerId_from_puuid(puuid)
        obj = self.get_league(summonerId)

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
        print(response.json())
        return response.json()
    
    def get_league(self, summonerId):
        url = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerId}"
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


class NewStats:
    def __init__(self, participant):
        self.participant = participant

    def dpt(self):
        if self.participant.get('totalDamageTaken', 0) == 0:
            return -1
        else:
            return self.participant.get('totalDamageDealt', 0) / self.participant.get('totalDamageTaken', 0)
        
    def dpg(self):
        if self.participant.get("challenges").get('goldPerMinute', 0) == 0:
            return -1
        else:
            return self.participant.get("challenges").get('damagePerMinute', 0) / self.participant.get("challenges").get('goldPerMinute', 0)
    def ddpt(self):
        if self.participant.get('timePlayed', 0) == 0:
            return -1
        else:
            return self.participant.get('totalTimeSpentDead', 0) / self.participant.get('timePlayed', 0)
    def dgpt(self):
        if self.participant.get('timePlayed', 0) == 0:
            return -1
        else:
            return self.participant.get("challenges").get('skillshotsDodged', 0) / self.participant.get('timePlayed', 0)
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
                new_stats = NewStats(participant)
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
                        dpt = new_stats.dpt(),
                        # damagePerMinute / goldPerMinute 
                        dpg = new_stats.dpg(),
                        # totalTimeSpentDead / timePlayed
                        ddpt = new_stats.ddpt(),
                        # skillshotsDodged / timePlayed
                        dgpt = new_stats.dgpt(),
                        totalPings=(
                            participant.get('allInPings', 0) +
                            participant.get('assistMePings', 0) +
                            participant.get('basicPings', 0) +
                            participant.get('commandPings', 0) +
                            participant.get('dangerPings', 0) +
                            participant.get('enemyMissingPings', 0) +
                            participant.get('enemyVisionPings', 0) +
                            participant.get('getBackPings', 0) +
                            participant.get('holdPings', 0) +
                            participant.get('needVisionPings', 0) +
                            participant.get('onMyWayPings', 0) +
                            participant.get('pushPings', 0) +
                            participant.get('visionClearedPings', 0)
                        ),
                        item0 = participant.get('item0', 0),
                        item1 = participant.get('item1', 0),
                        item2 = participant.get('item2', 0),
                        item3 = participant.get('item3', 0),
                        item4 = participant.get('item4', 0),
                        item5 = participant.get('item5', 0),
                        item6 = participant.get('item6', 0),
                        spell1Casts = participant.get('spell1Casts', 0),
                        spell2Casts = participant.get('spell2Casts', 0),
                        spell3Casts = participant.get('spell3Casts', 0),
                        spell4Casts = participant.get('spell4Casts', 0),
                        summoner1Casts = participant.get('summoner1Casts', 0),
                        summoner1Id = participant.get('summoner1Id', 0),
                        summoner2Casts = participant.get('summoner2Casts', 0),
                        summoner2Id = participant.get('summoner2Id', 0),

                                        )
                    # 데이터베이스에 저장합니다.
                    par_entry.save()
                    print("Participant saved successfully {}".format(participant.get('puuid', '')))
            ## 비교 스텟 추가
            for participant in participants:
                par_entry = Participant.objects.get(user_match=match, puuid=participant.get('puuid', ''))
                compare_ins = CreateStatsCompared(par_entry)
                try:
                    par_compare_entry = ParticipantCompare.objects.get(participant=par_entry)
                except ParticipantCompare.DoesNotExist:
                    par_compare_entry = ParticipantCompare.objects.create(
                        participant = par_entry,
                        damagePerMinuteOppo = compare_ins.damagePerMinuteOppo,
                        damagePerMinuteRank = compare_ins.damagePerMinuteRank,
                        bountyGoldOppo = compare_ins.bountyGoldOppo,
                        bountyGoldRank = compare_ins.bountyGoldRank,
                        dptOppo = compare_ins.dptOppo,
                        dptRank = compare_ins.dptRank,
                        dpgOppo = compare_ins.dpgOppo,
                        dpgRank = compare_ins.dpgRank,
                        ddptOppo = compare_ins.ddptOppo,
                        ddptRank = compare_ins.ddptRank,
                        dgptOppo = compare_ins.dgptOppo,
                        dgptRank = compare_ins.dgptRank,
                        turretPlatesTakenOppo = compare_ins.turretPlatesTakenOppo,
                        turretPlatesTakenRank = compare_ins.turretPlatesTakenRank,
                        killAfterHiddenWithAllyOppo = compare_ins.killAfterHiddenWithAllyOppo,
                        killAfterHiddenWithAllyRank = compare_ins.killAfterHiddenWithAllyRank,
                        takedownsFirstXMinutesOppo = compare_ins.takedownsFirstXMinutesOppo,
                        takedownsFirstXMinutesRank = compare_ins.takedownsFirstXMinutesRank,
                        laneMinionsFirst10MinutesOppo = compare_ins.laneMinionsFirst10MinutesOppo,
                        laneMinionsFirst10MinutesRank = compare_ins.laneMinionsFirst10MinutesRank,
                        killsNearTurret = compare_ins.killsNearTurret,
                        killsNearTurretOppo = compare_ins.killsNearTurretOppo,
                        killsNearTurretRank = compare_ins.killsNearTurretRank,
                        outnumberedKillsOppo = compare_ins.outnumberedKillsOppo,
                        outnumberedKillsRank = compare_ins.outnumberedKillsRank,
                        moreEnemyJungleThanOpponentOppo = compare_ins.moreEnemyJungleThanOpponentOppo,
                        moreEnemyJungleThanOpponentRank = compare_ins.moreEnemyJungleThanOpponentRank,
                        visionScorePerMinuteOppo = compare_ins.visionScorePerMinuteOppo,
                        visionScorePerMinuteRank = compare_ins.visionScorePerMinuteRank,
                        totalPingsOppo = compare_ins.totalPingsOppo,
                        totalPingsRank = compare_ins.totalPingsRank,
                        myTeamPings = compare_ins.myTeamPings,
                        myTeamPingsOppo = compare_ins.myTeamPingsOppo,
                    )
                    par_compare_entry.save()
                else:
                    par_entry.participant = par_entry,
                    par_entry.damagePerMinuteOppo = compare_ins.damagePerMinuteOppo,
                    par_entry.damagePerMinuteRank = compare_ins.damagePerMinuteRank,
                    par_entry.bountyGoldOppo = compare_ins.bountyGoldOppo,
                    par_entry.bountyGoldRank = compare_ins.bountyGoldRank,
                    par_entry.dptOppo = compare_ins.dptOppo,
                    par_entry.dptRank = compare_ins.dptRank,
                    par_entry.dpgOppo = compare_ins.dpgOppo,
                    par_entry.dpgRank = compare_ins.dpgRank,
                    par_entry.ddptOppo = compare_ins.ddptOppo,
                    par_entry.ddptRank = compare_ins.ddptRank,
                    par_entry.dgptOppo = compare_ins.dgptOppo,
                    par_entry.dgptRank = compare_ins.dgptRank,
                    par_entry.turretPlatesTakenOppo = compare_ins.turretPlatesTakenOppo,
                    par_entry.turretPlatesTakenRank = compare_ins.turretPlatesTakenRank,
                    par_entry.killAfterHiddenWithAllyOppo = compare_ins.killAfterHiddenWithAllyOppo,
                    par_entry.killAfterHiddenWithAllyRank = compare_ins.killAfterHiddenWithAllyRank,
                    par_entry.takedownsFirstXMinutesOppo = compare_ins.takedownsFirstXMinutesOppo,
                    par_entry.takedownsFirstXMinutesRank = compare_ins.takedownsFirstXMinutesRank,
                    par_entry.laneMinionsFirst10MinutesOppo = compare_ins.laneMinionsFirst10MinutesOppo,
                    par_entry.laneMinionsFirst10MinutesRank = compare_ins.laneMinionsFirst10MinutesRank,
                    par_entry.killsNearTurret = compare_ins.killsNearTurret,
                    par_entry.killsNearTurretOppo = compare_ins.killsNearTurretOppo,
                    par_entry.killsNearTurretRank = compare_ins.killsNearTurretRank,
                    par_entry.outnumberedKillsOppo = compare_ins.outnumberedKillsOppo,
                    par_entry.outnumberedKillsRank = compare_ins.outnumberedKillsRank,
                    par_entry.moreEnemyJungleThanOpponentOppo = compare_ins.moreEnemyJungleThanOpponentOppo,
                    par_entry.moreEnemyJungleThanOpponentRank = compare_ins.moreEnemyJungleThanOpponentRank,
                    par_entry.visionScorePerMinuteOppo = compare_ins.visionScorePerMinuteOppo,
                    par_entry.visionScorePerMinuteRank = compare_ins.visionScorePerMinuteRank,
                    par_entry.totalPingsOppo = compare_ins.totalPingsOppo,
                    par_entry.totalPingsRank = compare_ins.totalPingsRank,
                    par_entry.myTeamPings = compare_ins.myTeamPings,
                    par_entry.myTeamPingsOppo = compare_ins.myTeamPingsOppo

                    par_compare_entry.save()
                print("ParticipantCompare saved successfully {}".format(participant.get('puuid', '')))

        else:
            participants = info.get('participants', []) # lst
            for participant in participants:
                new_stats = NewStats(participant)
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
                        # pings
                        totalPings=(
                            participant.get('allInPings', 0) +
                            participant.get('assistMePings', 0) +
                            participant.get('basicPings', 0) +
                            participant.get('commandPings', 0) +
                            participant.get('dangerPings', 0) +
                            participant.get('enemyMissingPings', 0) +
                            participant.get('enemyVisionPings', 0) +
                            participant.get('getBackPings', 0) +
                            participant.get('holdPings', 0) +
                            participant.get('needVisionPings', 0) +
                            participant.get('onMyWayPings', 0) +
                            participant.get('pushPings', 0) +
                            participant.get('visionClearedPings', 0)
                        ),
                        # totalDamageDealt / totalDamageTaken 
                        dpt = new_stats.dpt(),
                        # damagePerMinute / goldPerMinute 
                        dpg = new_stats.dpg(),
                        # totalTimeSpentDead / timePlayed
                        ddpt = new_stats.ddpt(),
                        # skillshotsDodged / timePlayed
                        dgpt = new_stats.dgpt(),
                        item0 = participant.get('item0', 0),
                        item1 = participant.get('item1', 0),
                        item2 = participant.get('item2', 0),
                        item3 = participant.get('item3', 0),
                        item4 = participant.get('item4', 0),
                        item5 = participant.get('item5', 0),
                        item6 = participant.get('item6', 0),
                        spell1Casts = participant.get('spell1Casts', 0),
                        spell2Casts = participant.get('spell2Casts', 0),
                        spell3Casts = participant.get('spell3Casts', 0),
                        spell4Casts = participant.get('spell4Casts', 0),
                        summoner1Casts = participant.get('summoner1Casts', 0),
                        summoner1Id = participant.get('summoner1Id', 0),
                        summoner2Casts = participant.get('summoner2Casts', 0),
                        summoner2Id = participant.get('summoner2Id', 0),
                                        )
                    # 데이터베이스에 저장합니다.
                    par_entry.save()
                    print("Participant saved successfully {}".format(participant.get('puuid', '')))
                        ## 비교 스텟 추가
            for participant in participants:
                par_entry = Participant.objects.get(user_match=match, puuid=participant.get('puuid', ''))
                compare_ins = CreateStatsCompared(par_entry)
                try:
                    par_compare_entry = ParticipantCompare.objects.get(participant=par_entry)
                except ParticipantCompare.DoesNotExist:
                    par_compare_entry = ParticipantCompare.objects.create(
                        participant = par_entry,
                        damagePerMinuteOppo = compare_ins.damagePerMinuteOppo,
                        damagePerMinuteRank = compare_ins.damagePerMinuteRank,
                        bountyGoldOppo = compare_ins.bountyGoldOppo,
                        bountyGoldRank = compare_ins.bountyGoldRank,
                        dptOppo = compare_ins.dptOppo,
                        dptRank = compare_ins.dptRank,
                        dpgOppo = compare_ins.dpgOppo,
                        dpgRank = compare_ins.dpgRank,
                        ddptOppo = compare_ins.ddptOppo,
                        ddptRank = compare_ins.ddptRank,
                        dgptOppo = compare_ins.dgptOppo,
                        dgptRank = compare_ins.dgptRank,
                        turretPlatesTakenOppo = compare_ins.turretPlatesTakenOppo,
                        turretPlatesTakenRank = compare_ins.turretPlatesTakenRank,
                        killAfterHiddenWithAllyOppo = compare_ins.killAfterHiddenWithAllyOppo,
                        killAfterHiddenWithAllyRank = compare_ins.killAfterHiddenWithAllyRank,
                        takedownsFirstXMinutesOppo = compare_ins.takedownsFirstXMinutesOppo,
                        takedownsFirstXMinutesRank = compare_ins.takedownsFirstXMinutesRank,
                        laneMinionsFirst10MinutesOppo = compare_ins.laneMinionsFirst10MinutesOppo,
                        laneMinionsFirst10MinutesRank = compare_ins.laneMinionsFirst10MinutesRank,
                        killsNearTurret = compare_ins.killsNearTurret,
                        killsNearTurretOppo = compare_ins.killsNearTurretOppo,
                        killsNearTurretRank = compare_ins.killsNearTurretRank,
                        outnumberedKillsOppo = compare_ins.outnumberedKillsOppo,
                        outnumberedKillsRank = compare_ins.outnumberedKillsRank,
                        moreEnemyJungleThanOpponentOppo = compare_ins.moreEnemyJungleThanOpponentOppo,
                        moreEnemyJungleThanOpponentRank = compare_ins.moreEnemyJungleThanOpponentRank,
                        visionScorePerMinuteOppo = compare_ins.visionScorePerMinuteOppo,
                        visionScorePerMinuteRank = compare_ins.visionScorePerMinuteRank,
                        totalPingsOppo = compare_ins.totalPingsOppo,
                        totalPingsRank = compare_ins.totalPingsRank,
                        myTeamPings = compare_ins.myTeamPings,
                        myTeamPingsOppo = compare_ins.myTeamPingsOppo,
                    )
                    par_compare_entry.save()
                else:
                    par_entry.participant = par_entry,
                    par_entry.damagePerMinuteOppo = compare_ins.damagePerMinuteOppo,
                    par_entry.damagePerMinuteRank = compare_ins.damagePerMinuteRank,
                    par_entry.bountyGoldOppo = compare_ins.bountyGoldOppo,
                    par_entry.bountyGoldRank = compare_ins.bountyGoldRank,
                    par_entry.dptOppo = compare_ins.dptOppo,
                    par_entry.dptRank = compare_ins.dptRank,
                    par_entry.dpgOppo = compare_ins.dpgOppo,
                    par_entry.dpgRank = compare_ins.dpgRank,
                    par_entry.ddptOppo = compare_ins.ddptOppo,
                    par_entry.ddptRank = compare_ins.ddptRank,
                    par_entry.dgptOppo = compare_ins.dgptOppo,
                    par_entry.dgptRank = compare_ins.dgptRank,
                    par_entry.turretPlatesTakenOppo = compare_ins.turretPlatesTakenOppo,
                    par_entry.turretPlatesTakenRank = compare_ins.turretPlatesTakenRank,
                    par_entry.killAfterHiddenWithAllyOppo = compare_ins.killAfterHiddenWithAllyOppo,
                    par_entry.killAfterHiddenWithAllyRank = compare_ins.killAfterHiddenWithAllyRank,
                    par_entry.takedownsFirstXMinutesOppo = compare_ins.takedownsFirstXMinutesOppo,
                    par_entry.takedownsFirstXMinutesRank = compare_ins.takedownsFirstXMinutesRank,
                    par_entry.laneMinionsFirst10MinutesOppo = compare_ins.laneMinionsFirst10MinutesOppo,
                    par_entry.laneMinionsFirst10MinutesRank = compare_ins.laneMinionsFirst10MinutesRank,
                    par_entry.killsNearTurret = compare_ins.killsNearTurret,
                    par_entry.killsNearTurretOppo = compare_ins.killsNearTurretOppo,
                    par_entry.killsNearTurretRank = compare_ins.killsNearTurretRank,
                    par_entry.outnumberedKillsOppo = compare_ins.outnumberedKillsOppo,
                    par_entry.outnumberedKillsRank = compare_ins.outnumberedKillsRank,
                    par_entry.moreEnemyJungleThanOpponentOppo = compare_ins.moreEnemyJungleThanOpponentOppo,
                    par_entry.moreEnemyJungleThanOpponentRank = compare_ins.moreEnemyJungleThanOpponentRank,
                    par_entry.visionScorePerMinuteOppo = compare_ins.visionScorePerMinuteOppo,
                    par_entry.visionScorePerMinuteRank = compare_ins.visionScorePerMinuteRank,
                    par_entry.totalPingsOppo = compare_ins.totalPingsOppo,
                    par_entry.totalPingsRank = compare_ins.totalPingsRank,
                    par_entry.myTeamPings = compare_ins.myTeamPings,
                    par_entry.myTeamPingsOppo = compare_ins.myTeamPingsOppo

                    par_compare_entry.save()
                print("ParticipantCompare saved successfully {}".format(participant.get('puuid', '')))

class CreateStatsCompared:
    def __init__(self, par_entry):
        self.par_entry = par_entry
        self.user_match_id = par_entry.user_match_id
        self.get_oppo()
        self.get_with_match_participant()
        self.DamagePerMinute()
        self.BountyGold()
        self.Dpg()
        self.Dpt()
        self.TurretPlatesTaken()
        self.KillAfterHiddenWithAlly()
        self.TakedownsFirstXMinutes()
        self.LaneMinionsFirst10Minutes()
        self.Ddpt()
        self.Dgpt()
        self.KillsNearTurret()
        self.OutnumberedKills()
        self.MoreEnemyJungleThanOpponent()
        self.VisionScorePerMinute()
        self.Pings()


    def get_oppo(self):
        self.oppo = Participant.objects.filter(
            user_match=self.user_match_id,
            teamPosition=self.par_entry.teamPosition
            ).exclude(id=self.par_entry.id)
        self.oppo = self.oppo.get()
    def get_with_match_participant(self):
        self.match_player = Participant.objects.filter(
            user_match=self.user_match_id
            )
    def DamagePerMinute(self):
        dpm_my = self.par_entry.damagePerMinute
        higher_count = self.match_player.filter(damagePerMinute__gt=dpm_my).count()
        rank = higher_count + 1

        if dpm_my != 0:
            self.damagePerMinuteOppo = ((
                dpm_my - self.oppo.damagePerMinute ) / dpm_my)
        else:
            self.damagePerMinuteOppo = -1
        self.damagePerMinuteRank = rank

    def BountyGold(self):
        bounty_gold_my = self.par_entry.bountyGold
        higher_count = self.match_player.filter(bountyGold__gt=bounty_gold_my).count()
        rank = higher_count + 1

        self.bountyGoldOppo = (
            bounty_gold_my - self.oppo.bountyGold 
        )
        self.bountyGoldRank = rank

    def Dpg(self):
        dpg_my = self.par_entry.dpg
        higher_count = self.match_player.filter(dpg__gt=dpg_my).count()
        rank = higher_count + 1

        if dpg_my != 0:
            self.dpgOppo = ((
                dpg_my - self.oppo.dpg
            ) / dpg_my)
        else:
            self.dpgOppo = -1
        self.dpgRank = rank
    
    def Dpt(self):
        dpt_my = self.par_entry.dpt
        higher_count = self.match_player.filter(dpt__gt=dpt_my).count()
        rank = higher_count + 1

        if dpt_my != 0:
            self.dptOppo = ((
                dpt_my - self.oppo.dpt
            ) / dpt_my)
        else:
            self.dptOppo = -1
        self.dptRank = rank

    def TurretPlatesTaken(self):
        turretPlatesTaken_my = self.par_entry.turretPlatesTaken
        higher_count = self.match_player.filter(turretPlatesTaken__gt=turretPlatesTaken_my).count()
        rank = higher_count + 1

        self.turretPlatesTakenOppo = (
            turretPlatesTaken_my - self.oppo.turretPlatesTaken
        )
        self.turretPlatesTakenRank = rank

    def KillsNearTurret(self):
        killsNearTurret_my = self.par_entry.killsNearEnemyTurret + (1.5)*self.par_entry.killsUnderOwnTurret
        killsNearTurret_Oppo = self.oppo.killsNearEnemyTurret + (1.5)*self.oppo.killsUnderOwnTurret

        match_player_annotated = self.match_player.annotate(
        killsNearTurret=F('killsNearEnemyTurret') + (1.5)*F('killsUnderOwnTurret')
        )

        higher_count = match_player_annotated.filter(killsNearTurret__gt=killsNearTurret_my).count()

        rank = higher_count + 1

        self.killsNearTurretOppo = (
            killsNearTurret_my - killsNearTurret_Oppo
        )
        self.killsNearTurretRank = rank
        self.killsNearTurret = killsNearTurret_my
        
    def TakedownsFirstXMinutes(self):
        takedownsFirstXMinutes_my = self.par_entry.takedownsFirstXMinutes
        higher_count = self.match_player.filter(takedownsFirstXMinutes__gt=takedownsFirstXMinutes_my).count()
        rank = higher_count + 1

        self.takedownsFirstXMinutesOppo = (
            takedownsFirstXMinutes_my - self.oppo.takedownsFirstXMinutes
        )
        self.takedownsFirstXMinutesRank = rank

    def LaneMinionsFirst10Minutes(self):
        laneMinionsFirst10Minutes_my = self.par_entry.laneMinionsFirst10Minutes
        higher_count = self.match_player.filter(laneMinionsFirst10Minutes__gt=laneMinionsFirst10Minutes_my).count()
        rank = higher_count + 1

        self.laneMinionsFirst10MinutesOppo = (
            laneMinionsFirst10Minutes_my - self.oppo.laneMinionsFirst10Minutes
        )
        self.laneMinionsFirst10MinutesRank = rank

    def Ddpt(self):
        ddpt_my = self.par_entry.ddpt
        higher_count = self.match_player.filter(ddpt__gt=ddpt_my).count()
        rank = higher_count + 1
        if ddpt_my != 0:
            self.ddptOppo = ((
                ddpt_my - self.oppo.ddpt
            ) / ddpt_my)
        else:
            self.ddptOppo = -1
        self.ddptRank = rank
    
    def Dgpt(self):
        dgpt_my = self.par_entry.dgpt
        higher_count = self.match_player.filter(dgpt__gt=dgpt_my).count()
        rank = higher_count + 1

        if dgpt_my != 0:
            self.dgptOppo = ((
                dgpt_my - self.oppo.dgpt
            ) / dgpt_my)
        else:
            self.dgptOppo = -1
        self.dgptRank = rank

    def KillAfterHiddenWithAlly(self):
        killAfterHiddenWithAlly_my = self.par_entry.killAfterHiddenWithAlly
        higher_count = self.match_player.filter(killAfterHiddenWithAlly__gt=killAfterHiddenWithAlly_my).count()
        rank = higher_count + 1

        self.killAfterHiddenWithAllyOppo = (
            killAfterHiddenWithAlly_my - self.oppo.killAfterHiddenWithAlly
        )
        self.killAfterHiddenWithAllyRank = rank
    
    def OutnumberedKills(self):
        outnumberedKills_my = self.par_entry.outnumberedKills
        higher_count = self.match_player.filter(outnumberedKills__gt=outnumberedKills_my).count()
        rank = higher_count + 1

        self.outnumberedKillsOppo = (
            outnumberedKills_my - self.oppo.outnumberedKills
        )
        self.outnumberedKillsRank = rank
    
    def MoreEnemyJungleThanOpponent(self):
        moreEnemyJungleThanOpponent_my = self.par_entry.moreEnemyJungleThanOpponent
        higher_count = self.match_player.filter(moreEnemyJungleThanOpponent__gt=moreEnemyJungleThanOpponent_my).count()
        rank = higher_count + 1

        self.moreEnemyJungleThanOpponentOppo = (
            moreEnemyJungleThanOpponent_my - self.oppo.moreEnemyJungleThanOpponent
        )
        self.moreEnemyJungleThanOpponentRank = rank
    
    def VisionScorePerMinute(self):
        visionScorePerMinute_my = self.par_entry.visionScorePerMinute
        higher_count = self.match_player.filter(visionScorePerMinute__gt=visionScorePerMinute_my).count()
        rank = higher_count + 1

        if visionScorePerMinute_my != 0:
            self.visionScorePerMinuteOppo = ((
                visionScorePerMinute_my - self.oppo.visionScorePerMinute
            ) / visionScorePerMinute_my)
        else:
            self.visionScorePerMinuteOppo = -1
        self.visionScorePerMinuteRank = rank
    

    def Pings(self):
        pings_my = self.par_entry.totalPings
        higher_count = self.match_player.filter(totalPings__gt=pings_my).count()
        rank = higher_count + 1
        my_teamId = self.par_entry.teamId
        if my_teamId == 100:
            oppo_teamId = 200
        else:
            oppo_teamId = 100

        my_team = self.match_player.filter(teamId=my_teamId)
        oppo_team = self.match_player.filter(teamId=oppo_teamId)

        my_team_total_pings = my_team.aggregate(total_pings_sum=Sum('totalPings'))['total_pings_sum']
        oppo_team_total_pings = oppo_team.aggregate(total_pings_sum=Sum('totalPings'))['total_pings_sum']

        self.totalPingsOppo = (
            pings_my - self.oppo.totalPings
        )
        self.totalPingsRank = rank

        self.myTeamPings = my_team_total_pings
        
        if my_team_total_pings != 0:
            self.myTeamPingsOppo = (my_team_total_pings - oppo_team_total_pings)/my_team_total_pings
        else:
            self.myTeamPingsOppo = -1
        
def get_mvp(damagePerMinute):
    if damagePerMinute >= 800:
        return True
    else:
        return False
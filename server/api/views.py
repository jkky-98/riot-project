from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ModelRefreshToken, UserRiot, Participant, UserMatch, ParticipantCompare
from .auth import auth
from .riotAPI import RiotAPI, update_matches, get_mvp
import json
from django.db.models import Count, Avg, Q, Sum, F

### Riot API ###
RIOTAPIKEY = "RGAPI-e512b66f-810a-4b24-85df-80f8fb6cee86"
def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"파일 '{file_path}'을(를) 찾을 수 없습니다.")
        return None
class SignUpView(APIView):
    def post(self, request):
        # 사용자 입력값 가져오기
        userId = request.data.get('userId')
        userPassword = request.data.get('userPassword')
        email = request.data.get('email', '')  # 이메일이 없는 경우 빈 문자열로 처리

        # 입력값 유효성 검사
        if not userId or not userPassword:
            return Response({'error': 'userId와 userPassword는 필수 입력값입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 아이디 중복성 검사
        
        if User.objects.filter(username=userId).exists():
            return Response({'error': '이미 존재하는 아이디입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        

        # 새로운 사용자 생성 및 저장
        try:
            user = User.objects.create_user(username=userId, email=email, password=userPassword)
            return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LoginView(APIView):
    def post(self, request):
        # 사용자 입력값 가져오기
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        # 사용자 인증
        user = authenticate(username=username, email=email, password=password )
        if user is not None:
            # 사용자 인증 성공시 리프레시 토큰 생성
            # rest_framework_simplejwt에서 제공하는 RefreshToken 클래스를 사용하여 리프레시 토큰 생성
            refresh = RefreshToken.for_user(user)

            try:
                # 이미 존재하는 레코드를 가져옵니다.
                entry_refresh_token = ModelRefreshToken.objects.get(user=user)
            except ModelRefreshToken.DoesNotExist:
                # 존재하지 않는 경우에는 새로운 레코드를 생성합니다.
                entry_refresh_token = ModelRefreshToken.objects.create(
                    user=user,
                    refresh_token=str(refresh)
                )
            else:
                # 이미 존재하는 경우에는 해당 레코드의 필드를 업데이트합니다.
                entry_refresh_token.refresh_token = str(refresh)
                entry_refresh_token.save()

            # refresh_key로 해당하는 RefreshToken 인스턴스를 생성
            refresh_token_instance = ModelRefreshToken.objects.get(refresh_token=refresh)
            index_refresh = refresh_token_instance.user_id
            user_id = refresh_token_instance.user
            accessToken = refresh.access_token

            # UserRiot 테이블에 소환사명이 등록되어 있는지 확인
            try:
                entry = UserRiot.objects.get(user=user_id)
            except UserRiot.DoesNotExist:
                return Response({'message': '로그인 성공',
                            'accessToken': str(accessToken),
                            'refreshIndex': str(index_refresh),
                            'riot_id': ''})
            else:
                return Response({'message': '로그인 성공 / riot 연동 확인',
                            'accessToken': str(accessToken),
                            'refreshIndex': str(index_refresh),
                            'riot_id': entry.riot_id})
        
        else:
            # 사용자 인증 실패
            return Response({'error': '유효하지 않은 사용자 정보입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
class Auth(APIView):
    def post(self, request):
        return auth(request)    
class RiotRegisterView(APIView):
    def post(self, request):
        # 사용자 입력값 가져오기
        userId = request.data.get('userId')
        userSN = request.data.get('summonerName')
        user_instance = User.objects.get(username=userId)

        # SummonerName 유효성 검사
        RiotCussor = RiotAPI(RIOTAPIKEY)
        print(RiotCussor.authenticate_RiotID(userSN))
        if RiotCussor.authenticate_RiotID(userSN):
            try:
                # 이미 존재하는 레코드를 가져옵니다.
                entry = UserRiot.objects.get(user=user_instance)
            except UserRiot.DoesNotExist:
                # 존재하지 않는 경우에는 새로운 레코드를 생성합니다.
                entry = UserRiot.objects.create(
                    user=user_instance,
                    riot_id=userSN,
                    riot_puuid = RiotCussor.get_puuid_from_summonerName(userSN)
                )
            else:
                # 동일할 경우
                if entry.riot_id == userSN:
                    return Response({'message': '이전에 등록한 소환사명과 동일합니다.', 'riot_id': userSN}, status=status.HTTP_201_CREATED)
                # 업데이트라면
                else:
                    entry.riot_id = str(userSN)
                    entry.riot_puuid = str(RiotCussor.get_puuid_from_summonerName(userSN))
                    entry.save()
            return Response({'message': '소환사 등록 성공', 'riot_id': userSN}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': '유효하지 않은 소환사 정보입니다.'}, status=status.HTTP_400_BAD_REQUEST)
# 유저 기본 정보 업데이트 
class UpdateView(APIView):
    def post(self, request):
        userId = request.data.get('userId')    
        user_instance = User.objects.get(username=userId)
        ra = RiotAPI(RIOTAPIKEY)
        try:
            # 이미 존재하는 레코드를 가져옵니다.
            entry = UserRiot.objects.get(user=user_instance)
            update = ra.get_user_profile(entry.riot_puuid)
            
        except UserRiot.DoesNotExist:
            return Response({'error': '등록된 소환사명이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            entry.revision_date = update['revisionDate']
            entry.summonerLevel = update['summonerLevel']
            entry.profileIconId = update['profileIconId']
            entry.name = update['name']
            entry.save()

        # 유저 매치 정보 업데이트
        entry_riot = UserRiot.objects.get(user=user_instance)
        match_lst = ra.get_match_Full(entry_riot.riot_id)
        # 매치정보 데이터 베이스에 입력
        update_matches(match_lst)
        
        return Response({'message': '소환사 정보 업데이트 성공',
                         'summonerLevel': update['summonerLevel'],
                            'profileIconId': update['profileIconId'],
                            'name': update['name']}, status=status.HTTP_201_CREATED)
    def get(self, request):
        userId = request.query_params.get('userId')
        user_instance = User.objects.get(username=userId)
        ra = RiotAPI(RIOTAPIKEY)
        try:
            # 이미 존재하는 레코드를 가져옵니다.
            entry = UserRiot.objects.get(user=user_instance)
            profile = ra.get_user_profile(entry.riot_puuid)
            summoner_id = ra.get_summonerId_from_puuid(entry.riot_puuid)
            obj_solorank_summoner = ra.get_league(summoner_id)[0]
        except UserRiot.DoesNotExist:
            return Response({'error': '소환사 정보가 업데이트 되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            tier = obj_solorank_summoner['tier']
            rank = obj_solorank_summoner['rank']
            leaguePoints = obj_solorank_summoner['leaguePoints']
            wins = obj_solorank_summoner['wins']
            losses = obj_solorank_summoner['losses']
            return Response({'message': '소환사 정보 업데이트 성공',
                         'summonerLevel': profile['summonerLevel'],
                            'profileIconId': profile['profileIconId'],
                            'name': profile['name'],
                            'tier': tier,
                            'rank': rank,
                            'leaguePoints': leaguePoints,
                            'wins': wins,
                            'losses': losses}, status=status.HTTP_201_CREATED)
        
class ChampionUsedView(APIView):
    def get(self, request):
        userId = request.query_params.get('userId')
        user_instance = User.objects.get(username=userId)
        ra = RiotAPI(RIOTAPIKEY)
        try:
            # 이미 존재하는 레코드를 가져옵니다.
            entry = UserRiot.objects.get(user=user_instance)
            puuid = entry.riot_puuid
            
        except UserRiot.DoesNotExist:
            return Response({'error': '소환사 정보가 구축 되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            par_entry = Participant.objects.filter(puuid=puuid)

            result = (
                par_entry
                .values('championId')
                .annotate(
                    wins = Count('pk', filter=Q(win=True)),
                    losses = Count('pk', filter=Q(win=False)),
                    avg_kda = Avg('kda'),
                    kills = Sum('kills'),
                    assists = Sum('assists'),
                    deaths = Sum('deaths'),
                )
            )
            response = {}
            champion_name = load_json_file('./champion_name.json')
            for item in result:
                championId = item['championId']
                wins = item['wins']
                losses = item['losses']
                avg_kda = round((item['kills'] + item['assists']) / item['deaths'], 2) if item['deaths'] > 0 else 0
                total = wins + losses
                
                win_rate = round(wins / (wins + losses) * 100, 1) if wins + losses > 0 else 0
                name = champion_name[str(championId)]

                response[championId] = {
                    'wins': wins,
                    'losses': losses,
                    'win_rate': win_rate,
                    'avg_kda': avg_kda,
                    'total': total,
                    'name': name
                }

                
                json_data = json.dumps(response, ensure_ascii=False)
            return JsonResponse(json_data, status=status.HTTP_200_OK, safe=False)
        
class MatchDataIndividual(APIView):
    def get(self, request):
        userId = request.query_params.get('userId')
        user_instance = User.objects.get(username=userId)
        ra = RiotAPI(RIOTAPIKEY)
        try:
            # 이미 존재하는 레코드를 가져옵니다.
            entry = UserRiot.objects.get(user=user_instance)
            puuid = entry.riot_puuid
        except UserRiot.DoesNotExist:
            return Response({'error': '소환사 정보가 구축 되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 쿼리셋 가져오기 기준점 잡기
            match_dict = {}
            par_query_set = Participant.objects.filter(puuid=puuid).annotate(match_time=F('user_match_id__gameEndTimestamp')).order_by('-match_time')
            for participant in par_query_set:
                print(participant.match_time)
                match_instance = UserMatch.objects.get(id=participant.user_match_id)
                compare_instance = ParticipantCompare.objects.get(participant=participant.id)
                match_dict[match_instance.gameEndTimestamp] = {
                    'dataVersion': match_instance.dataVersion,
                    'match_id': match_instance.match_id,
                    'endofGameResult': match_instance.endofGameResult,
                    'gameCreation': match_instance.gameCreation,
                    'gameDuration': match_instance.gameDuration,
                    'match_id': match_instance.match_id,
                    'gameEndTimestamp': match_instance.gameEndTimestamp,
                    'gameId': match_instance.gameId,
                    'gameMode': match_instance.gameMode,
                    'gameName': match_instance.gameName,
                    'mapId': match_instance.mapId,
                    'assists': participant.assists,
                    'bountyGold': participant.bountyGold,
                    'controlWardsPlaced': participant.controlWardsPlaced,
                    'damagePerMinute': participant.damagePerMinute,
                    'deathsByEnemyChamps': participant.deathsByEnemyChamps,
                    'earlyLaningPhaseGoldExpAdvantage': participant.earlyLaningPhaseGoldExpAdvantage,
                    'epicMonsterKillsNearEnemyJungler': participant.epicMonsterKillsNearEnemyJungler,
                    'epicMonsterSteals': participant.epicMonsterSteals,
                    'epicMonsterStolenWithoutSmite': participant.epicMonsterStolenWithoutSmite,
                    'firstTurretKilled': participant.firstTurretKilled,
                    'firstTurretKilledTime': participant.firstTurretKilledTime,
                    'gameLength': participant.gameLength,
                    'goldPerMinute': participant.goldPerMinute,
                    'immobilizeAndKillWithAlly': participant.immobilizeAndKillWithAlly,
                    'initialBuffCount': participant.initialBuffCount,
                    'initialCrabCount': participant.initialCrabCount,
                    'jungleCsBefore10Minutes': participant.jungleCsBefore10Minutes,
                    'kTurretsDestroyedBeforePlatesFall': participant.kTurretsDestroyedBeforePlatesFall,
                    'kda': participant.kda,
                    'killAfterHiddenWithAlly': participant.killAfterHiddenWithAlly,
                    'killParticipation': participant.killParticipation,
                    'killingSprees': participant.killingSprees,
                    'killsNearEnemyTurret': participant.killsNearEnemyTurret,
                    'killsOnOtherLanesEarlyJungleAsLaner': participant.killsOnOtherLanesEarlyJungleAsLaner,
                    'killsUnderOwnTurret': participant.killsUnderOwnTurret,
                    'knockEnemyIntoTeamAndKill': participant.knockEnemyIntoTeamAndKill,
                    'laneMinionsFirst10Minutes': participant.laneMinionsFirst10Minutes,
                    'laningPhaseGoldExpAdvantage': participant.laningPhaseGoldExpAdvantage,
                    'legendaryCount': participant.legendaryCount,
                    'maxCsAdvantageOnLaneOpponent': participant.maxCsAdvantageOnLaneOpponent,
                    'maxLevelLeadLaneOpponent': participant.maxLevelLeadLaneOpponent,
                    'moreEnemyJungleThanOpponent': participant.moreEnemyJungleThanOpponent,
                    'multikills': participant.multikills,
                    'multikillsAfterAggressiveFlash': participant.multikillsAfterAggressiveFlash,
                    'outerTurretExecutesBefore10Minutes': participant.outerTurretExecutesBefore10Minutes,
                    'outnumberedKills': participant.outnumberedKills,
                    'scuttleCrabKills': participant.scuttleCrabKills,
                    'skillshotsDodged': participant.skillshotsDodged,
                    'soloKills': participant.soloKills,
                    'stealthWardsPlaced': participant.stealthWardsPlaced,
                    'takedownOnFirstTurret': participant.takedownOnFirstTurret,
                    'takedowns': participant.takedowns,
                    'takedownsFirstXMinutes': participant.takedownsFirstXMinutes,
                    'teamDamagePercentage': participant.teamDamagePercentage,
                    'teleportTakedowns': participant.teleportTakedowns,
                    'turretPlatesTaken': participant.turretPlatesTaken,
                    'turretTakedowns': participant.turretTakedowns,
                    'visionScorePerMinute': participant.visionScorePerMinute,
                    'wardTakedowns': participant.wardTakedowns,
                    'wardTakedownsBefore20M': participant.wardTakedownsBefore20M,
                    'wardsGuarded': participant.wardsGuarded,
                    'championName': participant.championName,
                    'detectorWardsPlaced': participant.detectorWardsPlaced,
                    'deaths': participant.deaths,
                    'doubleKills': participant.doubleKills,
                    'kills': participant.kills,
                    'puuid': participant.puuid,
                    'timePlayed': participant.timePlayed,
                    'tripleKills': participant.tripleKills,
                    'totalDamageDealt': participant.totalDamageDealt,
                    'totalDamageDealtToChampions': participant.totalDamageDealtToChampions,
                    'totalDamageTaken': participant.totalDamageTaken,
                    'win': participant.win,
                    'teamId': participant.teamId,
                    'teamPosition': participant.teamPosition,
                    'participantId': participant.participantId,
                    'champExperience': participant.champExperience,
                    'champLevel': participant.champLevel,
                    'championId': participant.championId,
                    'dpt': participant.dpt,
                    'dpg': participant.dpg,
                    'ddpt': participant.ddpt,
                    'dgpt': participant.dgpt,
                    'totalPings': participant.totalPings,

                    'damagePerMinuteOppo': compare_instance.damagePerMinuteOppo,
                    'damagePerMinuteRank': compare_instance.damagePerMinuteRank,
                    'bountyGoldOppo': compare_instance.bountyGoldOppo,
                    'bountyGoldRank': compare_instance.bountyGoldRank,
                    'dpgOppo': compare_instance.dpgOppo,
                    'dpgRank': compare_instance.dpgRank,
                    'dptOppo': compare_instance.dptOppo,
                    'dptRank': compare_instance.dptRank,
                    'turretPlatesTakenOppo': compare_instance.turretPlatesTakenOppo,
                    'turretPlatesTakenRank': compare_instance.turretPlatesTakenRank,
                    'killsNearTurret': compare_instance.killsNearTurret,
                    'killsNearTurretOppo': compare_instance.killsNearTurretOppo,
                    'killsNearTurretRank': compare_instance.killsNearTurretRank,
                    'takedownsFirstXMinutesOppo': compare_instance.takedownsFirstXMinutesOppo,
                    'takedownsFirstXMinutesRank': compare_instance.takedownsFirstXMinutesRank,
                    'laneMinionsFirst10MinutesOppo': compare_instance.laneMinionsFirst10MinutesOppo,
                    'laneMinionsFirst10MinutesRank': compare_instance.laneMinionsFirst10MinutesRank,
                    'ddptOppo': compare_instance.ddptOppo,
                    'ddptRank': compare_instance.ddptRank,
                    'dgptOppo': compare_instance.dgptOppo,
                    'dgptRank': compare_instance.dgptRank,
                    'killAfterHiddenWithAllyOppo': compare_instance.killAfterHiddenWithAllyOppo,
                    'killAfterHiddenWithAllyRank': compare_instance.killAfterHiddenWithAllyRank,
                    'outnumberedKillsOppo': compare_instance.outnumberedKillsOppo,
                    'outnumberedKillsRank': compare_instance.outnumberedKillsRank,
                    'moreEnemyJungleThanOpponentOppo': compare_instance.moreEnemyJungleThanOpponentOppo,
                    'moreEnemyJungleThanOpponentRank': compare_instance.moreEnemyJungleThanOpponentRank,
                    'visionScorePerMinuteOppo': compare_instance.visionScorePerMinuteOppo,
                    'visionScorePerMinuteRank': compare_instance.visionScorePerMinuteRank,
                    'totalPingsOppo': compare_instance.totalPingsOppo,
                    'totalPingsRank': compare_instance.totalPingsRank,
                    'myTeamPings': compare_instance.myTeamPings,
                    'myTeamPingsOppo': compare_instance.myTeamPingsOppo,
                    'item0': participant.item0,
                    'item1': participant.item1,
                    'item2': participant.item2,
                    'item3': participant.item3,
                    'item4': participant.item4,
                    'item5': participant.item5,
                    'item6': participant.item6,
                    'spell1Casts': participant.spell1Casts,
                    'spell2Casts': participant.spell2Casts,
                    'spell3Casts': participant.spell3Casts,
                    'spell4Casts': participant.spell4Casts,
                    'summoner1Casts': participant.summoner1Casts,
                    'summoner1Id': participant.summoner1Id,
                    'summoner2Casts': participant.summoner2Casts,
                    'summoner2Id': participant.summoner2Id,
                    'mvp' : get_mvp(participant.damagePerMinute)

                    }
        
                json_data = json.dumps(match_dict, ensure_ascii=False)
            return JsonResponse(json_data, status=status.HTTP_200_OK, safe=False)

        
            # 또는 필요한 경우 Q 객체를 사용하여 두 객체를 함께 필터링할 수 있습니다.
# class DetailView(APIView):
#     def get(self, request):
#         userId = request.query_params.get('userId')
#         user_instance = User.objects.get(username=userId)
#         ra = RiotAPI(RIOTAPIKEY)
#         try:
#             # 이미 존재하는 레코드를 가져옵니다.
#             entry = UserRiot.objects.get(user=user_instance)
#             puuid = entry.riot_puuid
            
#         except UserRiot.DoesNotExist:
#             return Response({'error': '소환사 정보가 구축 되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             par_entry = Participant.objects.filter(puuid=puuid)
#             par_compare_entry = ParticipantCompare.objects.filter(participant__in=par_entry)

#             combined_queryset = Participant.objects.annotate(
#     total_pings_oppo=F('participantcompare__totalPingsOppo'),
#     total_pings_rank=F('participantcompare__totalPingsRank'),
#     my_team_pings_oppo=F('participantcompare__myTeamPingsOppo'),
#     total_wins_and_pings=Sum(F('wins') + F('participantcompare__totalPingsOppo') + F('participantcompare__totalPingsRank') + F('participantcompare__myTeamPingsOppo'))
# )
#             result = (
#                 par_entry
#                 .values('championId')
#                 .annotate(
#                     wins = Count('pk', filter=Q(win=True)),
#                     losses = Count('pk', filter=Q(win=False)),
#                     avg_kda = Avg('kda'),
#                     kills = Sum('kills'),
#                     assists = Sum('assists'),
#                     deaths = Sum('deaths'),
#                 )
#             )
#             response = {}
#             champion_name = load_json_file('./champion_name.json')
#             for item in result:
#                 championId = item['championId']
#                 wins = item['wins']
#                 losses = item['losses']
#                 avg_kda = round((item
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class ModelRefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=1000)

class UserRiot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    riot_id = models.CharField(max_length=1000, default="")
    riot_puuid = models.CharField(max_length=1000, default="")
    revision_date = models.CharField(max_length=1000, default="")
    summonerLevel = models.IntegerField(default=0)
    profileIconId = models.IntegerField(default=0)
    name = models.CharField(max_length=1000, default="")


class UserMatch(models.Model):
    # 'metadata'
    dataVersion = models.CharField(max_length=1000, default="")
    match_id = models.CharField(max_length=1000, default="")

    # 'info'
    endofGameResult = models.CharField(max_length=1000, default="")
    gameCreation = models.CharField(max_length=1000, default="")
    gameDuration = models.CharField(max_length=1000, default="")
    gameEndTimestamp = models.CharField(max_length=1000, default="")
    gameId = models.CharField(max_length=1000, default="")
    gameMode = models.CharField(max_length=1000, default="")
    gameName = models.CharField(max_length=1000, default="")
    mapId = models.CharField(max_length=1000, default="")



class Participant(models.Model):
    user_match = models.ForeignKey(UserMatch, on_delete=models.CASCADE)
    assists = models.IntegerField(default=0)
    bountyGold = models.IntegerField(default=0)
    controlWardsPlaced = models.IntegerField(default=0)
    damagePerMinute = models.FloatField(default=0)
    damageTakenOnTeamPercentage = models.FloatField(default=0)
    deathsByEnemyChamps = models.IntegerField(default=0)
    earlyLaningPhaseGoldExpAdvantage = models.IntegerField(default=0)
    epicMonsterKillsNearEnemyJungler = models.IntegerField(default=0)
    epicMonsterSteals = models.IntegerField(default=0)
    epicMonsterStolenWithoutSmite = models.IntegerField(default=0)
    firstTurretKilled = models.BooleanField(default=False)
    firstTurretKilledTime = models.FloatField(default=0)
    gameLength = models.FloatField(default=0)
    goldPerMinute = models.FloatField(default=0)
    immobilizeAndKillWithAlly = models.IntegerField(default=0)
    initialBuffCount = models.IntegerField(default=0)
    initialCrabCount = models.IntegerField(default=0)
    jungleCsBefore10Minutes = models.IntegerField(default=0)
    kTurretsDestroyedBeforePlatesFall = models.IntegerField(default=0)
    kda = models.FloatField(default=0)
    killAfterHiddenWithAlly = models.IntegerField(default=0)
    killParticipation = models.FloatField(default=0)
    killingSprees = models.IntegerField(default=0)
    killsNearEnemyTurret = models.IntegerField(default=0)
    killsOnOtherLanesEarlyJungleAsLaner = models.IntegerField(default=0)
    killsUnderOwnTurret = models.IntegerField(default=0)
    knockEnemyIntoTeamAndKill = models.IntegerField(default=0)
    laneMinionsFirst10Minutes = models.IntegerField(default=0)
    laningPhaseGoldExpAdvantage = models.IntegerField(default=0)
    legendaryCount = models.IntegerField(default=0)
    maxCsAdvantageOnLaneOpponent = models.IntegerField(default=0)
    maxLevelLeadLaneOpponent = models.IntegerField(default=0)
    moreEnemyJungleThanOpponent = models.FloatField(default=0)
    multikills = models.IntegerField(default=0)
    multikillsAfterAggressiveFlash = models.IntegerField(default=0)
    outerTurretExecutesBefore10Minutes = models.IntegerField(default=0)
    outnumberedKills = models.IntegerField(default=0)
    scuttleCrabKills = models.IntegerField(default=0)
    skillshotsDodged = models.IntegerField(default=0)
    soloKills = models.IntegerField(default=0)
    stealthWardsPlaced = models.IntegerField(default=0)
    takedownOnFirstTurret = models.IntegerField(default=0)
    takedowns = models.IntegerField(default=0)
    takedownsFirstXMinutes = models.IntegerField(default=0)
    teamDamagePercentage = models.FloatField(default=0)
    teleportTakedowns = models.IntegerField(default=0)
    turretPlatesTaken = models.IntegerField(default=0)
    turretTakedowns = models.IntegerField(default=0)
    visionScorePerMinute = models.FloatField(default=0)
    wardTakedowns = models.IntegerField(default=0)
    wardTakedownsBefore20M = models.IntegerField(default=0)
    wardsGuarded = models.IntegerField(default=0)
    championName = models.CharField(max_length=1000, default="")
    detectorWardsPlaced = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    doubleKills = models.IntegerField(default=0)
    kills = models.IntegerField(default=0)
    puuid = models.CharField(max_length=1000, default="")
    timePlayed = models.FloatField(default=0)
    tripleKills = models.IntegerField(default=0)
    totalDamageDealt = models.IntegerField(default=0)
    totalDamageDealtToChampions = models.IntegerField(default=0)
    totalDamageTaken = models.IntegerField(default=0)
    win = models.BooleanField(default=False)
    teamId = models.IntegerField(default=0)
    teamPosition = models.CharField(max_length=1000, default="")
    participantId = models.IntegerField(default=0)
    champExperience = models.IntegerField(default=0)
    champLevel = models.IntegerField(default=0)
    championId = models.IntegerField(default=0)
    # 'stats made by me
    dpt = models.FloatField(default=0)
    dpg = models.FloatField(default=0)
    ddpt = models.FloatField(default=0)
    dgpt = models.FloatField(default=0)
    totalPings = models.IntegerField(default=0)

    # 추가 3/25
    item0 = models.IntegerField(default=0)
    item1 = models.IntegerField(default=0)
    item2 = models.IntegerField(default=0)
    item3 = models.IntegerField(default=0)
    item4 = models.IntegerField(default=0)
    item5 = models.IntegerField(default=0)
    item6 = models.IntegerField(default=0)
    spell1Casts = models.IntegerField(default=0)
    spell2Casts = models.IntegerField(default=0)
    spell3Casts = models.IntegerField(default=0)
    spell4Casts = models.IntegerField(default=0)
    summoner1Casts = models.IntegerField(default=0)
    summoner1Id = models.IntegerField(default=0)
    summoner2Casts = models.IntegerField(default=0)
    summoner2Id = models.IntegerField(default=0)
    



class ParticipantCompare(models.Model):
    # participant랑 1:1 매칭
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    # percentage
    damagePerMinuteOppo = models.FloatField(default=0)
    damagePerMinuteRank = models.IntegerField(default=0)
    # simple
    bountyGoldOppo = models.IntegerField(default=0)
    bountyGoldRank = models.IntegerField(default=0)
    # percentage
    dpgOppo = models.FloatField(default=0)
    dpgRank = models.IntegerField(default=0)
    # percentage
    dptOppo = models.FloatField(default=0)
    dptRank = models.IntegerField(default=0)
    # simple
    turretPlatesTakenOppo = models.IntegerField(default=0)
    turretPlatesTakenRank = models.IntegerField(default=0)
    # simple, float
    killsNearTurret = models.FloatField(default=0)
    killsNearTurretOppo = models.FloatField(default=0)
    killsNearTurretRank = models.IntegerField(default=0)
    # simple
    takedownsFirstXMinutesOppo = models.IntegerField(default=0)
    takedownsFirstXMinutesRank = models.IntegerField(default=0)
    # simple
    laneMinionsFirst10MinutesOppo = models.IntegerField(default=0)
    laneMinionsFirst10MinutesRank = models.IntegerField(default=0)

    # percentage
    ddptOppo = models.FloatField(default=0)
    ddptRank = models.IntegerField(default=0)
    # percentage
    dgptOppo = models.FloatField(default=0)
    dgptRank = models.IntegerField(default=0)
    # simple
    killAfterHiddenWithAllyOppo = models.IntegerField(default=0)
    killAfterHiddenWithAllyRank = models.IntegerField(default=0)
    # simple
    outnumberedKillsOppo = models.IntegerField(default=0)
    outnumberedKillsRank = models.IntegerField(default=0)
    # simple, float (jungler)
    moreEnemyJungleThanOpponentOppo = models.FloatField(default=0)
    moreEnemyJungleThanOpponentRank = models.IntegerField(default=0)
    # percentage
    visionScorePerMinuteOppo = models.FloatField(default=0)
    visionScorePerMinuteRank = models.IntegerField(default=0)

    # TeamPing
    totalPingsOppo = models.IntegerField(default=0)
    totalPingsRank = models.IntegerField(default=0)

    # TeamPing
    myTeamPings = models.IntegerField(default=0)
    myTeamPingsOppo = models.FloatField(default=0)

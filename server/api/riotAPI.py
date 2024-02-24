import requests
import json
import time
import pandas as pd
from tqdm import tqdm

API_KEY = "RGAPI-41ddc906-11ba-43fb-8f5d-9cc894ce7f0b"

class RiotAPI:
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.header = {"X-Riot-Token": API_KEY}

    def get_puuid_from_summonerName(self, summonerName):
        url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}"
        response = requests.get(url, headers=self.header)
        return response.json()['puuid']
    
    def get_matchid_lst_from_puuid(self, puuid):
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?"
        response = requests.get(url, headers=self.header)
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
            time.sleep(1.2)
        return match_lst
    
test = RiotAPI(API_KEY)
print(test.get_match_Full("zi존준기123#KR1")[0])
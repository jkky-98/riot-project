# Description: 챔피언 이름을 한글로 변환하는 json 파일을 생성하는 코드입니다.
import requests
import json

def create_json_champion_name():
    url = 'https://ddragon.leagueoflegends.com/cdn/14.5.1/data/ko_KR/champion.json'
    response = requests.get(url)
    champEnName = list(response.json()['data'].keys())

    dict_tmp = {}

    for i in champEnName:
        key = response.json()['data'][i]['key']
        name = response.json()['data'][i]['name']
        dict_tmp[key] = name
    
    with open('champion_name.json', 'w', encoding='utf-8') as make_file:
        json.dump(dict_tmp, make_file, ensure_ascii=False, indent="\t")

    return print('champion_name.json created successfully')

create_json_champion_name()
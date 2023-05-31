# -*- coding: utf-8 -*-
"""
Created on 26/02/2023 21:25
@author: GiovanniMINGHELLI
"""

import json
import pandas as pd
import urllib3
from nba_common_library.utils.lib_string import *
from nba_common_library.utils.utils import get_path_file

header_data = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}


def player_stats_url(season):
    return f"https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=" \
           f"&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=" \
           f"&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=" \
           f"0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season={season}&SeasonSegment=" \
           f"&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=" \
           f"&VsDivision=&Weight="


def extract_data(http_client, url):
    r = http_client.request('GET', url, headers=header_data)
    resp = json.loads(r.data)
    results = resp['resultSets'][0]
    headers = results['headers']
    rows = results['rowSet']
    frame = pd.DataFrame(rows)
    frame.columns = headers
    return frame


def convert_bbref_season_to_nba_season(season):
    if type(season) != str:
        season = str(season)

    year = int(season)
    last_year = year - 1
    last_two = season[-2:]
    return "{0}-{1}".format(last_year, last_two)


def get_nba_stats(season):
    if os.path.exists(get_path_file(f'stats_nba_player_data_{season}.csv')):
        return pd.read_csv(get_path_file(f'stats_nba_player_data_{season}.csv'))

    else:
        frame = extract_data(urllib3.PoolManager(), player_stats_url(convert_bbref_season_to_nba_season(season)))
        frame.to_csv(os.path.join(database_path, f'stats_nba_player_data_{season}.csv'), index=False)
    return frame

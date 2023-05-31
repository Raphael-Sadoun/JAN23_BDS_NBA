# -*- coding: utf-8 -*-
"""
Created on 23/02/2023 21:24
@author: GiovanniMINGHELLI
"""

import string
import pandas as pd
from urllib.request import urlopen
from basketball_reference_web_scraper.data import Position
from bs4 import BeautifulSoup
import urllib3
from nba_common_library.scrappers.merge_sources import get_id_corr
from nba_common_library.utils.lib_string import *
from tqdm import tqdm
from urllib.error import HTTPError
from basketball_reference_web_scraper import client
import random
import time
import numpy as np
import os
from nba_common_library.utils.utils import get_path_file


def get_nba_reference_hands():
    if os.path.exists(get_path_file('nba_hands.csv')):
        return pd.read_csv(get_path_file('nba_hands.csv'))

    all_data = []
    for letter in tqdm(string.ascii_lowercase, desc='Players list : '):
        soup = BeautifulSoup(urlopen(f"https://www.basketball-reference.com/players/{letter}/"), features="lxml")
        headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
        rows = soup.findAll('tr')[1:]
        rows_data = []
        for r in range(len(rows)):
            new_row = [td.getText() for td in rows[r].findAll('td')]
            new_row.insert(0, rows[r].find('th', {'data-append-csv': True}).get('data-append-csv'))
            rows_data.append(new_row)
        all_data.extend(rows_data)
        time.sleep(random.uniform(1, 5))

    df = pd.DataFrame(all_data, columns=headers)
    hands = {}

    for id in tqdm(df.Player, desc='Players hands : '):
        try:
            soup = BeautifulSoup(urlopen(f"https://www.basketball-reference.com/players/{id[0]}/{id}.html"),
                                 "html.parser")
            info_player = soup.find('div', class_='players', id='info').findAll('p')
            indices = [i for i, p in enumerate(info_player) if 'Shoots:' in p.text]
            if indices:
                hands[id] = info_player[indices[0]].text.split()[-1]
            else:
                hands[id] = None
        except HTTPError as err:
            hands[id] = err.code
        except:
            hands[id] = None
        time.sleep(random.uniform(1, 5))

    df['hands'] = df.Player.map(hands)
    df.to_csv(os.path.join(project_path, data, f'nba_hands.csv'))
    return df


def player_totals_page(season):
    return "https://www.basketball-reference.com/leagues/NBA_{0}_totals.html".format(season)


def player_page(slug_id):
    return f"https://www.basketball-reference.com/players/{slug_id[0]}/{slug_id}.html#all_adj_shooting"


def extract_column_names(table):
    columns = [col["aria-label"] for col in table.find_all("thead")[0].find_all("th")][1:]
    columns.append("id")
    return columns


def extract_rows(table):
    rows = table.find_all("tbody")[0].find_all("tr")
    parsed_rows = []
    for r in rows:
        parsed = parse_row(r)
        if len(parsed) > 0:
            parsed_rows.append(parsed)
    return parsed_rows


def parse_row(row):
    other_data = row.find_all("td")
    if len(other_data) == 0:
        return []
    id = other_data[0].find_all("a")[0]["href"].replace("/players/", "").replace(".html", "").split("/")[-1]
    row_data = [td.string for td in other_data]
    row_data.append(id)
    return row_data


def get_bb_stats(season):
    if os.path.exists(get_path_file(f'basketball_reference_totals_{season}.csv')):
        return pd.read_csv(get_path_file(f'basketball_reference_totals_{season}.csv'))

    else:
        r = urllib3.PoolManager().request('GET', player_totals_page('2019'))
        soup = BeautifulSoup(r.data, 'html')
        f = soup.find_all("table")
        rows = []
        columns = []
        if len(f) > 0:
            columns = extract_column_names(f[0])
            rows = rows + extract_rows(f[0])

        frame = pd.DataFrame(rows)
        frame.columns = columns
        frame.to_csv(os.path.join(project_path, data, f'basketball_reference_totals_{season}.csv'),
                     index=False)
    return frame


def get_advanced_score(season=2019, n_last=None):
    if not n_last and os.path.isfile(get_path_file(f'advanced_score_{season}.csv')):
        return pd.read_csv(get_path_file(f'advanced_score_{season}.csv'))
    data_frame = pd.DataFrame(client.players_advanced_season_totals(season_end_year=season))
    data_frame.drop(['name', 'age', 'positions', 'team', 'is_combined_totals'], axis=1, inplace=True)
    data_frame.to_csv(os.path.join(database_path, f'advanced_score_{season}.csv'))
    return data_frame


def get_player_score(season=2019, n_last=None):
    id_table = get_id_corr(season=season)
    if not n_last and os.path.isfile(get_path_file(f'player_score_{season}.csv')):
        return pd.read_csv(get_path_file(f'player_score_{season}.csv'))

    temp_list = []
    for id_ in tqdm(id_table.bbref_id):
        time.sleep(random.uniform(1, 3))
        try:
            stats_df = pd.DataFrame(client.regular_season_player_box_scores(
                player_identifier=id_, season_end_year=season)).sort_values(by='date', ascending=False)
            if n_last is not None:
                stats_df = stats_df.head(n_last)

            seconds_played = stats_df.seconds_played.sum()

            fg_attempted = stats_df.attempted_field_goals.sum()
            fg_made = stats_df.made_field_goals.sum()
            fg_score = (fg_made / fg_attempted / seconds_played) * 100000 if fg_attempted else 0

            fg3_attempted = stats_df.attempted_three_point_field_goals.sum()
            fg3_made = stats_df.made_three_point_field_goals.sum()
            fg3_score = (fg3_made / fg3_attempted / seconds_played) * 100000 if fg3_attempted else 0

            ft_attempted = stats_df.attempted_free_throws.sum()
            ft_made = stats_df.made_free_throws.sum()
            ft_score = (ft_made / ft_attempted / seconds_played) * 100000 if ft_attempted else 0

            temp_list.append([id_, fg_score, fg3_score, ft_score])
        except:
            temp_list.append([id_, np.nan, np.nan, np.nan])

    data_frame = pd.DataFrame(columns=['slug', 'fg_score', 'fg3_score', 'ft_score'], data=temp_list)
    data_frame.to_csv(os.path.join(database_path, f'player_score_{season}.csv'))
    return data_frame


def get_teams_stats(season=2019):
    abbrev_to_id = {item['abbreviation']: item['id'] for item in teams_data}
    data_frame = pd.read_csv(get_path_file('opponents_per_games.csv'))
    data_frame = data_frame[data_frame.season == season]
    data_frame['team_id'] = data_frame['abbreviation'].map(abbrev_to_id)
    keeped = ['team_id', 'mp_per_game', 'opp_fg_per_game', 'opp_fga_per_game', 'opp_fg_percent',
              'opp_x3p_per_game', 'opp_x3pa_per_game', 'opp_x3p_percent', 'opp_x2p_per_game',
              'opp_x2pa_per_game', 'opp_x2p_percent', 'opp_ft_per_game', 'opp_fta_per_game',
              'opp_ft_percent', 'opp_pf_per_game', 'opp_pts_per_game']
    return data_frame[keeped]


def get_position_from_slug(season=2019, from_name=False):
    df_list = [pd.DataFrame(client.players_season_totals(i)) for i in [season - 1, season, season + 1]]
    data_frame = pd.concat(df_list, axis=0)
    data_frame['positions'] = data_frame.positions.apply(lambda x: x[0]).map({Position.POINT_GUARD: PG,
                                                                              Position.SHOOTING_GUARD: SG,
                                                                              Position.SMALL_FORWARD: SF,
                                                                              Position.POWER_FORWARD: PF,
                                                                              Position.CENTER: C,
                                                                              Position.FORWARD: 'F',
                                                                              Position.GUARD: 'G'})
    return dict(zip(data_frame['name' if from_name else 'slug'], data_frame['positions']))

def get_fg3_bbref_score(season):
    datas = get_bb_stats(season)
    datas['fg3_norm'] = round(((datas['3-Point Field Goal Percentage'] / datas['Minutes Played']) * 100), 3)
    return datas.set_index('id')['fg3_norm'].to_dict()


if __name__ == '__main__':
    get_teams_stats()
    get_position_from_slug()
    get_player_score()

# -*- coding: utf-8 -*-
"""
Created on 26/02/2023 22:52
@author: GiovanniMINGHELLI
"""
import pandas as pd
from fuzzywuzzy import fuzz
from nba_common_library.scrappers.bb_ref_scrap import *
from nba_common_library.utils.lib_string import *
import os

from nba_common_library.utils.utils import get_path_file


def deduplicate_traded_players(group):
    if len(group) > 1:
        return group[group["Tm"] == "TOT"]
    return group


def check_names_fuzzy_match(row):
    row["name_match"] = fuzz.partial_ratio(row["Player"], row["PLAYER_NAME"]) > 60
    return row


def get_id_corr(season=2019):
    from nba_common_library.scrappers.nba_scrap import get_nba_stats
    from nba_common_library.scrappers.bb_ref_scrap import get_bb_stats
    bbref_data = get_bb_stats(season)
    nba_data = get_nba_stats(season)

    if os.path.exists(get_path_file(f'id_correspondancy_table_{season}.csv')):
        return pd.read_csv(get_path_file(f'id_correspondancy_table_{season}.csv'))

    else:
        nba_data["PLAYER_ID"] = nba_data["PLAYER_ID"].astype(str)
        bbref_base_data = bbref_data[["Player", "id", "Tm", "FGA", "Total Rebounds",
                                      "Assists"]].groupby(by="id").apply(deduplicate_traded_players)

        nba_base_data = nba_data[["PLAYER_ID", "PLAYER_NAME", "FGA", "REB", "AST"]]

        name_matches = bbref_base_data.merge(nba_base_data,
                                             left_on=["Player", "FGA", "Total Rebounds", "Assists"],
                                             right_on=["PLAYER_NAME", "FGA", "REB", "AST"], how="outer")

        name_matches_ids = name_matches.dropna()
        name_matches_ids = name_matches_ids[["Player", "id", "PLAYER_NAME", "PLAYER_ID"]]
        name_matches_ids.columns = ["bbref_name", "bbref_id", "nba_name", "nba_id"]

        non_matches = name_matches[name_matches.isnull().any(axis=1)]

        bbref_non_matches = non_matches[["Player", "id", "FGA", "Total Rebounds", "Assists"]].dropna()
        nba_non_matches = non_matches[["PLAYER_NAME", "PLAYER_ID", "FGA", "REB", "AST"]].dropna()

        possible_matches = bbref_non_matches.merge(nba_non_matches,
                                                   left_on=["FGA", "Total Rebounds", "Assists"],
                                                   right_on=["FGA", "REB", "AST"], how="outer").apply(
            check_names_fuzzy_match, axis=1)

        # print out any misses
        # print(possible_matches[possible_matches["name_match"] != True].head(10))

        fuzzy_matches = possible_matches[possible_matches["name_match"]][["Player", "id", "PLAYER_NAME", "PLAYER_ID"]]
        fuzzy_matches.columns = ["bbref_name", "bbref_id", "nba_name", "nba_id"]
        all_matches = fuzzy_matches.append(name_matches_ids)
        all_matches.to_csv(os.path.join(project_path, data, f'id_correspondancy_table_{season}.csv'))

    return all_matches


if __name__ == '__main__':
    get_id_corr()

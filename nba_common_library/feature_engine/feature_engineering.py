# -*- coding: utf-8 -*-
"""
Created on 28/02/2023 16:19
@authors:  SelimKNEDIF, GiovanniMINGHELLI, RaphaelSADOUN
"""

import os
from nba_common_library.utils.lib_string import *
import pandas as pd
import psutil
from nba_common_library.utils.utils import map_position, dual_situation, get_shooting_distance, get_shooting_angle, \
    get_shooting_quadrant, get_type_duel, get_path_file
from nba_common_library.scrappers.bb_ref_scrap import get_nba_reference_hands, get_advanced_score, get_player_score, \
    get_teams_stats, get_position_from_slug
from nba_common_library.scrappers.merge_sources import get_id_corr
from nba_common_library.preprocessing.merge_data import merge_data_by_season


def get_new_features(new_features_added=False, season=2019):
    # Si l'object existe déjà et aucune nouvelle feature implémentée on se contente d'importer
    file_fe = get_path_file(file=f'shot_data_merged_{season}_fe.csv')
    if not new_features_added and file_fe:
        return pd.read_csv(file_fe)

    # Importation de la table shot_data_merged_{season} ou creation
    data_merged_output = get_path_file(file=f'shot_data_merged_{season}.csv')
    if not os.path.isfile(data_merged_output):
        merge_data_by_season()
        get_new_features()

    chunk_list = []
    for chunk in pd.read_csv(data_merged_output, chunksize=int(psutil.virtual_memory().available * 0.1 / 1e6)):
        chunk_list.append(chunk)

    # Application des operations de feature engineering
    sdm_file = features_engine_operations(pd.concat(chunk_list))

    # Sauvegarde du fichier incluant les operations de feature engineering
    sdm_file.to_csv(os.path.join(database_path, transformed_data, f'shot_data_merged_{season}_fe.csv'))

    return sdm_file


def features_engine_operations(table: pd.DataFrame) -> pd.DataFrame:
    # Assignation des identifiant basket-ball référence
    table['bbref_id'] = table.player_id.map(get_id_corr(season=2019).set_index('nba_id')['bbref_id'].to_dict())

    # Dictionnaire des postes
    map_position_assign = map_position()  # Par nba_id
    slug_position_assign = get_position_from_slug()  # Par slug_id/bbref_id

    # Ajout des postes pour les n joueurs impliqués sur l'action
    for i in range(1, 4):
        table[f'player_{i}_position'] = table[f'player_{i}_name'].map(map_position_assign)
        table.loc[table.player_1_position.isna(), f'player_{i}_position'] = table.loc[table.player_1_position.isna(),
            'bbref_id'].map(slug_position_assign)
        # Ajout du type de poste interieur vs exterieur
        table[f'player_{i}_pos_type'] = list(map(lambda x: next((key for key,
        values in postes_type.items() if x in values), x), table[f'player_{i}_position']))

    # Affectation de la situation d'adversité
    table['situation'] = table.apply(dual_situation, axis=1)

    # Affactation de la présence de défense
    table['is_defended'] = table['situation'].apply(lambda x: x[-1])

    # Ajout de l'angle de tir
    table['shot_angle'] = table.apply(lambda x: get_shooting_angle(x['shot_x_location'], x['shot_y_location']),
                                      axis=1)

    # Ajout de la main de tir préferentielle #####  Noms des variables a harmoniser ######
    table['dominant_hand'] = table.bbref_id.map(get_nba_reference_hands().set_index('Player')['hands'].to_dict())

    # Ajout de la distance de tir
    table['shot_distance'] = table.apply(
        lambda x: get_shooting_distance(x['shot_x_location'], x['shot_y_location']), axis=1)

    # Ajout du quadrant de tir
    table['quadrant'] = table.apply(lambda x: get_shooting_quadrant(x['shot_x_location'], x['shot_y_location']),
                                    axis=1)

    # Ajout du temps joué pour le joueur sur le match du tir au moment du tir

    # Ajout du temps depuis le dernier match joué

    # Ajout du temps de jeu moyen d'un joueur

    # Ajout de l'experience du joueur

    # Ajout du nb de présence all-star, all-defense -- BBREF TO SCRAPP

    # Ajout de zones de tirs préferentiels (corners)

    # Score joueur par zone (joueurs de corner etc..)

    # Taux de conversion intra-match joueur -- BBREF TO SCRAPP

    # Taux de conversion intra-match équipe -- BBREF TO SCRAPP

    # Ajout du duel de poste
    table['dual_pos'] = table.apply(lambda x: None if pd.isna(x.player_3_position) else
                                    f"{x['player_1_position']} v {x['player_3_position']}", axis=1)
    table['dual_pos_type'] = table['dual_pos'][table['dual_pos'].notnull()].map(get_type_duel).value_counts()

    # Correction des égalités au score
    table.loc[table['score_margin'].notnull(), 'score_margin'] = table.loc[table[
        'score_margin'].notnull(), 'score_margin'].apply(lambda x: 0 if x == 'TIE' else int(x))

    # Ajout d'une colonne d'avantage au score
    table['is_advantaged'] = table['score_margin'][
        table['score_margin'].notnull()].apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))

    # Ajout du temps restant dans le quart-temps en cours en secondes
    table['time_remain_curper'] = table['minutes_remain'] * 60 + table['seconds_remain']

    # Ajout du temps restant dans le quart-temps en cours en secondes
    table['total_time_remain'] = table['period'] * table['minutes_remain'] * 60 + table['seconds_remain']

    # Ajout de l'identifiant de l'équipe qui joue à domicile
    table['home_team_id'] = table['home_team'].apply(lambda x: teams_ids[teams_names.index(x)])

    # Ajout de la reception du match ou non
    table['is_at_home'] = table[['team_id', 'home_team_id']].apply(lambda x: int(x[0] == x[1]), axis=1)

    # Ajout du type de tir effectué
    table['shoot_type'] = list(
        map(lambda x: next((key for key, values in shoot_types.items() if x in values), x), table['action_type']))

    # Ajout de la temporalité du tir sur la possession par rapport aux echéances de temps (24 sec et buzzer)

    # Ajout de la variable binaire indiquant si le tir est à 3pt ou non
    table[is_3pt_shot] = (table[shot_type] == "3PT Field Goal").astype(int)

    # On change la variable home_record en un ratio victoires/total de matchs à domicile
    # Pareil avec la variable away_record
    table[won_ratio_at_home] = table[home_record].apply(
        lambda x: float(x.split("-")[0]) / (float(x.split("-")[0]) + float(x.split("-")[1])) if x != "0-0" else 0)

    table[won_ratio_away] = table[away_record].apply(
        lambda x: float(x.split("-")[0]) / (float(x.split("-")[0]) + float(x.split("-")[1])) if x != "0-0" else 0)

    # Ajout de la pression temporalité sur tir (24sec possession et buzzer de fin de QT)
    

    # Ajout des advanced stats bb_ref (PER)
    advanced_scores = get_advanced_score().drop_duplicates(subset='slug')
    table = pd.merge(table, advanced_scores, how='left', left_on='bbref_id', right_on='slug')

    # Affectation des scores de tir
    player_scores = get_player_score().drop_duplicates(subset='slug')
    table = pd.merge(table, player_scores, how='left', left_on='bbref_id', right_on='slug')

    # Ajout des stats descriptives des équipes
    team_stats = get_teams_stats().drop_duplicates(subset='team_id')
    table = pd.merge(table, team_stats, how='left', on='team_id')
    
    return table


if __name__ == '__main__':
    get_new_features()

#%%

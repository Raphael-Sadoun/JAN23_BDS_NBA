# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:49:44 2023

@author: Raphael Sadoun
"""

# Importation des modules utilises
import os
import pandas as pd
from nba_common_library.utils.lib_string import *
from nba_common_library.utils.utils import get_path_file


def merge_data_by_season(season=2019, verbose=True, write_to_file=True):
    """
    Joint les informations concernant les joueurs, les équipes et les détails de l'action pour 
    chaque tir d'une saison NBA que l'on a à disposition dans le jeu de données nba_shot_locations.
    Retourne un unique jeu de données de type DataFrame.
    
    -- data_path: Chemin du dossier où sont situés les fichiers csv du projet
    -- season : La saison NBA que l'on souhaite sélectionner
    -- verbose : True si l'on veut que la fonction indique des informations détaillées, False sinon
    -- write_to_file: Si True, sauvegarde le DataFrame final dans un fichier csv
    """
    
    # Si le fichier existe déja, on se contente de charger les données dans un DataFrame
    # et de retourner ce dernier
    file_path = get_path_file(f"shot_data_merged_{season}.csv")
    if file_path is not None:
        return pd.read_csv(file_path, index_col=0)

    # Chargement des jeux de données
    pbp_file = f"{season-1}-{season % 1000}_pbp.csv"
    files = ['nba_shot_locations.csv',
             'players.csv',
             'ranking.csv',
             pbp_file]
    datasets = []
    for file in files:
        file_path = get_path_file(file)
        if verbose:
            print(f"Lecture du fichier '{file}'...")
        dataset = pd.read_csv(file_path)
        # On supprime les colonnes "unnamed_*" qui sont des pseudo-index et qui ont pu être ajoutées 
        # au moment de la lecture des fichiers csv avec la fonction read_csv.
        columns = [col for col in dataset.columns if "unnamed" not in col.lower()]
        dataset = dataset[columns]
        datasets.append(dataset)
    shot_data = datasets[0]
    player_data = datasets[1]
    ranking_data = datasets[2]
    pbp_data = datasets[3]
       
    # Avant de réaliser la jointure, on traite les valeurs manquantes de la colonne score_margin. 
    # Cette dernière contient des valeurs manquantes correspondant aux actions pour lesquelles 
    # le score n'a pas évolué (tir raté, passe, etc...).
    # La méthode consistant à remplacer les valeurs manquantes par la dernière valeur valide 
    # semble donc justifiée mais il faut l'appliquer uniquement match par match. Dans le cas 
    # contraire, on propage le résultat final du match précédent au match qui le succède
    # De plus, pour un match donné, les premières valeurs manquantes correspondent à des entrées non 
    # renseignées mais qui correspondent en réalité à un score de 0-0 en début de match avant qu'un tir
    # n'est été réussi par l'une des deux équipes. On remplace ces valeurs par 'TIE' qui est la valeur 
    # déja utilisée dans la colonne pour indiquer que les équipes sont à égalité.
    for game_id in pbp_data['game_id'].unique():
        selection = pbp_data['game_id']==game_id
        score_margin_copy = pbp_data[selection]['score_margin']
        pbp_data.loc[selection, 'score_margin'] = score_margin_copy.fillna(method='ffill')
        pbp_data.loc[selection, 'score_margin'] = pbp_data.loc[selection,'score_margin'].fillna('TIE')
    
    # On ajoute les données détaillées de l'action pour chaque tir en réalisant 
    # une jointure interne entre shot_data et pbp_data sur les colonnes game_id, 
    # period et game_event_id. Pour cela, on renomme la colonne 'event_num' de pbp_data 
    # en 'game_event_id'.
    if verbose:
        print("Ajout des données détaillées de l'action pour chaque tir...")
    pbp_data = pbp_data.rename({'event_num': 'game_event_id'}, axis=1)
    shot_data = shot_data.merge(pbp_data, how='inner',
                                on=['game_id', 'game_event_id', 'period'])

    # # On ajoute les données individuelles de chaque joueur dans shot_data 
    # en réalisant une jointure interne sur la colonne 'player_name'
    if verbose:
        print("Ajout des données des joueurs pour chaque tir...")
    shot_data = shot_data.merge(player_data, on="player_name", how='inner')

    # # On ajoute les données concernant le standings des équipes à shot_data
    # en réalisant une jointure interne sur les colonnes 'team_id' et 'game_date'
    # Pour cela, on convertit les colonnes 'game_date' des deux DataFrame en format datetime
    # afin d'avoir un format commun dans les deux colonnes
    if verbose:
        print("Ajout des données des équipes pour chaque tir...")
    shot_data['game_date'] = pd.to_datetime(shot_data['game_date'], format="%Y%m%d")
    ranking_data['game_date'] = pd.to_datetime(ranking_data['game_date'], format="%Y-%m-%d")
    ranking_data = ranking_data.drop('team_name', axis=1)
    shot_data = shot_data.merge(ranking_data, on=['team_id', 'game_date'], how='inner')
    
    # Sauvegarde dans un fichier csv 
    if write_to_file:
        merged_file = f"shot_data_merged_{season}.csv"
        transformed_data_path = os.path.join(database_path, "transformed_data")
        merged_file_path = os.path.join(transformed_data_path, merged_file)
        if verbose:
            print(f"Ecriture des données jointes dans le fichier '{merged_file}'")
        shot_data.to_csv(merged_file_path)
        
    return shot_data

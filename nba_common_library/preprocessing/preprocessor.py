# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 14:26:30 2023

@author: Raphael Sadoun
"""

# Importation des modules utilisés
import pandas as pd
from nba_common_library.utils.lib_string import *
from nba_common_library.utils.utils import get_path_file
from sklearn.preprocessing import OneHotEncoder

def preprocess_data(season=2019, verbose=True, write_to_file=True):
    
    """
    Fonction qui se charge d'appliquer les étapes de preprocessing spécifiques
    au jeu de données obtenu en sortie de l'étape de feature engineering : 
        
        - Prise en charge des valeurs manquantes
        - Conversion des variables numériques entières en type int
        - One hot encoding des variables catégorielles avec la fonction get_dummies de pandas
    
    """
    
    # Si le fichier existe déja, on se contente de charger les données dans un DataFrame
    # et de retourner ce dernier
    file_path = get_path_file(f"shot_data_merged_{season}_preprocessed.csv")
    if file_path is not None:
        return pd.read_csv(file_path, index_col=0)
      
    # Lecture du fichier contenant les données après étape de feature engineering
    file_fe = f"shot_data_merged_{season}_fe.csv"
    file_fe_path = get_path_file(file_fe)
    if verbose:
        print(f"Lecture du fichier '{file_fe}'...")
    df = pd.read_csv(file_fe_path, index_col=0)
    
    if verbose:
        print("Début des étapes de preprocessing...")

    # On ne garde que les colonnes utiles à la modélisation définies dans la liste 
    # 'useful_features' dans lib_string
    columns = useful_features+['shot_made_flag']
    df = df[columns]
    
    # Gestion des duplicata
    df = df.drop_duplicates()
    
    # Gestion des valeurs manquantes
    df = df.dropna()
    
    # On convertit en type int les variables censées être entières mais qui sont typées en float
    column_new_types = {'period': int,
                        'game_played': int,
                        'game_won': int,
                        'game_loss': int,
                        'is_at_home': int,
                        'score_margin': int,
                        '3pt_shot': int,
                        'quadrant': int
                        }
    df = df.astype(dtype = column_new_types)
    
    # On encode les variables catégorielles nominales avec un OneHotEncoder 
    # en conservant le nom des colonnes. La liste de ces variables est définie 
    # dans 'one_hot_features' dans lib_string.
    # encoder = OneHotEncoder(sparse=False, dtype='int')
    # encoder.fit(df[one_hot_features])
    # df_onehot = encoder.transform(df[one_hot_features])
    # df_onehot = pd.DataFrame(df_onehot, columns=encoder.get_feature_names_out(one_hot_features))
    # df = df.reset_index(drop=True)
    # df = df.join(df_onehot)
    # df = df.drop(one_hot_features, axis=1)
    
    df = pd.get_dummies(df)
    df = df.reset_index(drop=True)
    
    if verbose:
        print("Fin des étapes de preprocessing...")
        
    # Sauvegarde dans un fichier csv 
    if write_to_file:
        file = f"shot_data_merged_{season}_preprocessed.csv"
        transformed_data_path = os.path.join(database_path, "transformed_data")
        file_path = os.path.join(transformed_data_path, file)
        if verbose:
            print(f"Ecriture des données après preprocessing dans le fichier '{file}'")
        df.to_csv(file_path)
    
    return df
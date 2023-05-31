# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 15:01:57 2023

@author: Raphael Sadoun
"""

# Importation des modules utilisés
import pandas as pd
from nba_common_library.utils.lib_string import *
from nba_common_library.utils.utils import get_path_file
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler, NearMiss, ClusterCentroids


def resample_data(season=2019, method='rand_under', write_to_file=True, verbose=True):
    """
    Fonction qui applique un rééchantillonage des données pour améliorer l'équilibre de 
    la classe 0 et la classe 1 de la variable cible 'shot_made_flag'
    
    """

    # Si le fichier existe déja, on se contente de charger les données dans un DataFrame
    # et de retourner ce dernier
    file_path = get_path_file(f"shot_data_merged_{season}_{method}.csv")
    if file_path is not None:
        return pd.read_csv(file_path, index_col=0)

    # Lecture du fichier contenant les données après étape de preprocessing
    file = f'shot_data_merged_{season}_preprocessed.csv'
    file_path = get_path_file(file)
    if verbose:
        print(f"Lecture du fichier '{file}'...")
    df = pd.read_csv(file_path, index_col=0)
    X = df.drop('shot_made_flag', axis=1)
    y = df['shot_made_flag']

    if method == 'rand_under':
        resampler = RandomUnderSampler()
    elif method == 'near_miss':
        resampler = NearMiss()
    elif method == 'cluster_cent':
        resampler = ClusterCentroids()
    elif method == 'rand_over':
        resampler = RandomOverSampler()
    elif method == 'smote':
        resampler = SMOTE()
    else:
        print(f"La méthode resampling '{method}' n'est pas valide")
        return None

    # Rééchanillonage des données
    if verbose:
        resampler_name = str(resampler).split('(')[0]
        print(f"Rééchantillonage des données avec '{resampler_name}'...")
    X_resampled, y_resampled = resampler.fit_resample(X, y)
    df_resampled = pd.concat([X_resampled, y_resampled], axis=1)

    # Sauvegarde dans un fichier csv 
    if write_to_file:
        file = f"shot_data_merged_{season}_{method}.csv"
        transformed_data_path = os.path.join(database_path, "transformed_data")
        file_path = os.path.join(transformed_data_path, file)
        if verbose:
            print(f"Ecriture des données rééchantillonées dans le fichier '{file}'")
        df_resampled.to_csv(file_path)

    return df_resampled

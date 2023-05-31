# -*- coding: utf-8 -*-
"""
Created on 16/02/2023 17:54
@author: GiovanniMINGHELLI, RaphaëlSADOUN
"""

import pandas as pd
import os
from nba_common_library.utils.lib_string import *
from nba_common_library.utils.utils import *


def modify_column_names(directory_path, column_dict):
    """
    Modifie les noms de colonnes de tous les fichiers CSV dans un répertoire selon un dictionnaire de listes.

    :param directory_path:
    directory_path -- le chemin du répertoire contenant les fichiers CSV à modifier
    :param column_dict:
    column_dict -- un dictionnaire de listes spécifiant les nouveaux noms de colonnes

    Les clés du dictionnaire doivent correspondre aux nouveaux noms de colonnes.
    Les valeurs du dictionnaire doivent être des listes
    contenant les noms de colonnes existants à remplacer par la clé correspondante.
    """
    # Ouverture du fichier history stockant les fichiers déjà convertis
    text_file_path = os.path.join(project_path, nba_common_library, utils, 'history_rename.txt')
    with open(text_file_path, 'r') as f:
        already_converted_files = f.read().splitlines()[1:]

    # Génération de la liste de fichier à modifier
    file_list = [file for file in os.listdir(directory_path) if file not in already_converted_files
                 and file.endswith('.csv')]

    if not file_list:
        print('Aucun nouveau fichier à traiter')

    # Parcours de tous les fichiers dans le répertoire
    for n, filename in enumerate(file_list):
        n_files = len(file_list)
        if filename.endswith(".csv"):
            filepath = os.path.join(directory_path, filename)
            print("\n\nTraitement du fichier : ", filepath, f' {n:_>40}/{n_files}')

            # Chargement du fichier CSV en dataframe pandas
            df = pd.read_csv(filepath, low_memory=False)

            # Modification des noms de colonnes conformément au dictionnaire de listes fourni
            df = rename_columns(df, column_dict)

            # Sauvegarde du dataframe modifié en écrasant le fichier d'origine
            df.to_csv(filepath, index=False)
            print("Sauvegarde du fichier", filepath)

            # Ajout du fichier converti a history
            with open(text_file_path, 'a') as f:
                f.write(f"{filename}\n")


def rename_columns(dataframe: pd.DataFrame, column_dict):
    """
    Modifie les noms de colonnes de l'argument dataframe passé en entrée selon un dictionnaire de listes.

    -- dataframe : Un objet de type DataFrame
    -- column_dict : Un dictionnaire de listes spécifiant les nouveaux noms de colonnes

    Les clés du dictionnaire doivent correspondre aux nouveaux noms de colonnes.
    Les valeurs du dictionnaire doivent être des listes
    contenant les noms de colonnes existants à remplacer par la clé correspondante.
    """

    new_column_names = dict()
    for column in dataframe.columns:
        found_match = False
        for new_name, old_names in column_dict.items():
            if column in old_names:
                new_column_names[column] = new_name
                found_match = True
                break
        if not found_match:
            print(f"\nAucune correspondance trouvée pour la colonne '{column}' parmi '{dataframe.columns}'")
    return dataframe.rename(new_column_names, axis=1)


if __name__ == "__main__":
    modify_column_names(directory_path=database_path, column_dict=conventional_naming)

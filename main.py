# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 14:43:45 2023

@author:Selim KNEDIF, Giovanni MINGHELLI, Raphael SADOUN


"""

# Importation des modules utilisés
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from nba_common_library.feature_engine.feature_engineering import get_new_features
from nba_common_library.preprocessing.merge_data import merge_data_by_season
from nba_common_library.preprocessing.preprocessor import preprocess_data
from nba_common_library.modelling.model_choosen import *
from nba_common_library.modelling.parameters import *
from sklearn.metrics import make_scorer, recall_score


def recall_scored(y_true, y_pred):
    recall = recall_score(y_true, y_pred, pos_label=1)
    return recall


def main(model, param_grid={}, test_size=0.8,
         train_season=2019, test_season=2019,
         scaler=None, scoring='accuracy', cv=5):
    """
        Entrainement et (optionelle) optimisation d'un modèle de classification 
        pour la prédiction de la réussite des tirs de NBA.
        Les jeux d'entraînement et de test sont construits à partir des données agrégées des tirs 
        des joueurs sur les saisons NBA spécifiées en entrées.
        Retourne les jeux d'entrainements et de test ainsi que le modèle entraîné.
        
        - model : Un modèle de classification déja initialisé, ex: model = LogisticRegression()
        - param_grid : Un dictionnaire contenant les valeurs des hyperparamètres à considèrer 
                       lors de l'optimisation par validation croisée. Aucune optimisation n'est effectuée
                       si le dictionnaire passé est vide (valeur par défaut).
        - train_season : Entier ou liste d'entiers indiquant la ou les saisons de NBA 
                         à utiliser pour construire le jeu d'entraînement.
        - test_season :  Entier ou liste d'entiers indiquant la ou les saisons de NBA 
                         à utiliser pour construire le jeu de test.
        - test_size : Proportion des données à utiliser pour le jeu de test. N'est pas pris en compte si 
                      les arguments train_season et test_season décrits ci-dessus ne sont pas égaux.
        - scaler : Une instance de MinMaxScaler ou StandardScaler qui sera utilisée 
                   pour normaliser ou standardiser les données (None par défaut).
        - scoring : Le score à optimiser par validation croisée. Cet argument est passé tel quel 
                    à la fonction GridSearchCV de Scikit-learn (Valeur par défaut = 'accuracy')
        - cv : Argument passé tel quel à la fonction GridSearchCV de Scikit_learn
    
    """

    # Création du jeu d'entraînement
    train_list = []
    if type(train_season) is not list: train_season = [train_season]
    for season in list(train_season):
        df = merge_data_by_season(season=season)
        df = get_new_features(season=season)
        train_list.append(df)
    train = pd.concat(train_list, axis=0)

    # Création du jeu de test
    if train_season == test_season:
        X, y = preprocess_data(train)
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            test_size=test_size,
                                                            random_state=42)
    else:
        test_list = []
        if type(test_season) is not list: test_season = [test_season]
        for season in list(test_season):
            df = merge_data_by_season(season=season)
            df = get_new_features(season=season)
            test_list.append(df)
        test = pd.concat(test_list, axis=0)
        X_train, y_train = preprocess_data(train)
        X_test, y_test = preprocess_data(test)

    # Standardisation ou normalisation des données 
    if scaler is not None:
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    # Si une grille de paramètres a été donnée, on optimise les hyperparamètres du modèle par cross-validation
    if len(param_grid) != 0:
        grid = GridSearchCV(estimator=model, param_grid=param_grid, scoring=scoring, cv=cv)
        grid.fit(X_train, y_train)
        return X_train, X_test, X_test, y_test, grid
    else:
        model.fit(X_train, y_train)
        return X_train, X_test, y_train, y_test, model


if __name__ == '__main__':
    scorer = make_scorer(recall_scored)
    main(logistic_regression, ParamsDict.LR.getParams(), scoring=scorer)

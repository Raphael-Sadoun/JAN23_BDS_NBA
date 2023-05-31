# -*- coding: utf-8 -*-
"""
Created on 12/03/2023 19:04
@author: SelimKNEDIF
"""
import pandas as pd
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.metrics import make_scorer, recall_score


def recall_scored(y_true, y_pred):
    recall = recall_score(y_true, y_pred, pos_label=1)
    return recall


def optimizer(model, x_train, y_train, params, train_size=None, scoring=None):
    if train_size:
        x_train, _, y_train, _ = train_test_split(x_train, y_train, train_size=train_size, random_state=42)
    if scoring:
        scoring = make_scorer(scoring)

    grid_search = GridSearchCV(model, params, cv=KFold(n_splits=5, shuffle=True, random_state=42),
                               n_jobs=-1, verbose=1, scoring=scoring)
    grid_search.fit(x_train, y_train)
    return pd.DataFrame(grid_search.cv_results_)
# -*- coding: utf-8 -*-
"""
Created on 09/03/2023 19:59
@author: GiovanniMINGHELLI
"""
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, SelectFromModel, f_classif, \
    mutual_info_classif, RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.preprocessing import PolynomialFeatures
from sklearn.base import BaseEstimator, TransformerMixin
from nba_common_library.utils.lib_string import shot_made_flag, database_path, transformed_data
from nba_common_library.utils.utils import get_path_file
from lightgbm import LGBMClassifier



def select_best_polynomial_feature(X, y, order, n_best):
    X_poly = PolynomialFeatures(degree=order, include_bias=True).fit_transform(X)
    best_features = pd.DataFrame(X_poly).corrwith(pd.Series(y)).abs().sort_values(ascending=False).index[:n_best]
    best_features_df = pd.DataFrame(X_poly[:, best_features])
    best_features_df.columns = [f'poly_{i}' for i in range(len(best_features))]
    return pd.concat([pd.DataFrame(X), best_features_df], axis=1)


def select_Kbest_features(X, y, method: str, k: int):
    method_functions = {
        'f_classif': f_classif,
        'mutual_info_classif': mutual_info_classif}

    if method not in method_functions:
        raise ValueError(f"Invalid method: {method}")

    selector = SelectKBest(method_functions.get(method), k=k)
    selector.fit(X, y)
    return X.columns[selector.get_support()].tolist()


def selectFM_best_features(X, y, estimator=None, threshold: float = None):
    if estimator is None:
        estimator = RandomForestClassifier()
    selector = SelectFromModel(estimator, threshold=threshold)
    selector.fit(X, y)
    return X.columns[selector.get_support()].tolist()


def selectRFE_best_features(X, y, n_features_to_select: int, estimator=None):
    if estimator is None:
        estimator = RandomForestClassifier()
    selector = RFE(estimator, n_features_to_select=n_features_to_select)
    selector.fit(X, y)
    return X.columns[selector.get_support()].tolist()


def addPCA(X):
    df_pca = pd.DataFrame(PCA(0.95).fit_transform(X))
    df_pca.columns = [f'pca_{n}' for n in range(df_pca.shape[1])]
    return pd.concat([X, df_pca], axis=1)

def merge_lists(lists):
    return list(set().union(*lists))


def sort_by_presence(list_of_lists):
    flattened_list = [item for sublist in list_of_lists for item in sublist]
    counts = {item: flattened_list.count(item) for item in flattened_list}
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    sorted_list = [item[0] for item in sorted_items]
    return sorted_list


def feature_select(season: int = None, k: int = None):
    if not season:
        season = 2019
    processed_file = pd.read_csv(get_path_file(file=f'shot_data_merged_{season}_preprocessed.csv'), index_col=0)
    X, y = addPCA(processed_file.drop(shot_made_flag, axis=1)), processed_file[shot_made_flag]
    #X = select_best_polynomial_feature(X, y, order=3, n_best=15)
    anova = select_Kbest_features(X, y, 'f_classif', 25)
    mutual_info = select_Kbest_features(X, y, 'mutual_info_classif', 25)
    sfm = selectFM_best_features(X, y, estimator=RandomForestClassifier(), threshold=1e-4)
    rfe = selectRFE_best_features(X, y, estimator=RandomForestClassifier(), n_features_to_select=25)
    results = [anova, mutual_info, sfm, rfe]
    features = merge_lists(results)
    #if k and k < len(features):
    #    k = len(features)
    selected_features = X[sort_by_presence(results)[:k]] if k else X[merge_lists(results)]
    selected_features_with_target = pd.concat([y, selected_features], axis=1)
    selected_features_with_target.to_csv(os.path.join(database_path, transformed_data,
                                                      f'shot_data_merged_{season}_ready.csv'), index=False)
    return selected_features_with_target


class FeatureSelector(BaseEstimator, TransformerMixin):
    
    def __init__(self, k):
        #self.pca = PCA(0.95)
        self.selectors = [SelectKBest(score_func=f_classif, k=25),
                          SelectKBest(score_func=mutual_info_classif, k=25),
                          SelectFromModel(estimator=LGBMClassifier(),
                                          threshold=1e-4),
                          RFE(estimator=LGBMClassifier(),
                              n_features_to_select=25)]
        self.k = k
                          
    def fit(self, X, y):
        #self.pca.fit(X,y)
        #X_pca = pd.DataFrame(self.pca.transform(X), 
        #                     columns=[f'pca_{n}' for n in range(self.pca.n_components_)])
        #X = X.join(X_pca)
        for selector in self.selectors:
            selector.fit(X,y)
        return self
    
    def transform(self, X):
        #X_pca = pd.DataFrame(self.pca.transform(X), 
        #                     columns=[f'pca_{n}' for n in range(self.pca.n_components_)])
        #X = X.join(X_pca)
        results = []
        for selector in self.selectors:
            results.append(selector.feature_names_in_[selector.get_support()])        
        return X[sort_by_presence(results)[:self.k]]


if __name__ == '__main__':
    feature_select()

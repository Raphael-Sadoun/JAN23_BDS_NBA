# -*- coding: utf-8 -*-
"""
Created on 12/03/2023 23:09
@author: SelimKNEDIF
"""


from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier


logistic_regression = LogisticRegression()
knn = KNeighborsClassifier()
random_forest = RandomForestClassifier()
ada_boost = AdaBoostClassifier()
cat_boost = CatBoostClassifier()
xgb_boost = XGBClassifier()
lgbm = LGBMClassifier()

model_list = [logistic_regression, knn, random_forest, ada_boost, cat_boost, xgb_boost, lgbm]
model_names = [i.__class__.__name__ for i in model_list]
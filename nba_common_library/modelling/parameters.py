# -*- coding: utf-8 -*-
"""
Created on 12/03/2023 18:47
@author: SelimKNEDIF
"""

from enum import Enum

from sklearn.tree import DecisionTreeClassifier


class ParamsDict(Enum):
    LR = {'penalty': ['l1', 'l2', 'elasticnet', 'none'],
          'dual': [True, False],
          'tol': [1e-4, 1e-5, 1e-6],
          'C': [0.1, 1.0, 10.0],
          'fit_intercept': [True, False],
          'intercept_scaling': [1, 2, 3],
          'class_weight': [None, 'balanced'],
          'random_state': [42],
          'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
          'max_iter': [100, 200, 500],
          'multi_class': ['ovr', 'multinomial'],
          'verbose': [0, 1, 2],
          'warm_start': [True, False],
          'n_jobs': [-1]
          }

    KNN = {'n_neighbors': [3, 5, 7, 9],
           'weights': ['uniform', 'distance'],
           'algorithm': ['ball_tree', 'kd_tree', 'brute', 'auto'],
           'leaf_size': [10, 20, 30],
           'p': [1, 2],
           'metric': ['euclidean', 'manhattan', 'minkowski'],
           'n_jobs': [-1]}

    RANDOM_FOREST = {'n_estimators': [50, 100, 200, 400],
                     'criterion': ['gini', 'entropy'],
                     'max_depth': [10, 20, 30, None],
                     'min_samples_split': [2, 5, 10],
                     'min_samples_leaf': [1, 2, 4],
                     'max_features': ['auto', 'sqrt', 'log2', None],
                     'bootstrap': [True, False],
                     'oob_score': [True, False],
                     'n_jobs': [-1],
                     'random_state': [0],
                     'verbose': [0, 1, 2],
                     'warm_start': [True, False],
                     'class_weight': [None, 'balanced', 'balanced_subsample'],
                     'ccp_alpha': [0.0, 0.1, 0.5, 1.0],
                     'max_samples': [None, 0.5, 0.7, 0.9],
                     'min_weight_fraction_leaf': [0.0, 0.1, 0.2],
                     'min_impurity_decrease': [0.0, 0.1, 0.2],
                     'min_impurity_split': [None],
                     }

    CAT_BOOST = {'learning_rate': [0.01, 0.05, 0.1],
                 'iterations': [100, 200, 300],
                 'depth': [4, 6, 8],
                 'l2_leaf_reg': [1, 3, 5, 7],
                 'border_count': [32, 64, 128],
                 'bagging_temperature': [0, 1, 2],
                 'sampling_frequency': ['PerTree', 'PerTreeLevel', 'PerTreeGradient', 'PerFeature', 'PerFeatureLevel'],
                 'boosting_type': ['Ordered', 'Plain'],
                 'bootstrap_type': ['Bayesian', 'Bernoulli', 'MVS', 'Poisson'],
                 'min_data_in_leaf': [1, 3, 5, 7, 9],
                 'max_leaves': [31, 63, 127],
                 'grow_policy': ['SymmetricTree', 'Depthwise', 'Lossguide'],
                 'random_strength': [0.1, 0.5, 1, 5],
                 'one_hot_max_size': [2, 4, 8, 16],
                 'rsm': [0.5, 0.7, 1],
                 'leaf_estimation_iterations': [1, 3, 5],
                 'leaf_estimation_method': ['Newton', 'Gradient']
                 }

    XG_BOOST = {'max_depth': [3, 4, 5, 6, 7, 8, 9],
                'learning_rate': [0.01, 0.05, 0.1],
                'n_estimators': [50, 100, 200, 300],
                'gamma': [0, 0.1, 0.5, 1],
                'min_child_weight': [1, 3, 5, 7],
                'subsample': [0.5, 0.7, 0.9, 1],
                'colsample_bytree': [0.5, 0.7, 0.9, 1],
                'reg_alpha': [0, 0.1, 0.5, 1],
                'reg_lambda': [0, 0.1, 0.5, 1],
                'scale_pos_weight': [1, 2, 5, 10],
                'max_delta_step': [0, 1, 2],
                'tree_method': ['auto', 'exact', 'approx', 'hist', 'gpu_hist'],
                'validate_parameters': [True, False],
                'booster': ['gbtree', 'gblinear', 'dart'],
                'lambda_bias': [0, 0.1, 0.5, 1],
                'num_parallel_tree': [1, 2, 4, 8],
                'monotone_constraints': [None, [1, -1, 0]],
                }

    ADA_BOOST = {'base_estimator': [DecisionTreeClassifier(max_depth=i) for i in range(1, 5)],
                 'n_estimators': [50, 100, 200, 300],
                 'learning_rate': [0.01, 0.05, 0.1, 0.5, 1],
                 'algorithm': ['SAMME', 'SAMME.R'],
                 'random_state': [42],
                 'loss': ['linear', 'square', 'exponential']
                 }

    LGBM = {'boosting_type': ['gbdt', 'dart', 'goss'],
            'num_leaves': [10, 20, 30, 40, 50],
            'max_depth': [-1, 5, 10, 15, 20],
            'learning_rate': [0.01, 0.05, 0.1, 0.5, 1],
            'n_estimators': [50, 100, 200, 300],
            'objective': ['binary', 'multiclass'],
            'num_class': [2, 3, 4],
            'random_state': [42],
            'min_child_samples': [20, 30, 40, 50],
            'min_split_gain': [0.0, 0.1, 0.2, 0.3],
            'reg_alpha': [0.0, 0.1, 0.5, 1.0],
            'reg_lambda': [0.0, 0.1, 0.5, 1.0],
            'subsample': [0.5, 0.6, 0.7, 0.8, 0.9],
            'colsample_bytree': [0.5, 0.6, 0.7, 0.8, 0.9],
            }

    def getParams(self):
        return self.value



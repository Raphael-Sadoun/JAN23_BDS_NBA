# -*- coding: utf-8 -*-
"""
Created on 12/03/2023 20:50
@author: GiovanniMINGHELLI
"""


def outlier_thresholds(dataframe, cols_name, q1=0.25, q3=0.75):
    for col_name in cols_name:
        quartile1 = dataframe[col_name].quantile(q1)
        quartile3 = dataframe[col_name].quantile(q3)
        interquantile_range = quartile3 - quartile1
        up_limit = quartile3 + 1.5 * interquantile_range
        low_limit = quartile1 - 1.5 * interquantile_range
        if dataframe[(dataframe[col_name] > up_limit) | (dataframe[col_name] < low_limit)].any(axis=None):
            dataframe.loc[(dataframe[col_name] > up_limit), col_name] = up_limit
            dataframe.loc[(dataframe[col_name] < low_limit), col_name] = low_limit
    return dataframe

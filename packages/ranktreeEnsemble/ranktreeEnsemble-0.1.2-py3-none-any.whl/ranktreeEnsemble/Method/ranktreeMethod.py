#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Ruijie Yin (ruijieyin428@gmail.com), Chen Ye (cxy364@miami.edu) and Min Lu (m.lu6@umiami.edu)
# Description:
# Fast computing an ensemble of rank-based trees via boosting or random forest on binary and multi-class problems.
# It converts continuous gene expression profiles into ranked gene pairs,
# for which the variable importance indices are computed and adopted
# for dimension reduction.


import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
from numpy import sort
from sklearn.feature_selection import SelectFromModel
from shaphypetune import BoostSearch, BoostRFE, BoostRFA, BoostBoruta
import lightgbm as lgb
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from data.dataPrep import *

def rforest(train_x, train_y):
    """

    :param train_x: A data frame containing the predictor variables. The number of rows in train_x must be the same as the length of train_y.
    :param train_y: A vector of outcomes. The number of rows in train_x must be the same as the length of train_y.
    :return: A fitted Random Rank Forest model.
    """
    train_data_converted = pair(np.array(train_x))
    X_train = train_data_converted.astype('int64')
    y_train = train_y

    # define the model
    model = RandomForestClassifier()
    # fit the model on the whole dataset:
    fitted_model = model.fit(X_train, y_train)
    return (fitted_model)


# build a Boosting with Logitboost Cost model:

def rboost(train_x, train_y):
    """

    :param train_x: A data frame containing the predictor variables. The number of rows in train_x must be the same as the length of train_y.
    :param train_y: A vector of outcomes. The number of rows in train_x must be the same as the length of train_y.
    :return: A fitted Logitboost Cost model.
    """
    train_data_converted = pair(np.array(train_x))
    X_train = train_data_converted.astype('int64')
    y_train = train_y

    clf = GradientBoostingClassifier(n_estimators=200, max_depth=3, random_state=2).fit(X_train, y_train)
    return (clf)


def rboost_rfe(train_x, train_y, validation_size = 0.2):
    """

    :param train_x: A data frame containing the predictor variables. The number of rows in train_x must be the same as the length of train_y.
    :param train_y: A vector of outcomes. The number of rows in train_x must be the same as the length of train_y.
    :param validation_size: The proportion of train_x that should be used as validation set to determine the best parameter. Default value is 0.2 (20%).
    :return: A fitted Logitboost Cost model on the reduced dimension.
    """
    train_data_converted = pair(np.array(train_x))

    X_train = train_data_converted.astype('int64')
    y_train = train_y

    # get feature importance scores and eliminate unimportant features:
    model = GradientBoostingClassifier(n_estimators=100, random_state=2, max_depth=3).fit(X_train, y_train)

    f_importance_ = sort(model.feature_importances_)
    f_importance_greater_than_zero = f_importance_[f_importance_ != 0]
    selection = SelectFromModel(model, threshold=min(f_importance_greater_than_zero), prefit=True)

    select_X_train = pd.DataFrame(selection.transform(X_train))

    # get a validation set:
    sss = StratifiedShuffleSplit(n_splits=1, test_size=validation_size, random_state=2)
    split_gen = sss.split(select_X_train, y_train)
    train_index, validation_index = next(split_gen)

    X_train_temp = select_X_train[select_X_train.index.isin(train_index)]
    y_train_temp = y_train[y_train.index.isin(train_index)]
    X_validation = select_X_train[select_X_train.index.isin(validation_index)]
    y_validation = y_train[y_train.index.isin(validation_index)]

    # fit the final model
    rfe = BoostRFE(
        lgb.LGBMClassifier(),
        step=10, n_jobs=-1, verbose=1)
    fitted_model = rfe.fit(X_train_temp, y_train_temp, eval_set=[(X_validation, y_validation)])
    return (fitted_model)


# build a Boosting with Logitboost Cost model with forwardstage stepwise fitting:

def rboost_rfa(train_x, train_y, validation_size = 0.2):
    """

    :param train_x: A data frame containing the predictor variables. The number of rows in train_x must be the same as the length of train_y.
    :param train_y: A vector of outcomes. The number of rows in train_x must be the same as the length of train_y.
    :param validation_size: The proportion of train_x that should be used as validation set to determine the best parameter. Default value is 0.2 (20%).
    :return: A fitted Logitboost Cost model on the reduced dimension.
    """
    train_data_converted = pair(np.array(train_x))

    X_train = train_data_converted.astype('int64')
    y_train = train_y

    # get feature importance scores and eliminate unimportant features:
    model = GradientBoostingClassifier(n_estimators=100, random_state=2, max_depth=3).fit(X_train, y_train)

    f_importance_ = sort(model.feature_importances_)
    f_importance_greater_than_zero = f_importance_[f_importance_ != 0]
    selection = SelectFromModel(model, threshold=min(f_importance_greater_than_zero), prefit=True)

    select_X_train = pd.DataFrame(selection.transform(X_train))

    # get a validation set:
    sss = StratifiedShuffleSplit(n_splits=1, test_size=validation_size, random_state=2)
    split_gen = sss.split(select_X_train, y_train)
    train_index, validation_index = next(split_gen)

    X_train_temp = select_X_train[select_X_train.index.isin(train_index)]
    y_train_temp = y_train[y_train.index.isin(train_index)]
    X_validation = select_X_train[select_X_train.index.isin(validation_index)]
    y_validation = y_train[y_train.index.isin(validation_index)]

    # fit the final model
    rfa = BoostRFA(
        lgb.LGBMClassifier(),
        step=10, n_jobs=-1, verbose=1)
    fitted_model = rfa.fit(X_train_temp, y_train_temp, eval_set=[(X_validation, y_validation)])
    return (fitted_model)
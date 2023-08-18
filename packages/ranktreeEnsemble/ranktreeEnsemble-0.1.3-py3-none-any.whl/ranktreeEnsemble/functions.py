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


def pair(inputData):
    # inputData = np.array(inputData)
    input_raw = inputData
    # calculate number of rows
    nrow = inputData.shape[0]
    # calculate number of columns
    ncol = inputData.shape[1] - 1
    input_convert = []
    for i in range(ncol - 1):
        for j in range(i + 1, ncol):
            input_convert.append(np.multiply((input_raw[:, i] < input_raw[:, j]), 1))
            # print(' i: {} \n j: {}'.format(i, j))
    input_convertreshaped = np.reshape(input_convert, (-1, nrow)).T

    input_convert_ = np.concatenate((input_convertreshaped, np.reshape(input_raw[:, (ncol)],(nrow,-1))), axis=1)
    input_convert_ = pd.DataFrame(input_convert_)
    input_convert_.columns = input_convert_.columns.astype(str)

    input_convert_.rename(columns={input_convertreshaped.shape[1]: "subtype"}, inplace=True)
    return (input_convert_)




def rforest(train_x, train_y):
    train_data_converted = pair(np.array(train_x))


    X_train = train_data_converted.astype('int64')
    y_train = train_y

    # define the model
    model = RandomForestClassifier()
    # fit the model on the whole dataset:
    fitted_model = model.fit(X_train, y_train)
    return(fitted_model)


# build a Boosting with Logitboost Cost model:

def rboost(train_x, train_y):
    train_data_converted = pair(np.array(train_x))

    X_train = train_data_converted.iloc.astype('int64')
    y_train = train_y

    clf = GradientBoostingClassifier(n_estimators=200, max_depth=3, random_state=2).fit(X_train, y_train)
    return(clf)






def rboost_rfe(train_x, train_y):
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
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=2)
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
    return(fitted_model)
    


# build a Boosting with Logitboost Cost model with forwardstage stepwise fitting:

def rboost_rfa(train_x, train_y):
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
    sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=2)
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
    return(fitted_model)
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Ruijie Yin (ruijieyin428@gmail.com), Chen Ye (cxy364@miami.edu) and Min Lu (m.lu6@umiami.edu)
# Description:
# Fast computing an ensemble of rank-based trees via boosting or random forest on binary and multi-class problems.
# It converts continuous gene expression profiles into ranked gene pairs,
# for which the variable importance indices are computed and adopted
# for dimension reduction.

import pandas as pd
import numpy as np


def pair(inputData):
    """

    :param inputData: Preferably a panda data frame object. The rows are samples and the last column should be class labels.
    :return: A data frame in which each column is the converted values of the expression levels of a gene pair.
    """
    inputData = np.array(inputData)
    input_raw = inputData
    # calculate number of rows
    nrow = input_raw.shape[0]
    # calculate number of columns
    ncol = input_raw.shape[1] - 1
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




# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

import numpy as np, scipy.stats

from coppertop.pipe import *
from bones.ts.metatypes import BType
from coppertop.dm.core.types import N, num, matrix, pytuple, pydict, darray
from coppertop.dm.core.aggman import takeRowRemain, hjoin, numRows


OLSResult = BType('OLSResult: OLSResult & dstruct')

array_ = (N**num)&darray
matrix_ = matrix&darray

# OLS
# why replicate the work?
#   * because there are discrepancies between well-known tools
#   * I can condense many lines of code and classes into less than 100 lines or so - which is easier to read
#   * I can make terms really explicit
#   * we can see the provenance of the computations easily
#   * we often want a non-centered model / a model with no intercept and various packages confuse the maths of these
#   * we want to handle multicollinearity so may need SVD - other packages make assumptions here
#
# https://stats.stackexchange.com/questions/146804/difference-between-statsmodel-ols-and-scikit-linear-regression
#
# from https://stackoverflow.com/questions/54614157/scikit-learn-statsmodels-which-r-squared-is-correct
# scikit-learn doesn't have the focus we want, e.g. "the scikit-learn core developer who replies in the above
# thread casually admits that "I'm not super familiar with stats"...", and "In particular when using a test set,
# it's a bit unclear to me what the R^2 means."
#
# we'll use scipy - seems slightly more care has gone into it than numpy
# https://stackoverflow.com/questions/29372559/what-is-the-difference-between-numpy-linalg-lstsq-and-scipy-linalg-lstsq
#
# statsmodels uses a QR or the Moore-Penrose pseudoinverse to solve the least squares problem
# scipy uses an SVD which given we often want to handle multicollinearity this may be helpful for analysis / diagnosis
#
# CONFUSION AROUND DEGREES OF FREEDOM
# https://stackoverflow.com/questions/58497385/calculating-f-statistic-in-sklearn
# the above says dofResiduals is (N - K - 1), stats models says N - K
# from https://www.statsmodels.org/devel/generated/statsmodels.regression.linear_model.RegressionResults.html?highlight=rsquared
# Residual degrees of freedom. n - p - 1, if a constant is present. n - p if a constant is not included.
#
# R-SQUARED
# included for intuition and validation - see https://data.library.virginia.edu/is-r-squared-useless/
# https://www.statsmodels.org/devel/generated/statsmodels.regression.linear_model.RegressionResults.rsquared.html
# https://stackoverflow.com/questions/70179307/why-is-sklearn-r-squared-different-from-that-of-statsmodels-when-fit-intercept-f
# https://stackoverflow.com/questions/54614157/scikit-learn-statsmodels-which-r-squared-is-correct
#
# NESTED F-TEST
# maybe https://www.statsmodels.org/devel/generated/statsmodels.regression.linear_model.RegressionResults.compare_f_test.html#statsmodels.regression.linear_model.RegressionResults.compare_f_test

# NOMENCLATURE
# MSE - mean squared error, aka mean squared deviation (MSD)
#   = RSS / DoFResiduals = RSS divided by the number of degrees of freedom
# RSS - residual sum of squares, aka sum of squared residuals (SSR!! - don't use this term), aka the sum of squared
#       estimate of errors (SSE), aka SSres
# R2 - R squared, aka coefficient of determination
#   = 1 - SSres / SStot = SSreg / SStot
# TSS - total sum of squares, aka sum of squared totals (SST)
#   = sum((Y - YBar) ^ 2)       centered version
# SSR - sum square regression, aka SSreg
#   = sum((YHat - YBar) ^ 2)    centered version
# DoFResiduals = N - K
#
# F-stat = MSR / MSE = R2 / (1 - R2) * DoFResiduals / K
#
# sources
# https://en.wikipedia.org/wiki/Mean_squared_error#In_regression

@coppertop(style=nullary)
def ols(Y:matrix&darray, X:matrix&darray) -> OLSResult:
    return _ols(Y, X, {})

@coppertop(style=nullary)
def ols(Y: matrix & darray, X: matrix & darray, options:pydict) -> OLSResult:
    return _ols(Y, X, options)

def _ols(Y:matrix&darray, X:matrix&darray, options) -> OLSResult:
    addIntercept = options.get('addIntercept', False)
    X = np.append(np.ones((X.shape[0], 1)), X, axis=1) if addIntercept else X
    N, K = X.shape  # N is number of observations, K is number of betaHats, plus one for the intercept, YBar, if required
    resDoF = N - K
    betaHat, SSres, rank, s = scipy.linalg.lstsq(X, Y)        # uses svd under the hood
    # This example just following is horrible as the lhs matrix is treated as a collection of vectors
    # `np.array([[1], [2]]) + np.array([1, 2]) == np.array([2,3],[3,4])`
    # so until we've made np.array's +, - etc type safe we'll answer a column matrix
    # recalling that we answer xHat in A.xHat = b + e
    betaHat = (matrix&darray)(betaHat)
    # TODO in the future treat np.float64 as litnum (which weakens to num)
    # the type system whilst not preventing us from making mistakes it does constrain us to thoughtful architecture
    SSres = float(SSres)
    # YHat = X @ betaHat
    YBar = float(np.average(Y))
    centeredSStot = float(np.sum((Y - YBar) ** 2))
    uncenteredSStot = float(np.sum(Y ** 2))
    # SSreg = sum((YHat - YBar) ** 2)
    centeredSSreg = centeredSStot - SSres
    uncenteredSSreg = uncenteredSStot - SSres
    # if this is too much work we could make it optional and extend tStats etc to take X too
    invXTXDiag = np.linalg.inv(X.T @ X).diagonal()
    return OLSResult(dict(
        betaHat=betaHat, SSres=SSres, centeredSStot=centeredSStot, uncenteredSStot=uncenteredSStot,
        centeredSSreg=centeredSSreg, uncenteredSSreg=uncenteredSSreg, rank=rank, s=s, N=N, K=K, YBar=YBar,
        addedIntercept=addIntercept, resDoF=resDoF, invXTXDiag=invXTXDiag
    ))

@coppertop
def betaHat(res:OLSResult) -> matrix&darray:
    return res.betaHat

def _r2(res:OLSResult):
    return (res.centeredSSreg / res.centeredSStot) if res.addedIntercept else (res.uncenteredSSreg / res.uncenteredSStot)

@coppertop
def r2(res:OLSResult) -> num:
    return _r2(res)

def _tStats(res:OLSResult):
    mse = res.SSres / res.resDoF
    estVarOfBetaHat = mse * res.invXTXDiag
    return res.betaHat.reshape(res.K) / np.sqrt(estVarOfBetaHat)

@coppertop
def tStats(res:OLSResult) -> array_:
    return array_(_tStats(res))

@coppertop
def tVals(res:OLSResult) -> array_:
    tVals = [2 * (1 - scipy.stats.t.cdf(np.abs(tStat), res.resDoF)) for tStat in _tStats(res)]
    return array_(tVals)

def _fStat(res):
    return (r2 := _r2(res)) / (1 - r2) * res.resDoF / (res.K - (1 if res.addedIntercept else 0))

@coppertop
def fStat(res:OLSResult) -> num:
    return _fStat(res)

@coppertop
def fVal(res:OLSResult) -> num:
    return float(1 - scipy.stats.f.cdf(_fStat(res), res.K - 1, res.resDoF))

@coppertop
def fCrit(res:OLSResult, confidence) -> num:
    # https://stackoverflow.com/questions/39813470/f-test-with-python-finding-the-critical-value
    return float(scipy.stats.f.ppf(q=1-confidence, dfn=res.K - 1, dfd=res.resDoF))

@coppertop
def residuals(res:OLSResult, Y:matrix&darray, X:matrix&darray) -> array_:
    return array_((Y - X @ res.betaHat).reshape(Y.shape[0]))


@coppertop
def predictedR2(Y: matrix & darray, X: matrix & darray) -> pytuple:
    return _predictedR2(Y, X, {})

@coppertop
def predictedR2(Y: matrix & darray, X: matrix & darray, options) -> pytuple:
    return _predictedR2(Y, X, options)

def _predictedR2(Y: matrix & darray, X: matrix & darray, options) -> pytuple:
    addIntercept = options.get('addIntercept', False)
    betaHats = []
    errors = []
    r2 = []
    for i in range(Y >> numRows):
        y, Y_ = Y >> takeRowRemain >> i
        x, X_ = X >> takeRowRemain >> i
        lm = ols(Y_, X_, options)
        x = ((darray&matrix)(np.ones((1, 1))) >> hjoin >> x) if addIntercept else x
        betaHats.append(lm.betaHat)
        yHat = (x @ lm.betaHat)[0]
        errors.append(yHat - y[0])
        r2.append(_r2(lm))
    errors = np.array(errors)
    predictedSSres = sum(errors * errors)[0]
    lm = ols(Y, X, options)
    SStot = lm.centeredSStot if addIntercept else lm.uncenteredSStot
    predictedR2, meanModelR2, sdModelR2 = (SStot - predictedSSres) / SStot, np.mean(r2), np.std(r2)
    return predictedR2, meanModelR2, (meanModelR2 - predictedR2) / sdModelR2


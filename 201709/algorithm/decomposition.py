#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 01:05:57 2017

@author: misakawa
"""

import numpy as np
from sklearn.decomposition.pca import PCA
from sklearn.lda import LDA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest
# from scipy.stats import pearsonr
from sklearn.feature_selection import chi2,f_classif
# from minepy import MINE
# def MIC(X, y):
#      # Maximal Information Coefficient
#      base = MINE()
#      return np.array( [ (base.compute_score(x, y) or base.mic(), 0.5) for x in X.T ]).T
#      # just one kind of factor,
#      # but SelectKBest needs two factors to fit datas.
# def Pearsonr(X,y):
#     return np.array([pearsonr(x,y) for x in X.T]).T

def de_pca(X,y):
    dim = X.shape[1]
    de  = min(2000,dim)
    clf = PCA(n_components = de)
    _,x_mini,_,y_mini = train_test_split(X,y,test_size = 0.33)
    clf.fit(x_mini,y_mini)
    def _func(X1,X2):
        return clf.transform(X1), clf.transform(X2)
    return _func

def de_lda(X,y):
    """ lda """
    dim = X.shape[1]
    de  = min(2000,dim)
    clf = LDA(n_components = de)
    _,x_mini,_,y_mini = train_test_split(X,y,test_size = 0.33)
    clf.fit(x_mini,y_mini)
    def _func(X1,X2):
        return clf.transform(X1), clf.transform(X2)
    return _func

# def de_ps(X,y):
#     """ pearsonr method """
#     dim = X.shape[1]
#     de = min(2000,dim)
#     clf = SelectKBest(Pearsonr , k=de)
#     clf.fit(X,y)
#     def _func(X1,X2):
#         return clf.transform(X1),clf.transform(X2)
#     return _func

def de_rf(X,y):
    """random forest"""
    dim  = X.shape[1]
    de   = min(2000,dim)
    clf  = RandomForestClassifier(n_estimators=200)
    _,x_mini,_,y_mini = train_test_split(X,y,test_size = 0.33)
    clf.fit(x_mini,y_mini)
    index = np.argsort(clf.feature_importances_)[::-1][:de].astype(np.int32)
    def _func(X1,X2):
        return X1[:,index],X2[:,index]
    return _func

def de_c2(X,y):
    """ chi2 """
    dim  = X.shape[1]
    de   = min(2000,dim) 
    clf  = SelectKBest(chi2, k = de)
    clf.fit(X,y)
    def _func(X1,X2):
        return clf.transform(X1), clf.transform(X2)
    return _func

# def de_mic(X,y):
#     """ MIC """
#     dim  = X.shape[1]
#     de   = min(2000,dim) 
#     clf = SelectKBest(MIC, k=de)
#     clf.fit(X,y)
#     def _func(X1,X2):
#         return clf.transform(X1),clf.transform(X2)
#     return _func

def de_f_and_p_value(X,y):
    """ f&p value """
    dim = X.shape[1]
    de  = min(2000,dim)
    clf = SelectKBest(f_classif,k=de)
    clf.fit(X, y)
    def _func(X1,X2):
        return clf.transform(X1),clf.transform(X2)
    return _func

nameAssemble = list(filter(lambda x:x.startswith('de_'), globals()))


    
    
    
    

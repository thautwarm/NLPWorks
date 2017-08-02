

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 10:52:58 2017

@author: Thautwarm
import files
"""
from __future__ import division
import os
import sys
from functools import partial
from itertools import repeat
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from sklearn.cluster import MeanShift
from sklearn.cluster import Birch
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.dummy import DummyClassifier
from PyWekaMake import W2C as Word2Vec, makeX
from sklearn.externals import joblib
from sklearn.cross_validation import KFold, train_test_split
from sklearn.metrics import roc_auc_score





from .classifier import  cluster, wrap
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


methods = {'Birch': wrap(cluster, lazy_clf=wrap(Birch, n_clusters=2)),
           'DecisionTree': DecisionTreeClassifier,
           'ExtraTree': ExtraTreesClassifier,
           'KMeans': wrap(cluster, lazy_clf=wrap(KMeans, n_clusters=2)),
           'KNeighborsClassifier': KNeighborsClassifier,
           'MeanShift': MeanShift,
           'Naive_Bayes': GaussianNB,
           'RandomForest': RandomForestClassifier,
           'SVM-rbf': wrap(SVC, probability=True),
           'SVM-linear': wrap(SVC, kernel='linear', probability=True),
           'Dummy': DummyClassifier}

methods['Birch'].isCluster = True
methods['KMeans'].isCluster = True
methods['MeanShift'].isCluster = True


import json   
import numpy as np
import pandas as pd
haskmap=lambda *x:list(map(*x))
def unzip(aftersource):
    if isinstance(aftersource,None.__class__):
        return None
    if not aftersource:
        return dict()
    else:
        return aftersource
class W2C:
    def __init__(self,source):
        self.source=source
    def __getitem__(self,sentence1):
        if sentence1 in self.source:
            return self.source[sentence1]
        return dict()
    @staticmethod
    def load(sourcePath):
        f=open(sourcePath,'r')
        source=json.load(f)
        f.close()
        return W2C(source)
from functools import reduce
def makeX(dictArray1,dictArray2):
    N=len(dictArray1)
    Xall=np.hstack((dictArray1,dictArray2))
    sets=np.array( list(reduce(lambda x,y:x.union(set(y.keys())),Xall,set()))).astype(np.int)
    sets=np.sort(sets)
    X=np.zeros((len(Xall),len(sets)))
    indexRule=dict(zip(sets, np.argsort(sets)))
    getIndex=lambda x:indexRule[x]
    for i,x in enumerate(Xall):
        keys=np.array(list(x.keys())).astype(np.int)
        values=np.array(list(x.values())).astype(np.float)
        index=haskmap(getIndex,keys)
        X[i][index]=values
    return X[:N],X[N:]
    
    

    
        
    
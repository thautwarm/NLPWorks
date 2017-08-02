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
        for s in source:
            if len(source[s]):
                try:
                    source[s]=dict(zip(*source[s]))
                except:
                    print(source[s])
                    return BaseException
            else:
                source[s]=dict()
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
    if not any(sets):
        N2 = len(dictArray2)
        print(Warning("After dict merge there is no feature in common!!!The results later must be strange!"))
        return np.zeros( (N,1) ), np.zeros( (N2,1) )
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
    
    

    
        
    
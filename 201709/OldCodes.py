from functools import reduce
import numpy as np
hmap = lambda *x: list(map(*x))
def makeX(dictArray1, dictArray2):
    N=len(dictArray1)
    Xall=np.hstack((dictArray1, dictArray2))
    sets=np.array(list(reduce(lambda x, y: x.union(set(y.keys())), Xall, set()))).astype(np.int)
    if not any(sets):
        N2 = len(dictArray2)
        print(Warning("After dict merge there is no feature in common!!!The results later must be strange!"))
        return np.zeros((N, 1)), np.zeros((N2, 1))
    sets= np.sort(sets)
    X   = np.zeros((len(Xall), len(sets)))
    indexRule = dict(zip(sets, np.argsort(sets)))
    getIndex  = lambda x: indexRule[x]
    for i, x in enumerate(Xall):
        keys=np.array(list(x.keys())).astype(np.int)
        values=np.array(list(x.values())).astype(np.float)
        index=hmap(getIndex, keys)
        X[i][index]=values
    return X[:N], X[N:]






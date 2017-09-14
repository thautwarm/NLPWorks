import warnings ; warnings._setoption("ignore")
from ooutils.io import  dump, load
from scalable.core import fn, flatten
ettFile= 'entities'

try:
    res = load(ettFile)
except Exception: # any
    from DBPedia.dbpediaService import DBPediaSPARQL
    from Select import SelectCluster
    lst = flatten.noRecur.strict([DBPediaSPARQL.getFromCapitalChar(ch)
                        for ch in fn.map(lambda i:chr(i))
                                        ([i for i in range(ord('a'), ord('z')+1)])
                    ])
    res = SelectCluster(lst)
    dump(res, ettFile)






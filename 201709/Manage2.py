import warnings ; warnings._setoption("ignore")
from ooutils.io import  dump, load
ettFile= 'entities'

try:
    res = load(ettFile)
except Exception: # any
    from DBPedia.dbpediaService import DBPediaSPARQL
    from Select import SelectCluster
    from ooutils.io import DBPedia2WekaData
    grp = [chr(i) for i in range(ord('a'), ord('z')+1)]
    res = SelectCluster(lst = grp)
    dump(res, ettFile)
    DBPedia2WekaData(res, './weka')










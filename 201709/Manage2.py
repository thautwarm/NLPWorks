import warnings ; warnings._setoption("ignore")
from ooutils.io import  dump, load
import concurrent.futures.thread
ettFile= 'entities'
try:
    res = load(ettFile)
except Exception: # any
    from DBPedia.dbpediaService import DBPediaSPARQL
    from Select import SelectCluster, selectClusterCh
    from ooutils.io import DBPedia2WekaData
    from scalable.core import foreach, fn
    grp = [ (i, chr(ch)) for i, ch in enumerate(range(ord('a'), ord('z')+1))]
    res = [None for i in grp]
    def CharAction(tpl):
        idx, ch = tpl
        result = selectClusterCh(ch)
        res[idx] = result
    with concurrent.futures.thread.ThreadPoolExecutor(max_workers=26) as executor:
        executor.map(CharAction, grp)
    results = fn.reduce(lambda x,y: x.update(y) or x)(res)
    dump(results, ettFile)
    DBPedia2WekaData(results, './weka')

    # foreach(grp)(CharAction)
    # res = SelectCluster(lst = grp)
    # dump(res, ettFile)
    # DBPedia2WekaData(res, './weka')










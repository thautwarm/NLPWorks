import warnings ; warnings._setoption("ignore")
import concurrent.futures.thread
import pandas as pd
from ooutils.io import load, dump
ettFile= 'entities'
try:
    results = load(ettFile)
except Exception: # any
    from DBPedia.dbpediaService import DBPediaSPARQL
    from scalable.core import foreach, fn

    # pandas_cache, abst_index, onto_index = DBPediaSPARQL.GetEntityAbstPairsFromCapitalChar()
    # dump(pandas_cache, "pd_cache")
    # dump(abst_index, "abst_index")
    # dump(onto_index, "onto_index")
    # df = pd.DataFrame(pandas_cache)
    # s = groupBy(lambda x : x.group[0])( [df.loc[i] for i in range(df.shape[0])] )

    from Select import SelectCluster, selectClusterCh
    from ooutils.io import DBPedia2WekaData, dumpJson, dump
    from scalable.core import foreach, fn
    grp = [ chr(ch) for ch in range(ord('a'), ord('z')+1)]

    def CharAction(ch : str):
        result = selectClusterCh(ch, count_foreach=100, select_foreach=100)
        print(f"Finished {ch}.")
        return result
    with concurrent.futures.thread.ThreadPoolExecutor(max_workers=26) as executor:
        res = list(executor.map(CharAction, grp))
    dump(res, "res")
    results = fn.reduce(lambda x,y: x.update(y) or x)(res)
    dump(results, ettFile)
    print(len(results), ' ---- results')
    index, grouped_by_ontology = DBPedia2WekaData(results, './weka')
    dumpJson(index, "index.json")
    dump(grouped_by_ontology, "wekaBinarySource")

    foreach(grp)(CharAction)
    res = SelectCluster(lst = grp)
    dump(res, ettFile)
    DBPedia2WekaData(res, './weka')










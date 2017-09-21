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
    ontology_index = dict()
    abstract_index = dict()
    def CharAction(ch : str):
        selectClusterCh(ch, ontology_index, abstract_index, count_foreach=100, min_select=30, max_select=200)
        print(f"Finished {ch}.")
    with concurrent.futures.thread.ThreadPoolExecutor(max_workers=26) as executor:
        executor.map(CharAction, grp)
    dump(ontology_index, "ontology_index")
    dump(abstract_index, "abstract_index")
    DBPedia2WekaData(ontology_index, abstract_index, './weka')










import warnings ; warnings._setoption("ignore")
import concurrent.futures.thread
from ooutils.io import load, DBPedia2WekaData
try:
    ontology_index = load("ontology_index")
    abstract_index = load("abstract_index")
except Exception: # any
    from DBPedia.dbpediaService import DBPediaSPARQL
    from scalable.core import foreach, fn

    from Select import SelectCluster, selectClusterCh
    from ooutils.io import dumpJson, dump
    from scalable.core import foreach, fn
    grp = [ chr(ch) for ch in range(ord('a'), ord('z')+1)]
    ontology_index = dict()
    abstract_index = dict()
    def CharAction(ch : str):
        return selectClusterCh(ch, ontology_index, abstract_index, count_foreach=100, min_select=30, max_select=200)
    with concurrent.futures.thread.ThreadPoolExecutor(max_workers=26) as executor:
        entities = fn.reduce(lambda x,y: x+y)(executor.map(CharAction, grp))
    dump(entities,'entities')
    dump(ontology_index, "ontology_index")
    dump(abstract_index, "abstract_index")

DBPedia2WekaData(ontology_index, abstract_index, './weka')










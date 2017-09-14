import warnings ; warnings._setoption("ignore")
from scalable.core import groupBy, fn, foreach
from ooutils.io import  dump, load
import os

prefix = r"http://dbpedia.org/ontology"
lstFile= 'ontologyList'
ettFile= 'entities'
try:
    lst = load(lstFile)
except Exception: # any
    from DBPedia.dbpediaService import DBPediaSPARQL
    lst    =  list(fn.map(lambda x: x[len(prefix)+1:])(DBPediaSPARQL.getClasses()))
    dump(lst, lstFile)


try:
    entities = load(ettFile)
except Exception: #any
    grp      = groupBy(lambda name: name[0].lower())(lst)
    from Select import selectOntology
    entities = selectOntology(grp)
    dump(entities, "entities")


name     = 0
abstract = 1
from typing import Tuple, List, Dict
def genWekaData(entities: Dict[str, List[Tuple[str, str]]], char):

    these_entities = entities[char]
    directory = f"./WekaData/{char}"
    try:
        os.makedirs(directory)
    except:pass
    for entity in these_entities:
        filename = f"{directory}/{entity[name]}"
        print(f"dealing {entity[name]} ... ")
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(entity[abstract].lower())
        except Exception as e:
            with open("log", 'a', encoding='utf-8' ) as error_deal:
                error_deal.write(f"entity name : {entity[name]} {e} \n")


foreach(lambda char: genWekaData(entities, char))(entities)










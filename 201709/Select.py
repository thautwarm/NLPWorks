
# 从首字母不同的ontology组里, 分别抽取100个实例的abstract作为数据集.

from collections import  defaultdict
from DBPedia.dbpediaService import DBPediaSPARQL
import warnings
from random import shuffle
import math


def selectOntology(group : "dict[str:char->list[str:ontology]])", cache_from_ontology_to_select=40, to_select = 2600) \
        -> "dict[str:char->set[(str: entity, str: Abstract)]]":
    ontology_cache = defaultdict(list)
    entities       = defaultdict(set)
    each_group_num = math.ceil(to_select/len(group))
    threshold      = int(each_group_num/10)
    print('===========get data.===========')
    for group_name, ontologies in group.items():
        print(f'   {group_name}')
        shuffle(ontologies)
        select_num = each_group_num if len(ontologies) < threshold else cache_from_ontology_to_select
        for ontology in ontologies:
            ontology_cache[group_name].extend(DBPediaSPARQL.getAbstract(ontology, select_num))
            print(f'   -- {ontology}')
        if len(ontology_cache[group_name]) < 100:
            warnings.warn(f"group[{group_name}] is less than 100!")
    total          = 0
    left           = 0
    while total < to_select:
        print('===========select cycle 1.===========')
        for group_name, cache in list(ontology_cache.items()):
            print(f'   {group_name}')
            shuffle(cache)
            n    = len(cache)
            if n > each_group_num:
                n    =  each_group_num+ min(left, n-each_group_num)
                left -= n-each_group_num
            else:
                left += each_group_num-n
            total += n
            entities[group_name].update(cache[:n])
            ontology_cache[group_name] = cache[n:]
    return entities



















        
        
        







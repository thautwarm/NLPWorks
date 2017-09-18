
# 从首字母不同的ontology组里, 分别抽取100个实例的abstract作为数据集.

from collections import  defaultdict
from DBPedia.dbpediaService import DBPediaSPARQL
import warnings
from random import shuffle
import math
from typing import List, Dict, Any, Callable
from scalable.core import fn


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


def selectClusterCh(ch:str, func:Callable[[str],List[str]] = DBPediaSPARQL.getFromCapitalChar,count_foreach = 100, select_foreach = 200) -> Dict[str, str]:
    def _f1(char:chr):
        print(char)
        return func(char, limit=count_foreach*10)
    def _f2(ent:str) -> Dict[str, Dict[str, Any]]:
        return DBPediaSPARQL.getRelatedWithAbstractFromEntity(ent, select_foreach)
    entities = _f1(ch)
    ret = dict()
    _count=0
    for entity in entities:
        try:
            r=_f2(entity)
        except Exception as e:
            print(e)
            continue
        if r is None:
            continue
        ret[entity]=r
        _count+=1
        if _count == count_foreach: break
    else:
        warnings.warn(f"Not Enough entities for group[{ch}]")
    return ret


def SelectCluster(lst : List[str], func:Callable[[str],List[str]] = DBPediaSPARQL.getFromCapitalChar, count_foreach = 100, select_foreach = 200) -> Dict[str, Dict[str, str]]:
    print("SelectCluster")
    def _f1(char:chr):
        print(char)
        return func(char, limit=count_foreach*10)

    def _f2(ent:str) -> Dict[str, Dict[str, Any]]:
        return DBPediaSPARQL.getRelatedWithAbstractFromEntity(ent, select_foreach)
    ret = dict()
    for ch in lst:
        entities = _f1(ch)
        _count   = 0
        for entity in entities:
            try:
               r = _f2(entity)
            except:continue
            if r is None:
                continue
            ret[entity] = r
            _count += 1
            if _count==count_foreach: break
        else:
            warnings.warn(f"Not Enough entities for group[{ch}]")
    return ret






















        
        
        







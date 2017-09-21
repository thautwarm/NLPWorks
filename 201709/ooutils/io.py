import pickle, os, json
from collections import defaultdict
from typing import Dict, Any, Tuple, List
def dump(obj, filename):
    try:
        with open(filename, 'wb') as write:
            pickle.dump(obj, write)
        return True
    except Exception as e:
        print(e)
        return False

def load(filename):
    try:
        with open(filename, 'rb') as read:
            ret = pickle.load(read)
    except Exception as e:
        raise e
    return ret

def dumpJson(obj, filename):
    with open(filename, 'w') as jsonFile:
        json.dump(obj, jsonFile)
def loadJson(filename):
    with open(filename, 'r') as jsonFile:
        obj = json.load(jsonFile)
    return obj

def DBPedia2WekaData(ontology_index:Dict[str, set], abstract_index: Dict[str, str], path:str):

    for entity,ontologies in ontology_index.items():
        for ontology in ontologies:
            directory = f"{path}/{ontology}"
            try:
                os.makedirs(directory)
            except:pass
            try:
                abstract = abstract_index[entity]
                with open(f'{directory}/{entity}.txt','w', encoding='utf8') as file:
                    file.write(abstract)
            except Exception as e:
                print(e)




# def DBPedia2WekaData(dictionary:Dict[str, Dict[str, Dict[str, Any]]], path:str) -> Tuple[Dict[str,List[str]], Dict[str, Tuple[str, str]]]:
#     grouped_by_ontology=defaultdict(set)
#     index = defaultdict(set)
#     for entity_name, entity_struct in dictionary.items():
#         for related_entity, entity in entity_struct.items():
#             index[related_entity].update(entity['ontology'])
#             for ontology in entity['ontology']:
#                 grouped_by_ontology[ontology].add((related_entity, entity['abstract']))
#     index = {key:list(index[key]) for key in index}
#     os.makedirs(path)
#     with open(f'./index.json', 'w') as jsonFile:
#         json.dump(dict(index), jsonFile)
#     for ontology, entities in grouped_by_ontology.items():
#         directory=f"{path}/{ontology}"
#         os.makedirs(directory)
#         for (name, abstract) in entities:
#             with open(f"{directory}/{name}", 'w', encoding='utf8') as file:
#                 file.write(abstract)
#     return index, grouped_by_ontology
#





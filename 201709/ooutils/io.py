import pickle, os, json
from collections import defaultdict
from typing import Dict, Any
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

def DBPedia2WekaData(dictionary:Dict[str, Dict[str, Dict[str, Any]]], path) -> None:
    """
    :param dictionary: Dict[entity, Dict[related_entity, Dict[property, value]]]
    :return:
    """

    try:
        os.makedirs(path)
    except:pass
    index = defaultdict(set)
    for entity_name, entity_struct in dictionary.items():
        directory = f"{path}/{entity_name}"
        try:
            os.makedirs(directory)
        except:pass
        for related_entity, entity in entity_struct.items():
            index[related_entity].update(entity['ontology'])
            with open(f"{directory}/{related_entity}", 'w', encoding='utf8') as file:
                file.write(entity['abstract'])
    index = {key:list(index[key]) for key in index}
    with open('./index.json', 'w') as jsonFile:
        json.dump(dict(index), jsonFile)
    return index


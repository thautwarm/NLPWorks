# -*- coding: utf-8 -*-
"""
Created on Sun May 28 23:18:12 2017

@author: thautwarm
"""
from typing import Dict, List, Tuple, Any, Set
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
def beginWith(Astr, begin):
    return Astr[:len(begin)] == begin


headerLength=len("http://dbpedia.org/resource/")
ontologyheaderLength = len('http://dbpedia.org/ontology/')


class DBPediaSPARQL:


    @staticmethod
    def getClasses() -> List[str]:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        body= \
            """
        SELECT * 
        FROM <http://dbpedia.org>
        { ?x a owl:Class }
        """
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)
        sparql.setRequestMethod("POST")
        results=sparql.query().convert()
        Ret=[]
        for result in results["results"]["bindings"]:
            Ret.append(result["x"]["value"])
        return Ret
    @staticmethod
    def CountEntitiesOfType(Type: str) -> int:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        body= f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT (COUNT(?resource) AS ?count)
        WHERE {{?resource a dbo:{Type} }}
        """
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)
        results=sparql.query().convert()
        return int(results["results"]["bindings"][0]["count"]["value"])

    @staticmethod
    def getFromCapitalChar(ch, limit = 250) -> List[str]:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setMethod("POST")
        body = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        SELECT  DISTINCT ?entity
                WHERE{{ ?entity ?p ?type
                       FILTER regex(?entity, "http://dbpedia.org/resource/{ch}([a-zA-Z0-9_]*)$", "i") .
                }}
                LIMIT {limit}
        """
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        Ret=[]
        for result in results["results"]["bindings"]:
            Ret.append(result["entity"]["value"][headerLength:])
        return Ret


    @staticmethod
    def getEntitiesFromType(Type:str, limit=200) -> List[str]:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setMethod("POST")
        body = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        SELECT  DISTINCT ?resource 
            WHERE {{ ?resource ?g dbo:{Type} 
            FILTER regex(?resource, "http://dbpedia.org/resource/(?!Category:)", "i") 
            }} Limit {limit}
        """
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        Ret=[]
        for result in results["results"]["bindings"]:
            Ret.append(result["resource"]["value"][headerLength:])
        return Ret



    @staticmethod
    def getAbstractFromOntology(ontology : str, limit=1000) -> List[Tuple[str, str, str]]:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setMethod("POST")
        body= f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?resource ?abstract ?type
        WHERE {{ ?resource a dbo:{ontology} . ?resource dbo:abstract ?abstract .
               OPTIONAL {{ ?resource a ?type . ?type owl:sameAs? dbo:{ontology} }}
        FILTER (lang(?abstract) = 'en')
        }} LIMIT {limit} 
        """
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        Ret=[]
        for result in results["results"]["bindings"]:
            Ret.append(
                (result["type"]    ["value"][ontologyheaderLength:],
                 result["resource"]["value"][headerLength:],
                 result["abstract"]["value"])
            )
        return Ret

    @staticmethod
    def getRelated(entity:str, limit = 200) -> List[str]:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setMethod("POST")
        body = f"""
        SELECT  ?dbr  
        WHERE {{ 
                <http://dbpedia.org/resource/{entity}> ?e ?dbr
                FILTER regex(?dbr, "http://dbpedia.org/resource/(?!Category:)", "i") 
              }}
        LIMIT {limit}
        """
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        Ret=[]
        for result in results["results"]["bindings"]:
            Ret.append(result["dbr"]["value"][headerLength:])
        return Ret

    @staticmethod
    def getRelatedWithAbstractFromEntity(entity:str, ontology_index ,abstract_index, min_select = 30, max_select = 200) -> Tuple[Set[str],Set[str]]:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setMethod("POST")
        body = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        SELECT ?res ?type ?abstract
        where{{
            <http://dbpedia.org/resource/{entity}> ?property ?res . ?res dbo:abstract ?abstract . ?res a ?type
            FILTER (lang(?abstract) = 'en') . 
            FILTER regex(?res, "http://dbpedia.org/resource/(?!Category:)", "i")  .
            FILTER regex(?type, "http://dbpedia.org/ontology/", "i") .
            FILTER regex(?res,  "http://dbpedia.org/resource/([a-zA-Z0-9_]+)$","i") 
        }}
        LIMIT {max_select}
        """
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        num     = len(set([results['res']['value'] for results in results['results']['bindings']]))
        if num < min_select:
            return None
        related_entities = set()
        onto_refered     = set()
        for result in results["results"]["bindings"]:
            res      = result["res"]["value"][headerLength:]
            ontology = result['type']['value'][ontologyheaderLength:]
            onto_refered.add(ontology)
            related_entities.add(res)
            if res not in ontology_index:
                ontology_index[res] = {ontology}
            else:
                ontology_index[res].add(ontology)
            if res not in abstract_index:
                abstract_index[res] = result["abstract"]["value"]

        return related_entities, onto_refered

    @staticmethod
    def GetEntityAbstPairsFromCapitalChar():
        sparql=SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setMethod("POST")
        body = \
        """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        SELECT DISTINCT ?entity ?res ?type ?abstract
        where{
            ?entity ?property1 ?onto .
            ?entity ?property2 ?res  . 
            ?res dbo:abstract ?abstract .
            ?res a ?type
            FILTER (lang(?abstract) = 'en') . 
            FILTER regex(?entity, "http://dbpedia.org/resource/[a-zA-Z]", "i")
            FILTER regex(?res, "http://dbpedia.org/resource/(?!Category:)", "i")  .
            FILTER regex(?type, "http://dbpedia.org/ontology/", "i") .
            FILTER regex(?res,  "http://dbpedia.org/resource/([a-zA-Z0-9_]+)$","i") 
        }
        LIMIT 30000
        """
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)
        results  = sparql.query().convert()
        bindings = results["results"]["bindings"]
        pandas_cache  = defaultdict(list)
        abstract_index = dict()
        ontology_index = dict()
        for result in bindings:
            entity   = result['res']   ['value'][headerLength:]
            ontology = result['type']  ['value'][headerLength:]
            pandas_cache['group'] .append(result['entity']['value'][headerLength:])
            pandas_cache['entity']  .append(entity)
            pandas_cache['ontology'].append(ontology)
            if entity not in abstract_index:
                abstract=result['abstract']['value']
                abstract_index[entity] = abstract
            if entity not in ontology_index:
                ontology_index[entity] = {ontology}
            else:
                ontology_index[entity].add(ontology)
        return pandas_cache, abstract_index, ontology_index






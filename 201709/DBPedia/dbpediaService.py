# -*- coding: utf-8 -*-
"""
Created on Sun May 28 23:18:12 2017

@author: thautwarm
"""
from SPARQLWrapper import SPARQLWrapper, JSON
def beginWith(Astr, begin):
    return Astr[:len(begin)] == begin


headerLength=len("http://dbpedia.org/resource/")


class DBPediaSPARQL:
    @staticmethod
    def getClasses():
        sparql=SPARQLWrapper("http://dbpedia.org/sparql")
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
    def CountEntitiesOfType(Type: str):
        sparql=SPARQLWrapper("http://dbpedia.org/sparql")
        body= \
            """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT (COUNT(?resource) AS ?count)
        WHERE {{?resource a dbo:{Type} }}
        """.format(Type=Type)
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)
        results=sparql.query().convert()
        return int(results["results"]["bindings"][0]["count"]["value"])

    @staticmethod
    def getAbstract(item, limit=1000):
        sparql=SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setMethod("POST")
        body= \
            """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT DISTINCT ?resource ?abstract ?type
        WHERE {{ ?resource a dbo:{item} . ?resource dbo:abstract ?abstract .
               OPTIONAL {{ ?resource a ?type . ?type owl:sameAs? dbo:{item} }}
        FILTER (lang(?abstract) = 'en')
        }} LIMIT {limit} 
        """.format(item=item, limit=limit)
        sparql.setQuery(body)
        sparql.setReturnFormat(JSON)

        results=sparql.query().convert()
        Ret=[]
        for result in results["results"]["bindings"]:
            Ret.append(
                (result["resource"]["value"][headerLength:], result["abstract"]["value"])
            )
        return Ret

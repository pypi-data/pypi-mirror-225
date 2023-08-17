# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

class AnzoQueryBuilder():
    @staticmethod
    def activeGraphmarts() -> str:
        return """
        SELECT ?gmart ?title
        FROM <http://cambridgesemantics.com/datasource/SystemTables/Graphmarts>
        WHERE {{
            GRAPH ?g {{
                ?gmart a <http://cambridgesemantics.com/ontologies/GraphmartStatus#GraphmartStatus> ;
                <http://cambridgesemantics.com/ontologies/GraphmartStatus#status> <http://openanzo.org/ontologies/2008/07/System#Online> ;
                <http://purl.org/dc/elements/1.1/title> ?title .
            }}
        }}"""

    @staticmethod
    def activeLayers(graphmart: str) -> str:
        return """
            SELECT distinct ?layer ?title ?index
            FROM <http://openanzo.org/namedGraphs/reserved/graphs/ALL>
            where
            { <""" + graphmart + """> a <http://cambridgesemantics.com/ontologies/Graphmarts#Graphmart> ;
                            <http://cambridgesemantics.com/ontologies/Graphmarts#layer> ?orderedItem .
                            ?orderedItem <http://openanzo.org/ontologies/2008/07/Anzo#orderedValue> ?layer . 
                            ?layer <http://cambridgesemantics.com/ontologies/Graphmarts#enabled> "true"^^<http://www.w3.org/2001/XMLSchema#boolean> ;
                            <http://purl.org/dc/elements/1.1/title> ?title .
              ?orderedItem <http://openanzo.org/ontologies/2008/07/Anzo#index> ?index .
            }

            """

    @staticmethod
    def list_instances() -> str:
        return """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT (COUNT(DISTINCT(?s)) as ?instanceCount) ?classLabel ?classUri
            WHERE {
                ?s a ?classUri .
                ?classUri rdfs:label ?classLabel .
            } GROUP BY ?classUri ?classLabel ORDER BY DESC(?instanceCount) LIMIT 1000
            """

    @staticmethod
    def list_properties(class_uri: str) -> str:
        return """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX os: <http://cambridgesemantics.com/ontologies/2008/07/OntologyService#>
            SELECT ?instanceCount ?propertyLabel ?property ?sampleValue (GROUP_CONCAT(DISTINCT ?range; SEPARATOR=", ") as ?propertyRange)
            WHERE {
                {
                    select ?property (SAMPLE(?o) as ?sampleValue) (COUNT(DISTINCT(?s)) as ?instanceCount)
                    where {
                        ?s a <""" + class_uri + """> ;
                            ?property ?o .
                    } GROUP BY ?property
                }
                OPTIONAL {
                    ?frameProperty os:ontologyProperty ?property ;
                        os:propertyRange ?range ;
                        rdfs:label ?propertyLabel ;
                .
                }
            } GROUP BY ?property  ?propertyLabel ?sampleValue ?instanceCount ORDER BY DESC(?instanceCount) LIMIT 1000
            """

    @staticmethod
    def find_statements(subj: str, pred: str, obj: str) -> str:
        return """
            SELECT *
            WHERE {{
                ?s ?p ?o
                {}
                {}
                {}
            }}
            """.format(subj, pred, obj)

from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("group-concat-by-type", '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (CONCAT(STR(?type), ":", GROUP_CONCAT(?name; separator=",")) AS ?value) WHERE { ?s a ?type ; ex:name ?name } GROUP BY ?type ORDER BY ?value''', 2)


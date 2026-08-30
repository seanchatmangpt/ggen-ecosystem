from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ascending-name-rank", '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s a ex:Thing ; ex:name ?value ; ex:rank ?rank } ORDER BY ASC(?rank)''', 2)


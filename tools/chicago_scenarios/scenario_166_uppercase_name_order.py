from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("uppercase-name-order", '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (UCASE(?name) AS ?value) WHERE { ?s ex:name ?name } ORDER BY DESC(?value)''', 3)


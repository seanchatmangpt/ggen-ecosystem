from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("not-exists-missing-property", '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value FILTER NOT EXISTS { ?s ex:missing ?missing } } ORDER BY ?value''', 3)


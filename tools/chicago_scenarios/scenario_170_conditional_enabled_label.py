from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("conditional-enabled-label", '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (IF(?enabled, CONCAT(?name, ":on"), CONCAT(?name, ":off")) AS ?value) WHERE { ?s ex:name ?name ; ex:enabled ?enabled } ORDER BY ?value''', 3)


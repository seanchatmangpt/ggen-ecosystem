from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("rank-equality-and-enabled", '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value ; ex:rank ?rank ; ex:enabled ?enabled FILTER(?rank = 1 && ?enabled = true) } ORDER BY ?value''', 1)


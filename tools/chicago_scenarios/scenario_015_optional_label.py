from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("optional-label", '''PREFIX sh: <http://www.w3.org/ns/shacl#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?value WHERE { ?s a sh:NodeShape . OPTIONAL { ?s rdfs:label ?value } } ORDER BY ?value''', 2)

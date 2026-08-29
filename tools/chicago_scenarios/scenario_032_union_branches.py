from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("union-branches", '''PREFIX sh: <http://www.w3.org/ns/shacl#> PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { { ?value a sh:NodeShape } UNION { ?value a ex:Thing } } ORDER BY ?value''', 4)

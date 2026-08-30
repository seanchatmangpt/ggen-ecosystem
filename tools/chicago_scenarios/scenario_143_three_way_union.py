from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("three-way-union", '''PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { { ?value a sh:NodeShape } UNION { ?value a ex:Thing } UNION { ?value a ex:Other } } ORDER BY ?value''', 5)


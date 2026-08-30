from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("union-resource-types", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { { ?value a ex:Thing } UNION { ?value a ex:Other } } ORDER BY ?value''', 3)

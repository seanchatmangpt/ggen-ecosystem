from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("inverse-name-path", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?value ^ex:name ?name } ORDER BY ?value''', 3)

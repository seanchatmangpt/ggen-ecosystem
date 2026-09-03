from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-200-inverse-name-path", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?value ^ex:name ?name } ORDER BY ?value''', 3)

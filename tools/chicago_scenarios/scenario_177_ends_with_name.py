from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-177-ends-with-name", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value . FILTER(STRENDS(?value, "a")) } ORDER BY ?value''', 3)

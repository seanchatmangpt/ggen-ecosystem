from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("contains-name", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value . FILTER(CONTAINS(?value, "a")) } ORDER BY ?value''', 3)

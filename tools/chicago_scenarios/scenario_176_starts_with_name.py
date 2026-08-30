from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-176-starts-with-name", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value . FILTER(STRSTARTS(?value, "A") || STRSTARTS(?value, "B")) } ORDER BY ?value''', 2)

from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-159-filter-boolean-not", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value ; ex:enabled ?enabled . FILTER(!?enabled) } ORDER BY ?value''', 1)

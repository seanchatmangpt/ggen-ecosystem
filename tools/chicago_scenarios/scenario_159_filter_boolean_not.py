from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("filter-boolean-not", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value ; ex:enabled ?enabled . FILTER(!?enabled) }''', 1)

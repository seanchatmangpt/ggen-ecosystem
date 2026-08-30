from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("descending-rank-order", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:rank ?value } ORDER BY DESC(?value)''', 3)

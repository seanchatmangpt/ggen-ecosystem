from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-194-ascending-rank-order", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:rank ?value } ORDER BY ASC(?value)''', 3)

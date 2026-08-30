from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("average-ranks", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT (AVG(?rank) AS ?value) WHERE { ?s ex:rank ?rank }''', 1)

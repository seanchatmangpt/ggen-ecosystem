from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("sum-ranks", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT (SUM(?rank) AS ?value) WHERE { ?s ex:rank ?rank }''', 1)

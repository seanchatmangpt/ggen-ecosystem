from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-185-sum-ranks", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT (SUM(?rank) AS ?value) WHERE { ?s ex:rank ?rank }''', 1)

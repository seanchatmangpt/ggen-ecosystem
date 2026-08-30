from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-187-minimum-rank", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT (MIN(?rank) AS ?value) WHERE { ?s ex:rank ?rank }''', 1)

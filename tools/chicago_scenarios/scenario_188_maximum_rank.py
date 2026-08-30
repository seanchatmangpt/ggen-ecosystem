from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("maximum-rank", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT (MAX(?rank) AS ?value) WHERE { ?s ex:rank ?rank }''', 1)

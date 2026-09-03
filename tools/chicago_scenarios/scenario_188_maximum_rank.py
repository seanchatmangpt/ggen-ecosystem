from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-188-maximum-rank", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT (MAX(?rank) AS ?value) WHERE { ?s ex:rank ?rank } ORDER BY ?value''', 1)

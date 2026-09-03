from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-170-if-conditional", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:rank ?rank . BIND(IF(?rank > 1, "high", "low") AS ?value) } ORDER BY ?value''', 3)

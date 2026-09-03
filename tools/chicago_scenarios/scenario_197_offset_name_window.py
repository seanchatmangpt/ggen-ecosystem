from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-197-offset-name-window", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value } ORDER BY ?value OFFSET 1 LIMIT 2''', 2)

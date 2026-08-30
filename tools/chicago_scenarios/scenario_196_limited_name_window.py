from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("limited-name-window", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value } ORDER BY ?value LIMIT 2''', 2)

from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("offset-name-window", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT ?value WHERE { ?s ex:name ?value } ORDER BY ?value OFFSET 1 LIMIT 2''', 2)

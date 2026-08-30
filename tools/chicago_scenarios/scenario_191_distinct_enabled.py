from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("distinct-enabled", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT DISTINCT ?value WHERE { ?s ex:enabled ?value } ORDER BY ?value''', 2)

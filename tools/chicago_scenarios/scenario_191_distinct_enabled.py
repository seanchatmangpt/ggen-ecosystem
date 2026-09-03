from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-191-distinct-enabled", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT DISTINCT ?value WHERE { ?s ex:enabled ?value } ORDER BY ?value''', 2)

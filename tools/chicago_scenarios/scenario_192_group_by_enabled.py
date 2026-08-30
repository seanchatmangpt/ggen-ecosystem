from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("group-by-enabled", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT (COUNT(?s) AS ?value) WHERE { ?s ex:enabled ?enabled } GROUP BY ?enabled ORDER BY ?value''', 2)

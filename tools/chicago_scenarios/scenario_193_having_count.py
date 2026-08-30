from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-193-having-count", '''PREFIX ex: <https://example.org/chicago-consumer#> SELECT (COUNT(?s) AS ?value) WHERE { ?s ex:enabled ?enabled } GROUP BY ?enabled HAVING(COUNT(?s) >= 1) ORDER BY ?value''', 2)

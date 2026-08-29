from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("grouped-count-boolean", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (COUNT(?s) AS ?value) WHERE { ?s ex:enabled ?enabled } GROUP BY ?enabled ORDER BY ?value''', 2)


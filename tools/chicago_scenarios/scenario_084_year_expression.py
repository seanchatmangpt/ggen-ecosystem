from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("year-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:when ?when . BIND(YEAR(?when) AS ?value) } ORDER BY ?value''', 3)


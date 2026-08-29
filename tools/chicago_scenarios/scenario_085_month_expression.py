from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("month-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:when ?when . BIND(MONTH(?when) AS ?value) } ORDER BY ?value''', 3)


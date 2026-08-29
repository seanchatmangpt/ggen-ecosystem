from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("day-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:when ?when . BIND(DAY(?when) AS ?value) } ORDER BY ?value''', 3)


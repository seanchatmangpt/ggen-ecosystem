from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("absolute-value", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?rank . BIND(ABS(-?rank) AS ?value) } ORDER BY ?value''', 3)


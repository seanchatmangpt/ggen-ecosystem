from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("arithmetic-precedence", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?rank . BIND((?rank + 1) * 2 AS ?value) } ORDER BY ?value''', 3)


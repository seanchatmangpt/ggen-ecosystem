from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("subtraction-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?rank . BIND(?rank - 1 AS ?value) } ORDER BY ?value''', 3)


from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("decimal-subtraction", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:amount ?amount . BIND(?amount - 0.25 AS ?value) } ORDER BY ?value''', 3)


from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("decimal-addition", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:amount ?amount . BIND(?amount + 0.5 AS ?value) } ORDER BY ?value''', 3)


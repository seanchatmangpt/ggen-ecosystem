from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("round-decimal", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:amount ?amount . BIND(ROUND(?amount) AS ?value) } ORDER BY ?value''', 3)


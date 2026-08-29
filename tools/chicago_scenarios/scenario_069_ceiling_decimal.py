from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ceiling-decimal", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:amount ?amount . BIND(CEIL(?amount) AS ?value) } ORDER BY ?value''', 3)


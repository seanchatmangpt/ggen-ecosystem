from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("floor-decimal", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:amount ?amount . BIND(FLOOR(?amount) AS ?value) } ORDER BY ?value''', 3)


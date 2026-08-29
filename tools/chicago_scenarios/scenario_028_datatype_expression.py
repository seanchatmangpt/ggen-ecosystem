from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("datatype-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:amount ?amount . BIND(DATATYPE(?amount) AS ?value) } ORDER BY ?value''', 3)

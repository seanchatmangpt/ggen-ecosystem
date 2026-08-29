from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("decimal-literal", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:amount ?value } ORDER BY ?value''', 3)

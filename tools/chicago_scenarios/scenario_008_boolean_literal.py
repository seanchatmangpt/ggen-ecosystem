from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("boolean-literal", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:enabled ?value } ORDER BY ?value''', 3)

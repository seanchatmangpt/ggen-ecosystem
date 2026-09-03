from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("date-literal", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:when ?value } ORDER BY ?value''', 3)

from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("instance-identity", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?value a ex:Thing } ORDER BY ?value''', 2)

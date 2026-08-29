from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("integer-rank", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?value } ORDER BY ?value''', 3)

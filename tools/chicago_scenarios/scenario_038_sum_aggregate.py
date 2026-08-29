from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("sum-aggregate", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (SUM(?rank) AS ?value) WHERE { ?s ex:rank ?rank } ORDER BY ?value''', 1)

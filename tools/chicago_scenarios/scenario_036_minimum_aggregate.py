from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("minimum-aggregate", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (MIN(?rank) AS ?value) WHERE { ?s ex:rank ?rank } ORDER BY ?value''', 1)

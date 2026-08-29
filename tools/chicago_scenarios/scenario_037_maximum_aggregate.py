from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("maximum-aggregate", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (MAX(?rank) AS ?value) WHERE { ?s ex:rank ?rank } ORDER BY ?value''', 1)

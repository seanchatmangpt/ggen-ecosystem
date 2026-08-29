from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("having-sum", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (SUM(?rank) AS ?value) WHERE { ?s ex:enabled ?enabled ; ex:rank ?rank } GROUP BY ?enabled HAVING(SUM(?rank) >= 2) ORDER BY ?value''', 2)


from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("grouped-sum-boolean", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (SUM(?rank) AS ?value) WHERE { ?s ex:enabled ?enabled ; ex:rank ?rank } GROUP BY ?enabled ORDER BY ?value''', 2)


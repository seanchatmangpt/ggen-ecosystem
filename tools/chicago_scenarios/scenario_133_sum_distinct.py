from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("sum-distinct", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (SUM(DISTINCT ?rank) AS ?value) WHERE { ?s ex:rank ?rank } ORDER BY ?value''', 1)


from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("average-distinct", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (AVG(DISTINCT ?rank) AS ?value) WHERE { ?s ex:rank ?rank } ORDER BY ?value''', 1)


from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("distinct-count", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT (COUNT(DISTINCT ?s) AS ?value) WHERE { ?s ex:name ?name } ORDER BY ?value''', 1)
